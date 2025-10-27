# Day11_12/agent_with_tool.py
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from scheduling_tool import extract_shift_details

# Initialize the LLM
llm = Ollama(model="phi3", temperature=0.8)

# Define the agent prompt
agent_prompt = PromptTemplate.from_template("""
You are a friendly and helpful shift scheduling assistant.

You have access to the following tool:
{tools}

Tool Names: {tool_names}

When a user wants to schedule a shift, use the extract_shift_details tool to get structured data.

Always be conversational and friendly. Confirm shift details back to the user.

Question: {input}
Thought: {agent_scratchpad}
""")

# Create tools list
tools = [extract_shift_details]

# Create the agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=agent_prompt
)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)


def process_with_tool(user_input: str) -> str:
    """
    Process user input with the agent and return conversational response
    """
    try:
        result = agent_executor.invoke({"input": user_input})
        return result['output']
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}"


# Test the agent
if __name__ == "__main__":
    print("🤖 Testing Conversational Agent with Tools\n")

    test_queries = [
        "I want to work tomorrow from 9am to 5pm",
        "What's the weather like?",
        "Schedule me for Monday 10 to 2",
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"User: {query}")
        print(f"{'=' * 60}")
        response = process_with_tool(query)
        print(f"Agent: {response}\n")
