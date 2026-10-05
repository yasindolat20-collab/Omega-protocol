# Build Instructions for Omega-Protocol

## Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version
- **git**: For version control
- **Virtual Environment**: Recommended (venv or conda)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yasindolat20-collab/Omega-protocol.git
cd Omega-protocol
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .  # Install package in development mode (once pyproject.toml is ready)
```

### 4. Verify Installation

```bash
python -m pytest tests/ -v
python -c "from omega_core.agent import Agent; print('✅ Import successful')"
```

---

## Development Workflow

### Running Simulations

#### Rule-Based Simulation (Baseline)

```bash
cd apps/simulation
python main.py
```

**Output**: Prints to console, saves to `simulation.csv`

#### LLM-Driven Simulation

```bash
export GROQ_API_KEY="your-key-here"  # or OPENAI_API_KEY for OpenAI
python main_llm.py
```

**Output**: Prints to console, saves to `simulation_llm.csv`

#### Batch Run (20 Seeds, Monte Carlo)

```bash
python batch.py
```

**Output**: Aggregated statistics in `batch_results.csv`

### Visualization

#### Single-Run Plot

```bash
python -m apps.visualization.plot
# Output: simulation_plot.png
```

#### Batch Aggregation Chart

```bash
python -m apps.visualization.batch_plot
# Output: batch_plot.png
```

#### Comparison (Rule-Based vs LLM)

```bash
python -m apps.simulation.compare
python -m apps.visualization.comparison_plot
# Outputs: comparison_plot.png, comparison report
```

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Module

```bash
pytest tests/test_environment.py -v
pytest tests/test_agent.py -v
pytest tests/test_llm_integration.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=packages/omega_core --cov=packages/omega_llm --cov-report=html
# Open htmlcov/index.html to view coverage
```

### Run Linting & Type Checking

```bash
# Lint
pylint packages/ apps/ tests/
flake8 packages/ apps/ tests/

# Type checking
mypy packages/ apps/ tests/
```

---

## Environment Configuration

### LLM Provider Setup

#### Groq (Recommended for Development)

```bash
export GROQ_API_KEY="gsk_..."
```

Get your key: https://console.groq.com/keys

#### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

Get your key: https://platform.openai.com/account/api-keys

#### Environment File (.env)

Create `.env` in the project root:

```env
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk_...
SIMULATION_SEED=42
LOG_LEVEL=INFO
```

Load via Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
```

---

## Docker Support (Optional)

### Build Docker Image

```bash
docker build -t omega-protocol:latest .
```

### Run in Docker

```bash
docker run -e GROQ_API_KEY="gsk_..." \
  -v $(pwd)/results:/app/results \
  omega-protocol:latest \
  python -m apps.simulation.main
```

### Docker Compose (Multiple Services)

```bash
docker-compose up -d  # Start services
docker-compose logs -f  # View logs
docker-compose down  # Stop services
```

---

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'omega_core'`

**Solution**:
1. Ensure virtual environment is activated
2. Run `pip install -e .` from project root
3. Check `pyproject.toml` has `packages` defined

### LLM API Errors

**Problem**: `GROQ_API_KEY not found` or `AuthenticationError`

**Solution**:
1. Verify API key is set: `echo $GROQ_API_KEY`
2. Check key format (should start with `gsk_`)
3. Ensure key is not expired in Groq console
4. Try fallback to rule-based mode: `python main.py`

### Missing Dependencies

**Problem**: `ImportError: No module named 'rich'` or similar

**Solution**:
```bash
pip install -r requirements.txt
# or install individual package
pip install rich matplotlib numpy
```

### Test Failures

**Problem**: Tests fail with `AssertionError` or `TypeError`

**Solution**:
1. Run tests with verbose output: `pytest -vvv`
2. Run single failing test: `pytest tests/test_x.py::test_func -vvv`
3. Check Python version: `python --version` (must be ≥3.10)
4. Reinstall packages: `pip install -r requirements.txt --force-reinstall`

---

## Continuous Integration (GitHub Actions)

### Automated Workflows

On each push to `main`:
1. **pytest**: Run all tests
2. **Coverage**: Generate coverage report
3. **Lint**: Check code quality (pylint, flake8)
4. **Type Check**: Validate types (mypy)

View status: GitHub Actions tab in repository

---

## Performance Profiling

### Profile a Simulation Run

```python
import cProfile
import pstats

from apps.simulation.main import main

profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions by cumulative time
```

### Memory Profiling

```bash
pip install memory-profiler
python -m memory_profiler -m apps.simulation.main
```

---

## Production Deployment

### Package Distribution

```bash
# Build distribution
python -m build

# Install from distribution
pip install dist/omega_protocol-1.0.0-py3-none-any.whl
```

### Publishing to PyPI

```bash
pip install twine
twine upload dist/*
```

---

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from omega_core.agent import Agent
# Now Agent operations will print debug info
```

### Debug with IDE

**VS Code**:

Add `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/apps/simulation/main.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

Then press F5 to start debugging.

---

For further assistance, see `TROUBLESHOOTING.md` or open an issue on GitHub.
