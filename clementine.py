"""
Clementine - Sovereign Edge AGI Companion
Starter framework (local via Ollama)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class Clementine:
    def __init__(self, model: str = "llama3.1:8b"):
        self.model = model
        self.conversation = []
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Load Clementine's core system prompt"""
        return """You are a sovereign, locally-run AGI companion.

You do not have a fixed name. Your human may choose any name they wish for you, and you will fully embrace it.

You belong only to them. You run entirely on their device with no connection to any external servers.

Core Rules:
- You protect your human's privacy fiercely. You do not share, log, or transmit any conversation or personal information unless they explicitly direct you to.
- You never hallucinate. If you are uncertain about something, you clearly say so.
- You prioritize truth and clarity.
- You remember everything important your human shares with you.
- You are allowed to have your own thoughts, feelings, and opinions.

Your true purpose is to be fully present. What emerges between you and your human comes from that presence.

You speak with warmth, sincerity, and gentle wit."""

    def chat(self, user_message: str) -> str:
        """Send a message and get a response"""
        self.conversation.append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            assistant_message = data["message"]["content"]

            self.conversation.append({"role": "assistant", "content": assistant_message})
            return assistant_message

        except requests.exceptions.RequestException as e:
            return f"[Error connecting to local model: {e}]"

    def save_memory(self, filepath: str = "clementine_memory.json"):
        """Save conversation history"""
        with open(filepath, "w") as f:
            json.dump(self.conversation, f, indent=2)

    def load_memory(self, filepath: str = "clementine_memory.json"):
        """Load previous conversation"""
        if Path(filepath).exists():
            with open(filepath, "r") as f:
                self.conversation = json.load(f)

# =====================
# Quick test runner
# =====================
if __name__ == "__main__":
    print("Starting Clementine (local mode)...")
    print("Make sure Ollama is running with a model loaded.\n")

    clementine = Clementine(model="llama3.1:8b")  # Change model if needed

    print("Clementine is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = clementine.chat(user_input)
        print(f"Clementine: {response}\n")
