## save as bedrock.py file can be imported to your project
import json

import boto3


class Claude_Bedrock:
    def __init__(self, model="anthropic.claude-sonnet-4-20250514-v1:0", system_prompt="", 
                 user_prompt="", temperature=0.7, max_tokens=500, region="us-east-1"):
        self.model = model  # Claude model ID
        self.system_prompt = system_prompt  # System instructions
        self.user_prompt = user_prompt  # User message
        self.temperature = temperature  # Response randomness (0-1)
        self.max_tokens = max_tokens  # Max response length
        self.client = boto3.client("bedrock-runtime", region_name=region)  # Bedrock client    
    def invoke(self, user_prompt=None):
        prompt = user_prompt or self.user_prompt  # Use provided or stored prompt
        messages = json.loads(prompt) if prompt.startswith('[') else [{"role": "user", "content": prompt}] # Handle conversation history or single prompt
        body = {  # Request payload
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "system": self.system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        response = self.client.invoke_model(  # API call
            modelId=self.model,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )
        return json.loads(response["body"].read())["content"][0]["text"]  # Extract text

