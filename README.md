# Omega-Protocol

Multi-agent socio-political simulation with LLM-driven agents.

## Key Finding
LLM agents show cooperation bias — they prefer Loyalty even when the treasury is empty.

## Files
- main_llm.py — simulation loop
- agent.py — 6 archetypes
- environment.py — 4 resources + shocks
- network.py — social graph
- leader_llm.py — LLM ruler
- llm_gateway.py — API gateway
- compare.py — LLM vs rule-based

## Run
```bash
export GROQ_API_KEY="..."
python main_llm.py
```
