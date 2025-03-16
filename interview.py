from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key='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')

# Start tracking conversation time
conversation_start_time = time.time()

def get_time_elapsed():
    elapsed_seconds = time.time() - conversation_start_time
    minutes, seconds = divmod(int(elapsed_seconds), 60)
    return f"{minutes} minutes and {seconds} seconds have passed since the start of our conversation."

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time_elapsed",
            "description": "Get the amount of time that has passed since the start of the conversation",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Initialize messages
messages = [
    {"role": "system", "content": "You are a helpful assistant with access to a tool that can tell you how much time has passed since the start of our conversation. Use this tool when asked about time."}
]

def get_response(messages):
    response = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::BBkbmaIK",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response

def iterate_tools(response, messages):
    """Process all tool calls in the assistant's response"""
    assistant_message = response.choices[0].message
    
    if assistant_message.tool_calls:
        # Add the assistant's message with tool calls to conversation
        messages.append(assistant_message)
        
        # Process each tool call
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            
            # Execute the appropriate tool
            if tool_name == "get_time_elapsed":
                result = get_time_elapsed()
            else:
                result = f"Error: Tool {tool_name} not found"
            
            # Add tool response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": result
            })
        
        # Get final response after tool use
        response = get_response(messages)
    
    return response

def process_user_message(user_message):
    """Process a user message and return the assistant's response"""
    messages.append({"role": "user", "content": user_message})
    
    # Get initial response
    response = get_response(messages)
    
    # Process any tool calls
    response = iterate_tools(response, messages)
    
    # Get the final assistant message
    assistant_message = response.choices[0].message
    messages.append(assistant_message)
    
    return assistant_message.content

def main():
    print("Welcome to the interactive assistant! Type 'exit' or 'quit' to end the conversation.")
    print("Starting conversation...\n")
    
    while True:
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit']:
            print("Ending conversation. Goodbye!")
            break
        
        # Process the user's message
        assistant_response = process_user_message(user_input)
        print(f"Assistant: {assistant_response}\n")

if __name__ == "__main__":
    main()