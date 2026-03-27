#!/usr/bin/env python3
"""Jarvis — Desktop AI Assistant with LLM Integration."""
import argparse, sys
from modules.listener import Listener
from modules.speaker import Speaker
from modules.parser import parse
from modules.executor import execute
from modules.llm_engine import LLMEngine
from config.settings import ASSISTANT_NAME

def main():
    ap = argparse.ArgumentParser(description="Jarvis Desktop Assistant")
    ap.add_argument("--text-only", action="store_true", help="Text input mode (no mic)")
    ap.add_argument("--mute", action="store_true", help="Disable voice output")
    args = ap.parse_args()

    speaker = Speaker()
    speak = speaker.mute_say if args.mute else speaker.say
    llm = LLMEngine()
    listener = None if args.text_only else Listener()

    speak(f"{ASSISTANT_NAME} online. {'LLM ready.' if llm.available else 'LLM disabled — set OPENAI_API_KEY.'}")

    while True:
        try:
            if args.text_only:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
            else:
                user_input = listener.listen()
                if not user_input:
                    continue

            if user_input in ("exit", "quit", "bye", "shutdown"):
                speak("Goodbye!")
                break

            # Try pattern-matched commands first
            cmd, arg = parse(user_input)
            if cmd == "clear_history":
                speak(llm.clear_history())
                continue
            if cmd:
                result = execute(cmd, arg)
                speak(result)
                continue

            # Fall through to LLM for general questions
            if llm.available:
                reply = llm.ask(user_input)
                # Check if LLM wants a system action
                if "[ACTION:" in reply:
                    import re
                    m = re.search(r"\[ACTION:(\w+):(.+?)\]", reply)
                    if m:
                        result = execute(m.group(1), m.group(2))
                        speak(result)
                        continue
                speak(reply)
            else:
                speak("I can only handle system commands without an LLM key. Try: open, search, find file, etc.")

        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"[Error] {e}")
            speak("Something went wrong. Please try again.")

if __name__ == "__main__":
    main()
