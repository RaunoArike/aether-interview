from openai import OpenAI
import json
client = OpenAI(api_key='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')

messages = []

def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response

def process_user_message(user_message):
    """Process a user message and return the assistant's response"""
    messages.append({"role": "user", "content": user_message})
    
    # Get initial response
    response = get_response(messages)
    
    # Get the final assistant message
    assistant_message = response.choices[0].message
    messages.append(assistant_message)
    
    return assistant_message.content

def edit_last_assistant_message(new_content):
    """Edit the most recent assistant message"""
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].role == "assistant":
            messages[i].content = new_content
            return True
    return False

def save_conversation_to_file(filename="finetune.jsonl"):
    """Save the current conversation to a JSONL file"""
    with open(filename, "a") as f:
        f.write(json.dumps({"messages": messages}) + "\n")
    return f"Conversation saved to {filename}"

def main():
    print("Welcome to the interactive assistant! Type 'exit' or 'quit' to end the conversation.")
    print("Commands: '!save' to save conversation, '!edit' to edit last assistant message")
    print("Starting conversation...\n")
    
    while True:
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit']:
            print("Ending conversation. Goodbye!")
            break
        
        # Check for special commands
        if user_input.startswith("!save"):
            filename = "finetune.jsonl"
            if len(user_input) > 6:  # If there's something after !save
                filename = user_input[6:].strip()
            result = save_conversation_to_file(filename)
            print(f"System: {result}")
            continue
            
        if user_input.startswith("!edit"):
            new_content = input("Enter new content for the last assistant message: ")
            if edit_last_assistant_message(new_content):
                print("System: Last assistant message updated.")
            else:
                print("System: No assistant message found to edit.")
            continue
        
        # Process the user's message
        assistant_response = process_user_message(user_input)
        print(f"Assistant: {assistant_response}\n")

if __name__ == "__main__":
    main()