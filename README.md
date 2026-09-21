# Omega-Protocol

A multi-agent socio-political simulation framework exploring how rule-based and LLM-driven agents respond to economic stress, legitimacy shocks, and institutional leadership.

## Key Finding
LLM cooperation bias: when compared against a rule-based baseline, LLM-led populations consistently favor Loyalty and defer exit/rebellion even under tightening conditions, producing a more stable but less adaptive social profile.

| Scenario | Loyalty % | Exit % | Voice % | Rebellion % | Final Economy | Final Legitimacy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Rule-based | ~41.2 | ~26.1 | ~19.8 | ~13.0 | ~0.58 | ~0.56 |
| LLM-assisted | ~62.7 | ~11.4 | ~17.3 | ~8.6 | ~0.67 | ~0.71 |

## Architecture

```text
+-------------------+      +--------------------+
| Environment       | ---> | Social Network     |
| economy/legit     |      | agent connections  |
| military/treasury |      +--------------------+
+---------+---------+                 |
          |                           |
          v                           v
+-------------------+      +-------------------+
| Leader / Policy   | ---> | Agents            |
| command & power   |      | archetypes +     |
+-------------------+      | decision rules   |
                             +-------------------+
                                      |
                                      v
                            +-------------------+
                            | Shared Memory     |
                            | actions + success |
                            +-------------------+
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
python main_llm.py
python plot.py
python compare.py
python comparison_plot.py
python batch.py
python batch_plot.py
```

## File List
- agent.py — autonomous agents with archetypes, memory, and decision logic
- batch.py — 20-seed Monte Carlo simulation runner
- batch_plot.py — batch outcome visualization generator
- compare.py — rule-based versus LLM summary report
- comparison_plot.py — comparison chart across key metrics
- environment.py — environment state transitions and shocks
- leader.py — rule-based leader logic
- leader_llm.py — LLM-backed leadership logic
- llm_client.py — LLM interaction wrapper
- llm_gateway.py — gateway for LLM providers
- logger.py — CSV logging utility
- main.py — baseline simulation entry point
- main_llm.py — LLM-driven simulation entry point
- memory.py — per-agent memory object
- network.py — social graph generation
- plot.py — single-run plotting utility
- shared_memory.py — collective memory and success tracking
- README.md — project documentation
- requirements.txt — project dependencies

## Requirements
- Python 3.10+
- matplotlib
- numpy
- openai
- pytest
- rich

## License
This project is licensed under the Creative Commons Attribution 4.0 International License (CC-BY-4.0).

## Author
yasindolat20-collab

## CI
![CI](https://github.com/yasindolat20-collab/Omega-protocol/actions/workflows/ci.yml/badge.svg)

## Related Work (2026)

1. From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents. ACM Computing Surveys, 2026.
2. Belief-Driven Multi-Agent Collaboration via Approximate Perfect Bayesian Equilibrium for Social Simulation. ACM Web Conference, 2026.
3. Collective Alignment in LLM Multi-Agent Systems: Disentangling Bias from Cooperation via Statistical Physics. arXiv, 2026.
4. Evolutionary Dynamics of Cooperation in Next-Generation LLM Agent Systems. arXiv, 2026.
5. A survey of social network simulation in the LLM era. Elsevier, 2026.
