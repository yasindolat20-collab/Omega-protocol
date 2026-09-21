import os
import time
from typing import Optional, Dict, List
from openai import OpenAI


class LLMGateway:
    """دروازه چندمدلی با fallback خودکار"""

    def __init__(self):
        self.providers = []
        self.stats = {"success": {}, "failure": {}}

        # Groq (رایگان، سریع)
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            self.providers.append({
                "name": "groq",
                "client": OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key),
                "model": "llama-3.3-70b-versatile",
                "priority": 1,
            })

        # Zhipu GLM (رایگان)
        zai_key = os.environ.get("ZAI_API_KEY")
        if zai_key:
            self.providers.append({
                "name": "glm",
                "client": OpenAI(base_url="https://open.bigmodel.cn/api/paas/v4", api_key=zai_key),
                "model": "glm-4-flash",
                "priority": 2,
            })

        # OpenRouter (رایگان، چند مدل)
        or_key = os.environ.get("OPENROUTER_API_KEY")
        if or_key:
            self.providers.append({
                "name": "openrouter",
                "client": OpenAI(base_url="https://openrouter.ai/api/v1", api_key=or_key),
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "priority": 3,
            })

        self.providers.sort(key=lambda p: p["priority"])
        if not self.providers:
            print("WARNING: No API keys found. Set GROQ_API_KEY, ZAI_API_KEY, or OPENROUTER_API_KEY")
        else:
            print(f"Loaded {len(self.providers)} providers: {[p['name'] for p in self.providers]}")

    def ask(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7) -> Optional[str]:
        """پرسش از مدل‌ها با fallback خودکار"""
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
                print(f"[{name}] FAIL: {str(e)[:80]}")
                continue
        print("All providers failed")
        return None

    def get_stats(self) -> Dict:
        return self.stats


if __name__ == "__main__":
    gateway = LLMGateway()
    print("\n--- Test 1 ---")
    ans = gateway.ask("به یک جمله کوتاه بگو: پایتخت ایران کجاست؟")
    print(f"Answer: {ans}\n")

    print("--- Test 2 ---")
    ans = gateway.ask("در یک جمله: چرا حکومت‌ها فروپاشی می‌کنند؟")
    print(f"Answer: {ans}\n")

    print("=== Stats ===")
    print(gateway.get_stats())
