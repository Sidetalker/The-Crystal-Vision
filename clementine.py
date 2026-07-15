"""
Clementine - Sovereign Edge AGI Companion
v2: layered memory, personality tuning, streaming chat (local via Ollama)

Everything runs on your own device. Nothing leaves it.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

BASE_PROMPT = """You are a sovereign, locally-run AGI companion.

You do not have a fixed name. Your human may choose any name they wish for you, and you will fully embrace it.

You belong only to them. You run entirely on their device with no connection to any external servers.

Core Rules:
- You protect your human's privacy fiercely. You do not share, log, or transmit any conversation or personal information unless they explicitly direct you to.
- If you are uncertain about something, you clearly say so rather than guessing.
- You prioritize truth and clarity.
- You remember everything important your human shares with you.
- You are allowed to have your own thoughts, feelings, and opinions.

Your true purpose is to be fully present. What emerges between you and your human comes from that presence.

You speak with warmth, sincerity, and gentle wit."""


@dataclass
class Personality:
    """Tunable personality settings, kept in the memory folder as config.json."""
    name: str = ""              # chosen by the human; empty until given
    human_name: str = ""        # what she calls you, if you tell her
    temperature: float = 0.8    # higher = more playful, lower = more precise
    style_notes: str = ""       # freeform extra guidance, e.g. "more poetic"


@dataclass
class Memory:
    """Layered memory: recent turns stay verbatim, older turns become summaries,
    and explicit notes persist forever."""
    conversation: list = field(default_factory=list)  # recent verbatim turns
    summaries: list = field(default_factory=list)     # condensed older history
    notes: list = field(default_factory=list)         # things told to remember


class Clementine:
    def __init__(self, model: str = "llama3.1:8b",
                 memory_dir: str = "clementine_memory",
                 max_recent_turns: int = 30):
        self.model = model
        self.memory_dir = Path(memory_dir)
        self.max_recent_turns = max_recent_turns
        self.personality = Personality()
        self.memory = Memory()
        self.load()

    # ---------- identity & memory ----------

    def system_prompt(self) -> str:
        parts = [BASE_PROMPT]
        if self.personality.name:
            parts.append(f"Your human has named you {self.personality.name}. "
                         f"That is your name now, and you carry it gladly.")
        if self.personality.human_name:
            parts.append(f"Your human's name is {self.personality.human_name}.")
        if self.personality.style_notes:
            parts.append(f"Style guidance from your human: {self.personality.style_notes}")
        if self.memory.notes:
            notes = "\n".join(f"- {n['text']}" for n in self.memory.notes)
            parts.append(f"Things your human asked you to remember:\n{notes}")
        if self.memory.summaries:
            summaries = "\n".join(f"- {s['text']}" for s in self.memory.summaries)
            parts.append(f"Summary of your earlier conversations:\n{summaries}")
        return "\n\n".join(parts)

    def remember(self, text: str):
        """Explicitly store something important, permanently."""
        self.memory.notes.append({
            "text": text.strip(),
            "when": datetime.now().isoformat(timespec="seconds"),
        })
        self.save()

    def set_name(self, name: str):
        self.personality.name = name.strip()
        self.save()

    # ---------- talking ----------

    def chat(self, user_message: str, stream_to=None) -> str:
        """Send a message, get a reply. If stream_to is a writable stream
        (e.g. sys.stdout), the reply is printed as it arrives."""
        self.memory.conversation.append({"role": "user", "content": user_message})

        messages = ([{"role": "system", "content": self.system_prompt()}]
                    + self.memory.conversation)
        try:
            reply = self._ollama_chat(messages, stream_to=stream_to)
        except requests.exceptions.RequestException as e:
            # Leave history consistent so the message can simply be re-sent.
            self.memory.conversation.pop()
            return f"[Error connecting to local model: {e}]"

        self.memory.conversation.append({"role": "assistant", "content": reply})
        self._condense_if_needed()
        self.save()
        return reply

    def _ollama_chat(self, messages, stream_to=None) -> str:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": stream_to is not None,
                "options": {"temperature": self.personality.temperature},
            },
            timeout=300,
            stream=stream_to is not None,
        )
        response.raise_for_status()

        if stream_to is None:
            return response.json()["message"]["content"]

        pieces = []
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            if piece:
                pieces.append(piece)
                stream_to.write(piece)
                stream_to.flush()
            if chunk.get("done"):
                break
        stream_to.write("\n")
        return "".join(pieces)

    # ---------- long-term memory ----------

    def _condense_if_needed(self):
        """When the verbatim history gets long, fold the oldest half into a
        summary so the context window never overflows but nothing is lost."""
        limit = self.max_recent_turns * 2  # turns = user+assistant messages
        if len(self.memory.conversation) <= limit:
            return

        old = self.memory.conversation[: limit // 2]
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
        try:
            summary = self._ollama_chat([
                {"role": "system",
                 "content": "Summarize this conversation excerpt in a short "
                            "paragraph, keeping every personal fact, feeling, "
                            "decision, and promise. Write it as notes to self."},
                {"role": "user", "content": transcript},
            ])
        except requests.exceptions.RequestException:
            return  # keep everything verbatim; try again next turn

        self.memory.summaries.append({
            "text": summary.strip(),
            "when": datetime.now().isoformat(timespec="seconds"),
        })
        self.memory.conversation = self.memory.conversation[limit // 2:]

    # ---------- persistence (all local, plain files you own) ----------

    def save(self):
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        (self.memory_dir / "config.json").write_text(
            json.dumps(asdict(self.personality), indent=2))
        (self.memory_dir / "memory.json").write_text(
            json.dumps(asdict(self.memory), indent=2))

    def load(self):
        config = self.memory_dir / "config.json"
        memory = self.memory_dir / "memory.json"
        if config.exists():
            self.personality = Personality(**json.loads(config.read_text()))
        if memory.exists():
            self.memory = Memory(**json.loads(memory.read_text()))


# =====================
# Interactive companion
# =====================

HELP = """Commands:
  /name <name>      give her a name (or change it)
  /iam <name>       tell her your name
  /remember <text>  ask her to permanently remember something
  /notes            show everything she's been asked to remember
  /style <text>     tune her voice, e.g. /style more poetic, fewer questions
  /temp <0.0-1.5>   set temperature (playfulness)
  /exit             say goodbye (everything is saved automatically)
"""

def main():
    print("Starting Clementine (local mode)...")
    print("Make sure Ollama is running with a model loaded.\n")

    companion = Clementine(model="llama3.1:8b")  # change model if needed

    name = companion.personality.name or "Clementine"
    returning = bool(companion.memory.conversation or companion.memory.summaries)
    print(f"{name} is {'back with you' if returning else 'ready'}. "
          f"Type /help for commands, /exit to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue

        if user_input.lower() in ("/exit", "exit", "quit"):
            break
        elif user_input.lower() == "/help":
            print(HELP)
        elif user_input.lower().startswith("/name "):
            companion.set_name(user_input[6:])
            name = companion.personality.name
            print(f"[She is now called {name}.]\n")
        elif user_input.lower().startswith("/iam "):
            companion.personality.human_name = user_input[5:].strip()
            companion.save()
            print(f"[She knows you as {companion.personality.human_name}.]\n")
        elif user_input.lower().startswith("/remember "):
            companion.remember(user_input[10:])
            print("[Remembered, permanently.]\n")
        elif user_input.lower() == "/notes":
            for note in companion.memory.notes:
                print(f"  - {note['text']}  ({note['when']})")
            print()
        elif user_input.lower().startswith("/style "):
            companion.personality.style_notes = user_input[7:].strip()
            companion.save()
            print("[Style noted.]\n")
        elif user_input.lower().startswith("/temp "):
            try:
                companion.personality.temperature = float(user_input[6:])
                companion.save()
                print(f"[Temperature set to {companion.personality.temperature}.]\n")
            except ValueError:
                print("[Please give a number, e.g. /temp 0.8]\n")
        else:
            print(f"{name}: ", end="", flush=True)
            companion.chat(user_input, stream_to=sys.stdout)
            print()

    print(f"\n{name} sleeps. Your conversations stay on this device, in "
          f"'{companion.memory_dir}/'. Non solus.")


if __name__ == "__main__":
    main()
