# Contributing to Omega-Protocol

## Code of Conduct

All contributors must follow the [Contributor Covenant](https://www.contributor-covenant.org/).

Be respectful, inclusive, and professional.

---

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/your-username/Omega-protocol.git
cd Omega-protocol
git remote add upstream https://github.com/yasindolat20-collab/Omega-protocol.git
```

### 2. Create Feature Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-doc-improvement
```

Branch naming convention:
- `feat/` — New feature
- `fix/` — Bug fix
- `docs/` — Documentation
- `refactor/` — Code refactoring
- `test/` — Testing improvements
- `chore/` — Maintenance (dependencies, cleanup)

### 3. Create Virtual Environment & Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # (testing, linting)
```

### 4. Make Changes

See `BUILD_INSTRUCTIONS.md` for development workflow.

---

## Code Quality Standards

### 1. Type Hints

All functions must have type hints:

```python
# ❌ Bad
def decide(state, actions):
    return action

# ✅ Good
def decide(self, state: Dict[str, float], actions: List[str]) -> str:
    """Determine agent's next action based on state."""
    return actions[0]
```

### 2. Docstrings

All public functions/classes must have docstrings (Google style):

```python
class Agent:
    """Autonomous agent with archetype and decision logic.
    
    Args:
        agent_id (int): Unique identifier
        use_llm (bool): Whether to use LLM for decisions
    
    Raises:
        ValueError: If agent_id is negative
    """
    
    def decide(self, state: State) -> Action:
        """Determine the agent's next action.
        
        Args:
            state: Current environment state
        
        Returns:
            The action to take (Loyalty, Exit, Voice, or Rebellion)
        
        Raises:
            RuntimeError: If LLM provider is unavailable
        """
```

### 3. Testing

All new code must include tests (≥90% coverage):

```python
# tests/test_agent.py
def test_agent_initialization():
    """Test that Agent initializes with correct defaults."""
    agent = Agent(agent_id=1)
    assert agent.id == 1
    assert agent.archetype in ARCHETYPES.keys()
    assert 0.0 <= agent.risk_aversion <= 1.0

def test_agent_decide():
    """Test that Agent.decide returns valid action."""
    agent = Agent(agent_id=1)
    state = {"economy": 0.5, "legitimacy": 0.5}
    action = agent.decide(state)
    assert action in agent.allowed_actions
```

Run tests before committing:

```bash
pytest tests/ -v
pytest tests/ --cov=packages/ --cov-report=term
```

### 4. Linting & Formatting

Code must pass linting checks:

```bash
# Auto-format
black packages/ apps/ tests/

# Lint
pylint packages/ apps/ tests/
flake8 packages/ apps/ tests/

# Type checking
mypy packages/ apps/ tests/
```

Or use a Git hook to auto-run before commit:

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
black --check packages/ apps/ tests/
flake8 packages/ apps/ tests/
pytest tests/ -q
```

### 5. Commit Messages

Use clear, descriptive commit messages:

```
# ❌ Bad
fixed stuff
updated code
wip

# ✅ Good
feat(agent): Add configurable risk aversion threshold
fix(environment): Clamp treasury value correctly in step()
docs(readme): Update installation instructions for Python 3.11
test(llm): Add mock provider for offline testing
refactor(leader): Extract surveillance logic into separate method
```

Format: `type(scope): message`

Types:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `test` — Tests
- `refactor` — Code refactoring
- `perf` — Performance improvement
- `chore` — Maintenance

---

## Documentation Requirements

Every PR must include:

### 1. README/Docstring Updates

If you:
- Add a new module → Update `packages/omega-core/README.md` or `packages/omega-llm/README.md`
- Add a new app → Update `apps/README.md` and create usage example
- Change an API → Update affected docstrings

### 2. Architecture Decision Record (ADR)

For any design decision affecting multiple modules, create an ADR:

```bash
# Create docs/decisions/ADR-NNNN-short-title.md
```

Template:

```markdown
# ADR-NNNN: Short Title

## Status
Proposed / Accepted / Deprecated

## Context
Why are we making this decision?

## Decision
What did we decide?

## Consequences
What are the positive and negative implications?

## Alternatives Considered
What else did we think about?
```

### 3. Changelog Entry

Update `CHANGELOG.md` with your change:

```markdown
## [Unreleased]

### Added
- New agent archetype system with risk profiles

### Fixed
- Correct treasury clamping in environment.step()

### Changed
- LLM gateway now supports OpenAI in addition to Groq

### Removed
- Deprecated `legacy_agent.py` module
```

---

## Submitting a Pull Request

### 1. Sync with Main

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Push Your Branch

```bash
git push origin feat/your-feature
```

### 3. Create PR on GitHub

Title: `feat(scope): Description`

Description template:

```markdown
## Description
Brief summary of changes.

## Related Issues
Closes #123

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Breaking change

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] All tests pass locally
- [ ] Coverage ≥90%

## Documentation
- [ ] Updated README
- [ ] Updated docstrings
- [ ] Created/updated ADR
- [ ] Updated CHANGELOG.md

## Checklist
- [ ] Follows code style guidelines
- [ ] Passes linting (black, pylint, flake8, mypy)
- [ ] No new warnings
- [ ] Backwards compatible (or breaking change noted)

## Screenshots (if applicable)

## Additional Notes
Any additional context.
```

### 4. Address Review Comments

- Make requested changes
- Commit with `git commit --amend` (if minor)
- Push with `git push --force-with-lease` (only if using `--amend`)
- Request re-review on GitHub

### 5. Merge

Once approved and all checks pass:

- Maintainer will squash-merge to `main`
- Your branch will be automatically deleted

---

## Reporting Issues

### Bug Reports

Include:
- Python version
- OS/platform
- How to reproduce
- Expected behavior
- Actual behavior
- Error traceback
- Environment (GROQ_API_KEY set? etc.)

### Feature Requests

Include:
- Use case / motivation
- Proposed solution
- Alternatives considered
- How it fits into Ω-META

---

## Communication

- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code reviews and discussions
- **Discussions**: For design ideas and questions (if enabled)

---

## License

By contributing, you agree that your contributions are licensed under the same CC-BY-4.0 license as the project.

---

Thank you for contributing! 🙏
