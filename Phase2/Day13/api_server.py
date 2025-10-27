# Phase2/Day13/api_server.py
# FINAL ROBUST VERSION - Fixes "tonight" bug

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import datetime
import re
from langchain_community.llms import Ollama

# --- Configuration ---
app = FastAPI(
    title="Intelligent Scheduling API",
    description="AI-powered shift scheduling with robust, direct extraction.",
    version="2.2.0"  # Version bump for the fix
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
llm = Ollama(model="phi3", temperature=0.0)


# --- Pydantic Models ---
class ScheduleRequest(BaseModel):
    query: str
    user_id: str


class ScheduleResponse(BaseModel):
    status: str
    response: str
    user_id: str
    shift_data: Optional[dict] = None


# --- Core Logic ---
def extract_shift_from_text(user_query: str) -> Optional[dict]:
    """
    Extracts structured shift data using an LLM, with robust JSON parsing
    and corrected date logic for relative terms like "tonight".
    """
    print(f"\n🔧 Extracting from query: '{user_query}'")

    now = datetime.datetime.now()
    today_date = now.strftime('%Y-%m-%d')
    today_day = now.strftime('%A')

    prompt = f"""
From the text "{user_query}", extract the shift details.
Today is {today_date} ({today_day}).

Return ONLY a valid JSON object with these keys:
- "day_name": The name of the day mentioned (e.g., "Monday", "tonight", "tomorrow").
- "start_time": The start time in HH:MM format.
- "end_time": The end time in HH:MM format.

Example for "I want to work tonight 9pm-11pm":
{{
  "day_name": "tonight",
  "start_time": "21:00",
  "end_time": "23:00"
}}

Your Response:
"""

    try:
        # 1. Get raw response from LLM
        response_str = str(llm.invoke(prompt)).strip()
        print(f"🔍 LLM Raw Response: {response_str}")

        # 2. Find and parse the first JSON object
        match = re.search(r'\{.*?\}', response_str, re.DOTALL)
        if not match:
            print("❌ No JSON object found in LLM response.")
            return None

        json_str = match.group(0)
        print(f"📊 Isolated JSON String: {json_str}")

        data = json.loads(json_str)

        # 3. Corrected Date Calculation Logic
        day_name_lower = data.get("day_name", "").lower()
        query_lower = user_query.lower()
        target_date = now

        # --- THIS IS THE FIX ---
        if 'tonight' in query_lower or 'today' in query_lower or day_name_lower == 'today':
            target_date = now
        elif 'tomorrow' in query_lower or day_name_lower == 'tomorrow':
            target_date = now + datetime.timedelta(days=1)
        else:
            days_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            if day_name_lower in days_map:
                target_weekday = days_map[day_name_lower]
                days_ahead = (target_weekday - now.weekday() + 7) % 7
                # If day is today BUT user didn't say "tonight/today", schedule for next week
                if days_ahead == 0:
                    days_ahead = 7
                target_date = now + datetime.timedelta(days=days_ahead)
        # --- END OF FIX ---

        # 4. Assemble and validate the final data
        final_shift_data = {
            "date": target_date.strftime('%Y-%m-%d'),
            "day": target_date.strftime('%A'),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }

        if not all(final_shift_data.values()):
            print("❌ Validation failed: Missing values in final data.")
            return None

        print(f"✅ Successfully extracted and validated shift data: {final_shift_data}")
        return final_shift_data

    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# --- API Endpoints ---
@app.get("/")
async def health_check():
    return {"status": "online", "service": "Shift Scheduling API v2.2", "version": "2.2.0"}


@app.post("/schedule", response_model=ScheduleResponse)
async def process_schedule_request(request: ScheduleRequest):
    try:
        print(f"\n{'=' * 60}\n📨 Request from {request.user_id}: '{request.query}'")

        shift_data = extract_shift_from_text(request.query)

        if shift_data:
            agent_response = (
                f"Got it! I've logged your shift for {shift_data['day']}, {shift_data['date']} "
                f"from {shift_data['start_time']} to {shift_data['end_time']}."
            )
        else:
            agent_response = (
                "My apologies, I couldn't understand the shift details. "
                "Could you please try again? For example: 'Schedule me for Tuesday 10am to 4pm'."
            )

        print(f"💬 Generated Response: {agent_response}")

        return ScheduleResponse(
            status="success",
            response=agent_response,
            user_id=request.user_id,
            shift_data=shift_data
        )

    except Exception as e:
        print(f"❌ Top-level error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Shift Scheduling API v2.2 (Date Fix)")
    print("🔗 URL: http://0.0.0.0:8000")
    print("📖 Docs: http://0.0.0.0:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
