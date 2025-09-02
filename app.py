# save this as app.py file
import json

from bedrock import Claude_Bedrock

with open("config.json") as f: 
    config = json.load(f)    # Load config
# Initialize Bedrock
client = Claude_Bedrock(**config)
conversation = []  # Store conversation history
print("🤖 Claude Sonnet 4 Demo (type 'quit;' to exit)")
print("-" * 40)

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == "quit;":
        break
    try:# Build conversation with history
        conversation.append({"role": "user", "content": user_input})
        client.user_prompt = json.dumps(conversation)  # Pass full history        
        response = client.invoke()    # Get response
        print(f"\nClaude: {response}")
        conversation.append({"role": "assistant", "content": response}) # Add to history
    except Exception as e:
        print(f"❌ Error: {e}")
print("\n👋 Goodbye!")
