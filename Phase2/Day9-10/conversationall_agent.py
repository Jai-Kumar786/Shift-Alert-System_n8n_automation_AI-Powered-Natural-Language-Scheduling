from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import datetime

# Initialize LLM
llm = Ollama(model="phi3", temperature=0.8)

# Get current date
current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")

# System prompt
system_prompt = """You are a helpful and efficient scheduling assistant for an intern management system.

Your primary goal is to gather all necessary information to schedule a shift:
- Date (which day?)
- Start time (what time does it start?)
- End time (what time does it end?)

Be friendly, professional, and clear in your communication.
Ask ONE question at a time.
Do not perform any other tasks.

Today's date is: """ + current_date + """

Example conversation:
User: I need to book a shift
Assistant: Of course! What day would you like to schedule the shift?
User: Tomorrow
Assistant: Great! What time does the shift start?
User: 10am
Assistant: Perfect. And what time does it end?
User: 2pm
Assistant: Excellent! Shift scheduled for tomorrow from 10:00 AM to 2:00 PM.
"""

# Create memory with input_key specified
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="input"  # ← FIX: Specify which variable is the user input
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["chat_history", "input"],  # ← Only these two
    template=system_prompt + """

Current conversation:
{chat_history}

User: {input}
Assistant:"""
)

# Conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)

print("✅ Conversational agent ready!")
print(f"📅 Today's date: {current_date}\n")


# Interactive chat function
def chat_with_agent():
    """Interactive chat interface"""
    print("=" * 60)
    print("🤖 Scheduling Assistant Ready!")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation\n")

    while True:
        # Get user input
        user_input = input("👤 You: ").strip()

        # Check for exit command
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n🤖 Assistant: Thank you! Have a great day!")
            break

        # Skip empty inputs
        if not user_input:
            continue

        try:
            # Get response from agent
            response = conversation.predict(
                input=user_input  # ← Only pass 'input', not 'current_date'
            )

            print(f"\n🤖 Assistant: {response}\n")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.\n")


# Start the chat
if __name__ == "__main__":
    chat_with_agent()
