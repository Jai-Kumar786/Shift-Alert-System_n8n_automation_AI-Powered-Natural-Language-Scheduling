# Day11_12/scheduling_tool.py
from langchain.tools import tool
from langchain_community.llms import Ollama
import datetime
import json
import re
from dateutil import parser

# Initialize LLM for data extraction
llm = Ollama(model="phi3", temperature=0.1)


@tool
def extract_shift_details(user_query: str) -> str:
    """
    Extracts structured shift scheduling data from natural language input.
    Returns JSON with date, day, start_time, and end_time.

    Args:
        user_query: Natural language scheduling request

    Returns:
        JSON string with extracted shift details including day of week
    """

    print(f"\n🔧 Tool called with query: {user_query}")

    # Create extraction prompt
    extraction_prompt = f"""
Extract shift scheduling information from this text: "{user_query}"

Today's date is: {datetime.datetime.now().strftime('%Y-%m-%d %A')}

Extract:
1. The date (convert relative dates like "tomorrow", "Monday" to YYYY-MM-DD format)
2. Start time (convert to HH:MM 24-hour format)
3. End time (convert to HH:MM 24-hour format)

Rules:
- If no specific date is mentioned, return today's date
- Convert 12-hour time to 24-hour format
- If only day name is given (Monday, Tuesday, etc.), find the next occurrence

Return ONLY valid JSON in this exact format:
{{
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM"
}}

Return ONLY the JSON object, nothing else.
"""

    try:
        # Get LLM response
        print("🤖 Calling LLM for extraction...")
        llm_response = llm.invoke(extraction_prompt)
        print(f"🔍 Raw LLM response:\n{llm_response}\n")

        # Clean the response
        llm_response = llm_response.strip()

        # Extract JSON from response (handle markdown code blocks)
        if "```":
            json_match = re.search(r'```json\s*(\{.*?\})\s*```')
            if json_match:
                llm_response = json_match.group(1)
            elif "```" in llm_response:
                json_match = re.search(r'``````', llm_response, re.DOTALL)
            if json_match:
                llm_response = json_match.group(1)

                # Try to parse as JSON
        try:
            extracted_data = json.loads(llm_response)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            json_match = re.search(r'\{[^}]+\}', llm_response)
            if json_match:
                extracted_data = json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in LLM response")

        # Validate extracted data
        required_fields = ['date', 'start_time', 'end_time']
        if not all(field in extracted_data for field in required_fields):
            missing = [f for f in required_fields if f not in extracted_data]
            raise ValueError(f"Missing required fields: {missing}")

        # Parse the date and extract day of week
        date_str = extracted_data['date']
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime('%A')  # Full day name (Monday, Tuesday, etc.)

        # Format the response with day included
        result = {
            "status": "success",
            "data": {
                "date": extracted_data['date'],
                "day": day_of_week,  # ← Added day of week
                "start_time": extracted_data['start_time'],
                "end_time": extracted_data['end_time']
            }
        }

        print(f"✅ Extraction successful!")
        print(f"📊 Result: {json.dumps(result, indent=2)}\n")

        return json.dumps(result)

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")

        error_result = {
            "status": "error",
            "error": str(e),
            "data": None
        }

        return json.dumps(error_result)


# Standalone function for direct use (optional)
def extract_shift_details_from_text(text: str) -> dict:
    """
    Direct extraction function that returns a dict instead of JSON string
    """
    result_json = extract_shift_details(text)
    result = json.loads(result_json)

    if result.get("status") == "success":
        return result.get("data")
    return None


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Shift Extraction Tool\n")

    test_queries = [
        "I want to work tomorrow 9am to 5pm",
        "Schedule me for Monday 10:00 to 14:00",
        "I'm available next Friday from 8am to 12pm",
        "Can I work October 30th 9:00-17:00?",
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"Testing: {query}")
        print(f"{'=' * 60}")
        result = extract_shift_details(query)
        print(f"Result: {result}\n")
