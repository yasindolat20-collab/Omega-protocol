# Omega-Protocol Repository Inventory

## Overview
Multi-agent socio-political simulation framework exploring LLM vs rule-based agent behavior under stress.

**Repository ID:** 1379990808  
**Language:** Python (100%)  
**Created:** 13 days ago  
**License:** CC-BY-4.0  
**Visibility:** Public  

---

## Categorized File Inventory

### 🔧 Core Architecture (Reusable Simulation Engine)

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `agent.py` | Agent archetypes, decision logic, memory | Core Logic | ✅ Production |
| `environment.py` | State management, shocks, economic dynamics | Core Logic | ✅ Production |
| `leader.py` | Rule-based leader governance and surveillance | Core Logic | ✅ Production |
| `leader_llm.py` | LLM-backed leadership logic | Core Logic | ✅ Production |
| `memory.py` | Per-agent experience replay interface | Core Logic | ✅ Production |
| `shared_memory.py` | Collective memory, decay, success rates | Core Logic | ✅ Production |
| `network.py` | Social graph generation (Watts-Strogatz) | Core Logic | ✅ Production |

### 🤖 LLM Integration Layer

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `llm_gateway.py` | Multi-provider LLM abstraction (Groq) | Integration | ✅ Production |
| `llm_client.py` | Agent decision LLM wrapper with caching | Integration | ✅ Production |

### 📊 Application Entry Points

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `main.py` | Rule-based simulation (50 steps, 100 agents) | App | ✅ Production |
| `main_llm.py` | LLM-driven simulation entry point | App | ✅ Production |
| `plot.py` | Single-run result visualization | App | ✅ Production |
| `batch.py` | Monte Carlo runner (20 seeds) | App | ✅ Production |
| `batch_plot.py` | Batch results aggregation charts | App | ✅ Production |
| `compare.py` | Rule-based vs LLM comparison report | App | ✅ Production |
| `comparison_plot.py` | Comparative metrics visualization | App | ✅ Production |

### 📝 Utilities

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `logger.py` | CSV logging utility for simulation metrics | Utility | ✅ Production |

### 🧪 Testing & Validation

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `tests/test_core.py` | Unit tests for core modules | Test | ✅ Functional |
| `tests/__init__.py` | Test package marker | Test | ✅ Present |

### 📦 Configuration & Metadata

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `requirements.txt` | Python dependencies | Config | ✅ Current |
| `.gitignore` | Git exclusion rules | Config | ✅ Current |
| `README.md` | Project documentation | Docs | ✅ Current |
| `LICENSE` | CC-BY-4.0 license | Legal | ✅ Current |

### 📊 Generated Research Artifacts

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `simulation.csv` | Rule-based run results (50 steps) | Data | 🔍 Generated |
| `simulation_llm.csv` | LLM-driven run results | Data | 🔍 Generated |
| `batch_results.csv` | Monte Carlo aggregation (20 seeds) | Data | 🔍 Generated |
| `simulation_plot.png` | Single-run visualization | Asset | 🔍 Generated |
| `batch_plot.png` | Batch aggregation chart | Asset | 🔍 Generated |
| `comparison_plot.png` | LLM vs rule-based comparison | Asset | 🔍 Generated |

### 🗑️ Build Artifacts

| File | Purpose | Category | Status |
|------|---------|----------|--------|
| `__pycache__/` | Python bytecode cache | Artifact | ❌ Should be ignored |

---

## Module Dependency Map

```
┌─────────────────────────────────────────────┐
│            Simulation Engine                │
├─────────────────────────────────────────────┤
│  agent.py ─┐                                │
│  ├─ memory.py                               │
│  └─ shared_memory.py                        │
│                                             │
│  environment.py                             │
│  network.py                                 │
│                                             │
│  leader.py (rule-based)                     │
│  leader_llm.py → llm_client.py              │
│                  ├─ llm_gateway.py          │
│                  └─ (openai client)         │
│                                             │
│  logger.py                                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         Application Layer                   │
├─────────────────────────────────────────────┤
│  main.py ──┐                                │
│  main_llm.py ├─ [all core + llm modules]    │
│  batch.py ─┤                                │
│  compare.py┤                                │
│            └─ logger.py, plot.py            │
│                                             │
│  plot.py, batch_plot.py, comparison_plot.py│
│  └─ matplotlib, CSV readers                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         Test Layer                          │
├────────────────────��────────────────────────┤
│  test_core.py ──→ [all core modules]        │
└─────────────────────────────────────────────┘
```

---

## Architecture Notes

### FACT
- 7 core simulation modules are stable and interdependent
- 2 LLM integration modules provide abstraction over Groq/OpenAI
- 7 application entry points test different simulation modes
- Tests validate core module behavior end-to-end
- Dependency flow is: core → llm → apps
- All modules are located in repository root

### INFERENCE
- Code is research-quality: well-structured, type-hinted, purposeful
- The simulation framework is reusable and could support future derivatives (Ω-MED, Ω-DEGRADE, etc.)
- LLM integration is abstracted well enough for multi-provider support
- Batch/comparison logic suggests iterative research cycles

### HYPOTHESIS
- Generated CSV/PNG files are retained for documentation/comparison purposes
- The repository expects to be extended with new simulation modes or agent types
- Performance profiling and cost tracking for LLM calls is an emerging concern (per llm_gateway.ask stats)

### UNKNOWN
- What is the production use case? (research artifact, ongoing study, teaching tool?)
- Should generated simulation results be versioned or excluded from source control?
- Are there database seeding/integration requirements with Omega-Residency or other projects?

---

## Health Indicators

✅ **Strengths**
- Clear module separation: core/llm/app layers
- Comprehensive test coverage for core modules
- Well-documented README with usage examples
- Active development: recent commits
- Type hints in place

⚠️ **Concerns**
- No pyproject.toml or setup.py → packaging/installation not formalized
- Generated artifacts (CSV, PNG) in source control → size bloat potential
- No CI/CD workflows yet (despite .github/ directory)
- No data schema documentation for CSV outputs
- Import structure assumes files run from root (may break with packaging)

🔧 **Recommended Actions**
1. Move generated artifacts to `archive/generated-artifacts/`
2. Create `packages/omega-core/` to formalize the simulation engine
3. Add pyproject.toml with proper package metadata
4. Document Ω-META interoperability rules
5. Create `.github/workflows/ci.yml` for test automation
6. Formalize CSV output schemas under `schemas/`

---

## Next Steps

See `REPOSITORY_MAP.md` for the proposed target structure and migration plan.
