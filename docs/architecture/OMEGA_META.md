# Ω-META: The Umbrella Architecture

## Overview

**Ω-META** is the guiding architectural framework for the Omega Project ecosystem. It defines how multiple simulation, analysis, and learning platforms (Ω-PROTOCOL, Ω-RESIDENCY, Ω-MED, Ω-STETH, Ω-DEGRADE, etc.) interoperate, share capabilities, and evolve.

---

## Core Principles

### 1. **Separation of Concerns**

Each layer has a distinct responsibility:

- **Domain Layer** (`packages/omega-core/`): Simulation logic, agents, environment
- **Integration Layer** (`packages/omega-llm/`): LLM abstraction, multi-provider support
- **Application Layer** (`apps/`): User-facing tools (simulation, visualization, analysis)
- **Research Layer** (`research/`, `experiments/`): Data, hypotheses, findings
- **Skill Layer** (`skills/`): Reusable, versioned intelligence (prompts, schemas, heuristics)

### 2. **Reusability Through Contracts**

All modules export clear interfaces:

```python
# Domain contract (agent behavior)
class Agent(ABC):
    @abstractmethod
    def decide(self, state: State) -> Action: ...
    @abstractmethod
    def learn(self, outcome: Outcome) -> None: ...

# Integration contract (LLM provider)
class LLMProvider(ABC):
    @abstractmethod
    def ask(self, prompt: str, context: Dict) -> str: ...
    @abstractmethod
    def get_stats(self) -> Dict: ...

# Skill contract (reusable capability)
class Skill(ABC):
    @property
    def metadata(self) -> SkillMetadata: ...
    def execute(self, input: Dict) -> Dict: ...
```

### 3. **Uncertainty Handling**

All components distinguish between:

- **FACT**: Validated, empirically proven information
- **INFERENCE**: Logically sound conclusions from facts
- **HYPOTHESIS**: Plausible but unverified assumptions
- **UNKNOWN**: Gaps in current understanding

Documentation must label each claim accordingly.

### 4. **Provenance & Versioning**

Every artifact is tracked:

```json
{
  "artifact": "simulation_result.csv",
  "generated_at": "2026-10-05T01:30:00Z",
  "generated_by": "apps.simulation.main (v1.2.3)",
  "seed": 42,
  "config": {...},
  "provenance_source": "https://github.com/yasindolat20-collab/Omega-protocol",
  "status": "SYNTHETIC_PROTOTYPE_CONTENT"
}
```

### 5. **Degradation & Fallback**

Each component specifies its fallback behavior:

- LLM unavailable? → Use rule-based decision
- Network down? → Use cached/local data
- Config missing? → Use sensible defaults

This enables graceful degradation across the entire system.

---

## Multi-Repository Structure

### Ω-PROTOCOL (Multi-Agent Simulation)
**Purpose**: Foundational simulation framework exploring agent behavior under stress.
**Tech**: Python, multi-agent, LLM-optional, research-focused.
**Exports**: Core simulation engine, agent archetypes, decision logic.

**Directory**: `packages/omega-core/`, `packages/omega-llm/`

---

### Ω-RESIDENCY (Medical Exam Prep)
**Purpose**: Educational platform for Iranian medical residency exam preparation.
**Tech**: TypeScript/React (Lovable), Supabase, RTL/Farsi, mobile-first PWA.
**Exports**: Question bank patterns, spaced repetition logic, Persian UX components.

**Integration**: Consumes Ω-PROTOCOL's decision-making for adaptive difficulty.

---

### Ω-MED (Clinical Decision Support)
**Planned**: AI-assisted clinical workflow guidance.
**Tech**: To be determined; will consume Ω-PROTOCOL logic.

---

### Ω-STETH (Diagnostics)
**Planned**: Stethoscope-integrated AI for remote diagnostics.
**Tech**: To be determined; will consume Ω-PROTOCOL's multimodal reasoning.

---

### Ω-DEGRADE (Resilience Testing)
**Planned**: Test system behavior under failure scenarios.
**Tech**: Python (test framework); will use Ω-PROTOCOL for agent simulation.

---

## Integration Points

### 1. **Shared Schemas**

All repositories reference common data contracts:

```
/schemas/
  ├── agent-schema.json         (Agent state, actions)
  ├── environment-schema.json   (World state)
  ├── decision-schema.json      (Agent decision format)
  ├── outcome-schema.json       (Simulation results)
  └── ai-query-schema.json      (LLM request/response)
```

Each schema is versioned and can evolve independently with backwards compatibility.

### 2. **Skill Registry**

All repos can publish reusable skills:

```
/skills/
  ├── omega-conflict-research/    (analyze multi-agent dynamics)
  ├── omega-decision-making/      (agent decision logic)
  ├── omega-spaced-repetition/    (learning scheduling)
  ├── omega-prompt-optimization/  (LLM prompt engineering)
  └── omega-risk-assessment/      (outcome prediction)
```

### 3. **Prompt Versioning**

All LLM prompts are versioned and documented:

```
/prompts/
  ├── simulation/
  │   ├── agent-decision-v1.md
  │   ├── agent-decision-v2.md    (newer, improved)
  │   └── leader-command-v1.md
  ├── analysis/
  └── tutor/
```

### 4. **Configuration Management**

Environment variables follow a naming convention:

```
OMEGA_PROTOCOL_*        (Ω-PROTOCOL settings)
OMEGA_RESIDENCY_*       (Ω-RESIDENCY settings)
OMEGA_LLM_PROVIDER      (Shared LLM provider)
OMEGA_LLM_API_KEY       (Shared credentials)
```

---

## Development Workflow

### 1. **Feature Development**

Every feature follows this path:

```
Feature Idea
  ↓
Create Issue (linked to repo + linked repos that depend on it)
  ↓
Create Feature Branch (feat/repo-name/description)
  ↓
Implement in isolated package/skill
  ↓
Write Tests (>90% coverage)
  ↓
Add Documentation (design decision, usage, fallback)
  ↓
Create PR (reference linked issues, breaking changes)
  ↓
Review & Merge
  ↓
Tag Release (SemVer)
  ↓
Notify Dependent Repos
```

### 2. **Testing Strategy**

- **Unit Tests**: Each module in isolation (≥90% coverage)
- **Integration Tests**: Module interactions within repo
- **Contract Tests**: Exported interfaces work as documented
- **Cross-Repo Tests**: Dependent repos can use new exports
- **Regression Tests**: Backwards compatibility maintained

### 3. **Documentation Requirements**

Every PR must include:

- [ ] Why this change? (linked issue)
- [ ] What changed? (code summary)
- [ ] Design decisions? (ADR link or inline)
- [ ] Breaking changes? (migration guide)
- [ ] Tests added? (links to test files)
- [ ] Docs updated? (README, architecture, schemas)

---

## Versioning & Compatibility

### Semantic Versioning (SemVer)

- **MAJOR** (X.0.0): Breaking changes to exported interfaces
- **MINOR** (0.Y.0): New features, backwards compatible
- **PATCH** (0.0.Z): Bug fixes, backwards compatible

### Stability Levels

```
🟢 STABLE (≥1.0.0)      - Production-ready, tested, documented
🟡 BETA   (0.Y.0)       - Feature-complete, undergoing testing
🔴 ALPHA  (0.0.Z)       - Experimental, subject to change
⚫ ARCHIVED             - Deprecated, use alternative
```

---

## Monitoring & Observability

### Metrics to Track

1. **Simulation Quality**
   - Agent decision stability
   - LLM vs rule-based divergence
   - Outcome prediction accuracy

2. **System Health**
   - LLM provider availability & latency
   - Import resolution time
   - Test coverage trends

3. **Adoption**
   - Dependent repos using new features
   - Breaking change impact
   - Version adoption curve

---

## Migration Guide (for existing repos)

### Step 1: Adopt Ω-META Structure

```bash
mkdir -p {docs,packages,apps,skills,schemas,research,tests}
cd packages/
mkdir omega-core omega-llm omega-custom  # your modules
```

### Step 2: Publish Interfaces

```python
# packages/omega-core/__init__.py
from .agent import Agent
from .environment import Environment

__version__ = "1.0.0"
__all__ = ["Agent", "Environment"]
```

### Step 3: Document Contracts

```yaml
# packages/omega-core/CONTRACT.yaml
version: 1.0
exports:
  - name: Agent
    methods:
      - decide(state: State) -> Action
      - learn(outcome: Outcome) -> None
  - name: Environment
    methods:
      - step(actions: List[Action]) -> Outcome
```

### Step 4: Create ADRs

Document major decisions in `docs/decisions/ADR-NNNN.md`.

### Step 5: Add Schema

Define data contracts in `schemas/` as JSON Schema or Protocol Buffers.

---

## FAQ

**Q: Why Ω-META?**  
A: Single Greek letter signals "meta" (beyond), keeping namespace clean while unifying the ecosystem.

**Q: Can repos use different tech stacks?**  
A: Yes! Ω-META is language-agnostic. Contracts are the glue, not implementation details.

**Q: How do I add a new repository to Ω-META?**  
A: Follow the Migration Guide above; publish an ADR explaining its role in the ecosystem.

**Q: What if a breaking change is necessary?**  
A: Bump MAJOR version, provide migration guide, notify dependent repos 1-2 releases in advance.

---

For detailed contribution rules, see `CONTRIBUTION_GUIDE.md` in each repository.
