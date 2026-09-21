import os
import time
from typing import Optional, Dict
from openai import OpenAI


class LLMGateway:
    def __init__(self):
        self.providers = []
        self.stats = {"success": {}, "failure": {}, "total_calls": 0}
        self._setup_providers()

    def _setup_providers(self):
        # Groq — تأیید شده که کار می‌کند
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            self.providers.append({
                "name": "groq",
                "client": OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=groq_key,
                ),
                "model": "openai/gpt-oss-20b",
                "priority": 1,
            })

        self.providers.sort(key=lambda p: p["priority"])
        if not self.providers:
            print("WARNING: No GROQ_API_KEY found.")
        else:
            print(f"Loaded {len(self.providers)} providers: {[p['name'] for p in self.providers]}")

    def ask(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7) -> Optional[str]:
        self.stats["total_calls"] += 1
        for provider in self.providers:
            name = provider["name"]
            try:
                t0 = time.time()
                response = provider["client"].chat.completions.create(
                    model=provider["model"],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                elapsed = time.time() - t0
                answer = response.choices[0].message.content.strip()
                self.stats["success"][name] = self.stats["success"].get(name, 0) + 1
                print(f"[{name}] OK ({elapsed:.2f}s)")
                return answer
            except Exception as e:
                self.stats["failure"][name] = self.stats["failure"].get(name, 0) + 1
                print(f"[{name}] FAIL: {str(e)[:120]}")
                continue
        return None

    def get_stats(self) -> Dict:
        return self.stats


if __name__ == "__main__":
    gw = LLMGateway()
    print("\n--- Test ---")
    ans = gw.ask("In one sentence, what is the capital of Iran?")
    print(f"Answer: {ans}")
    print(f"Stats: {gw.get_stats()}")
