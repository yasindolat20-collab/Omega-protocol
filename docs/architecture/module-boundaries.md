# Module boundaries

## Core runtime

The core runtime owns simulation state transitions and agent decision logic.

- `packages/omega_core/agent.py` — agent archetypes, strategy handling, decision logic.
- `packages/omega_core/environment.py` — economy, legitimacy, military, treasury transitions.
- `packages/omega_core/network.py` — social adjacency generation.
- `packages/omega_core/memory.py` — per-agent memory.
- `packages/omega_core/shared_memory.py` — shared observational memory.
- `packages/omega_core/leader.py` — command and surveillance logic.
- `packages/omega_core/logger.py` — simulation event logging.

## External adapters

- `packages/omega_core/llm_gateway.py` — provider gateway abstraction.
- `packages/omega_core/llm_client.py` — LLM decision adapter for agents.

## Application layer

- `apps/omega_simulation/*.py` — scripts that execute or analyze runs.

## Research and reusable systems

- `skills/` — reusable research skills, prompts, schemas, examples, and tests.
- `research/` — domain-specific research and notes.
- `docs/` — architecture, repository guidance, and decisions.

## Archive

- `archive/generated/` — generated artifacts intentionally retained but not treated as active source.
