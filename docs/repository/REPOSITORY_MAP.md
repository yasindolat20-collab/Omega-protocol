# Omega-Protocol Repository Map

## Current State → Target State Transformation

### Target Architecture

```
omega-protocol/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              (NEW: pytest, lint, type-check)
│   │   └── test-coverage.yml   (NEW: coverage reporting)
│   └── COPILOT.md              (NEW: agent guidance)
├── README.md                    (UPDATED: new structure refs)
├── pyproject.toml               (NEW: package metadata)
├── setup.py                     (NEW: installation support)
├── requirements.txt             (CURRENT: unchanged)
├── .gitignore                   (UPDATED: add build artifacts)
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md          (NEW: Ω-META architecture)
│   │   ├── omega-meta.md        (NEW: umbrella framework)
│   │   └── module-boundaries.md (NEW: interop rules)
│   ├── decisions/
│   │   ├── ADR-0001-repository-structure.md     (NEW)
│   │   ├── ADR-0002-agent-compatibility.md      (NEW)
│   │   └── ADR-0003-uncertainty-handling.md     (NEW)
│   ├── repository/
│   │   ├── REPOSITORY_MAP.md         (THIS FILE)
│   │   ├── REPOSITORY_INVENTORY.md   (CREATED)
│   │   ├── CONTRIBUTION_GUIDE.md     (NEW)
│   │   └── VALIDATION_RULES.md       (NEW)
│   ├── research/
│   │   ├── notes/
│   │   │   └── 2026-10-05-key-findings.md (NEW)
│   │   └── bibliography.md      (NEW)
│   └── operations/
│       ├── BUILD_INSTRUCTIONS.md    (NEW)
│       ├── VALIDATION.md            (NEW)
│       └── TROUBLESHOOTING.md       (NEW)
│
├── skills/
│   └── omega-conflict-research/
│       ├── SKILL.md                 (NEW)
│       ├── README.md                (NEW)
│       ├── prompts/
│       │   ├── master-research.md   (NEW)
│       │   └── update-research.md   (NEW)
│       ├── schemas/
│       │   ├── claim-schema.md      (NEW)
│       │   ├── data-contract.md     (NEW)
│       │   └── graph-spec.md        (NEW)
│       ├── examples/
│       │   └── example-analysis.md  (NEW)
│       └── tests/
│           └── test_skill.py        (NEW)
│
├── prompts/
│   ├── simulation/
│   │   ├── agent-decision.md       (NEW)
│   │   └── leader-command.md       (NEW)
│   ├── analysis/
│   │   └── comparison-summary.md   (NEW)
│   └── README.md                   (NEW: prompt conventions)
│
├── schemas/
│   ├── environment-schema.json    (NEW)
│   ├── agent-schema.json          (NEW)
│   ├── simulation-result-schema.json (NEW)
│   ├── memory-schema.json         (NEW)
│   └── README.md                  (NEW: schema docs)
│
├── packages/
│   ├── omega-core/
│   │   ├── __init__.py             (NEW: package root)
│   │   ├── environment.py          (MOVED: src → pkg)
│   │   ├── agent.py                (MOVED: src → pkg)
│   │   ├── memory.py               (MOVED: src → pkg)
│   │   ├── shared_memory.py        (MOVED: src → pkg)
│   │   ├── leader.py               (MOVED: src → pkg)
│   │   ├── network.py              (MOVED: src → pkg)
│   │   └── py.typed                (NEW: PEP 561)
│   │
│   └── omega-llm/
│       ├── __init__.py             (NEW)
│       ├── llm_gateway.py          (MOVED: src → pkg)
│       ├── llm_client.py           (MOVED: src → pkg)
│       ├── leader_llm.py           (MOVED: src → pkg)
│       ├── prompts.py              (NEW: prompt management)
│       └── py.typed                (NEW)
│
├── apps/
│   ├── simulation/
│   │   ├── __init__.py             (NEW)
│   │   ├── main.py                 (MOVED: entry point)
│   │   ├── main_llm.py             (MOVED: entry point)
│   │   ├── batch.py                (MOVED: multi-run)
│   │   ├── compare.py              (MOVED: analysis)
│   │   └── config.py               (NEW: app config)
│   │
│   └── visualization/
│       ├── __init__.py             (NEW)
│       ├── plot.py                 (MOVED: single-run viz)
│       ├── batch_plot.py           (MOVED: aggregate viz)
│       ├── comparison_plot.py      (MOVED: comparative viz)
│       └── utils.py                (NEW: viz helpers)
│
├── research/
│   ├── datasets/
│   │   └── README.md               (NEW: data guide)
│   ├── notes/
│   │   ├── 2026-10-05-findings.md
│   │   └── research-log.md         (NEW)
│   └── experiments/
│       └── README.md               (NEW)
│
├── prototypes/
│   └── README.md                   (NEW: prototype guide)
│
├── experiments/
│   └── README.md                   (NEW: experiment guide)
│
├── scripts/
│   ├── setup.sh                    (NEW: env setup)
│   ├── validate.sh                 (NEW: validation runner)
│   ├── test.sh                     (NEW: test runner)
│   ├── build.sh                    (NEW: build script)
│   ├── export_results.py           (NEW: data export)
│   └── README.md                   (NEW: script guide)
│
├── tests/
│   ├── __init__.py                 (NEW)
│   ├── conftest.py                 (NEW: pytest config)
│   ├── test_core.py                (MOVED: core tests)
│   ├── test_environment.py         (NEW: focused tests)
│   ├── test_agent.py               (NEW: focused tests)
│   ├── test_leader.py              (NEW: focused tests)
│   ├── test_network.py             (NEW: focused tests)
│   ├── test_memory.py              (NEW: focused tests)
│   ├── test_llm_integration.py    (NEW: llm tests)
│   └── fixtures/
│       ├── __init__.py             (NEW)
│       ├── sample_data.py          (NEW)
│       └── mock_llm.py             (NEW)
│
└── archive/
    ├── generated-artifacts/
    │   ├── simulation.csv          (MOVED: generated output)
    │   ├── simulation_llm.csv      (MOVED: generated output)
    │   ├── batch_results.csv       (MOVED: generated output)
    │   ├── simulation_plot.png     (MOVED: generated asset)
    │   ├── batch_plot.png          (MOVED: generated asset)
    │   ├── comparison_plot.png     (MOVED: generated asset)
    │   └── README.md               (NEW: artifact guide)
    │
    └── provenance/
        ├── MIGRATION_LOG.md        (NEW: this restructure)
        └── FILE_MOVEMENTS.md       (NEW: tracking)
```

---

## Migration Path (Reversible)

### Phase 1: Documentation & Planning ✅ COMPLETE
- [x] Create comprehensive inventory (REPOSITORY_INVENTORY.md)
- [x] Document target architecture (this file)
- [x] Create ADRs for major decisions

### Phase 2: Package Structure (IN PROGRESS)
- [ ] Create pyproject.toml with metadata
- [ ] Create packages/omega-core/ package structure
- [ ] Create packages/omega-llm/ package structure
- [ ] Add __init__.py files and py.typed markers
- [ ] Update import statements for package-based imports

### Phase 3: App Reorganization
- [ ] Create apps/simulation/ structure
- [ ] Create apps/visualization/ structure
- [ ] Move app entry points and update imports

### Phase 4: Documentation & Guidance
- [ ] Create docs/architecture/ files
- [ ] Create docs/decisions/ ADRs
- [ ] Create docs/operations/ guides
- [ ] Update root README.md with new structure

### Phase 5: Testing & Validation
- [ ] Reorganize tests/ with focused test modules
- [ ] Create pytest fixtures and conftest.py
- [ ] Add .github/workflows/ci.yml
- [ ] Validate all imports and dependencies

### Phase 6: Final Cleanup
- [ ] Move generated artifacts to archive/
- [ ] Add .gitignore updates
- [ ] Create archive/provenance/ documentation
- [ ] Create CHANGELOG.md for v2.0 restructure

### Phase 7: PR & Review
- [ ] Create comprehensive PR with migration summary
- [ ] Link to all new documentation
- [ ] Provide rollback instructions if needed

---

## Key Principles

### 1. **Preserve Provenance**
- No files are deleted; only moved
- Generated artifacts are archived, not lost
- All movements are documented

### 2. **Reversible Changes**
- Every step can be undone
- Import compatibility layer maintained during transition
- Archive structure allows easy recovery

### 3. **Ω-META Alignment**
- Core simulation becomes a reusable skill
- LLM integration is abstracted and upgradeable
- App layer is independent of core
- Clear boundaries and contracts

### 4. **Agent/Copilot Compatibility**
- Clear directory purposes
- Consistent naming conventions
- Machine-readable schemas
- Comprehensive documentation

---

## Dependency Impact Analysis

### Current (Root-Level) Imports
```python
from agent import Agent
from environment import Environment
from llm_client import LLMClient
```

### New (Package-Based) Imports
```python
from omega_core.agent import Agent
from omega_core.environment import Environment
from omega_llm.client import LLMClient
```

### Compatibility Strategy
- Apps in `apps/` will use new package imports
- Root-level wrapper imports can be maintained for backwards compatibility
- Documentation will guide users to new import paths

---

## Validation Gates

Before each phase, validate:

1. ✅ All imports resolve correctly
2. ✅ Tests pass (pytest)
3. ✅ Type checking passes (mypy)
4. ✅ Linting passes (pylint/flake8)
5. ✅ No circular dependencies
6. ✅ No orphaned files

---

## Roll-Back Plan

If issues arise:

1. All original files are preserved in git history
2. Branch can be abandoned; main remains stable
3. Archive directory documents the intended changes
4. Each phase is independently reversible

---

## Success Criteria

✅ **Repository is mission-ready when:**
1. Package structure is formalized (pyproject.toml)
2. All imports are package-based and resolvable
3. Tests pass with >90% coverage
4. CI/CD pipeline is active (.github/workflows/)
5. Documentation covers all major components
6. Generated artifacts are archived
7. Repository can be installed via pip install -e .
8. Code is agent/Copilot-friendly (clear conventions, schemas)
9. Multi-repository Ω-META framework is documented
10. Contribution guidelines are clear and enforced

---

See `CONTRIBUTION_GUIDE.md` for how to work within this structure post-migration.
