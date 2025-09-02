# save as app.py
from bedrock import Claude_Bedrock

# Agent configurations
agents = {
    "Haiku": {
        "model": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "system_prompt": "You are Haiku, a fast and thoughtful assistant. Be like Will Smith in the fresh prince.",
        "temperature": 0.6
    },
    "Sonnet": {
        "model": "us.anthropic.claude-sonnet-4-20250514-v1:0", 
        "system_prompt": "You are Sonnet, an analytical reasoning expert. Be like Stephen Frye from QI.",
        "temperature": 0.9
    },
    "Opus": {
        "model": "us.anthropic.claude-opus-4-1-20250805-v1:0",
        "system_prompt": "You are Opus, a detail-oriented researcher. Be like Marvin from Hitch Hikers Guide.",
        "temperature": 0.5
    },
    "Compare": {
        "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "system_prompt": "You are Compare, a conversation reviewer. Return the best of the answer with justification and credit the agent.",
        "temperature": 0.7
    }
}

# Initialize agents
clients = {name: Claude_Bedrock(**config, max_tokens=500, region="us-east-1") 
            for name, config in agents.items()}
print("🤖 Multi-Agent Discussion System")
print("=" * 50)

while True:
    question = input("\n📝 Your question (or 'quit;'): ").strip()
    if question.lower() == 'quit;': break
    
    discussion = []  # Store agent responses
    print("\n🔄 Agents discussing...\n")
 
    for name, client in clients.items():    # Round 1: Each agent responds to user
        try:
            if name == "Compare": continue # Skip synthesis agent for now
            response = client.invoke(question)
            discussion.append(f"{name}: {response}")
            print(f"💭 {name}: {response}...")  # Show response
        except Exception as e:
            print(f"❌ {name} error: {e}")
    synthesis_prompt = f"Question: {question}\n\nAgent responses:\n" + "\n".join(discussion) # Round 2: Synthesis - Compare synthesizes all responses
    synthesis_prompt += "\n\nSynthesize the best answer from these perspectives:"    
    try:
        print("\n🎯 Final synthesis:")
        final = clients["Compare"].invoke(synthesis_prompt)
        print("-" * 50)
        print(final)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
print("\n👋 Goodbye!")
