# Design Patterns with AI-Powered Recommendations 🤖🎨

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable/)
[![Claude Code](https://img.shields.io/badge/Claude-Code%20Ready-purple.svg)](https://claude.ai/code)
[![CI/CD](https://github.com/ahmadhasan2k8/design-patterns-tutorial/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/ahmadhasan2k8/design-patterns-tutorial/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)](https://github.com/ahmadhasan2k8/design-patterns-tutorial/actions)

**The only design patterns tutorial with built-in AI pattern recommendations for your code!**

Never wonder "should I use a pattern here?" again. This repository combines comprehensive design pattern tutorials with an intelligent recommendation system that analyzes your code and suggests the right patterns at the right time.

## 🤖 AI-Powered Pattern Recommendations

**NEW**: Smart `dp::` commands that analyze your code and provide expert pattern guidance:

```bash
# Analyze your existing code for pattern opportunities
/dp::refactor /path/to/your/project/main.py

# Get expert recommendations for complex scenarios  
/dp::analyze I have 5 different payment processors with growing complexity

# Quick pattern validation
/dp::check singleton for database connection pool

# Prevent anti-patterns and overengineering
/dp::validate Making all my data models singletons for consistency
```

**🎯 Stop guessing, start knowing** - Get confident, expert-level pattern recommendations instantly.

## 📚 Table of Contents

- [🤖 AI Pattern Commands](#-ai-pattern-commands) ⭐ **NEW**
- [🚀 Quick Start with AI](#-quick-start-with-ai)
- [📖 Traditional Learning](#-traditional-learning)
- [Design Patterns Covered](#design-patterns-covered)
- [Prerequisites](#prerequisites)
- [Installation Options](#installation-options)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Installation](#option-2-local-installation)
  - [Option 3: Poetry](#option-3-poetry)
- [Testing & Validation](#testing--validation)
- [Project Structure](#project-structure)
- [Learning Path](#learning-path)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🤖 AI Pattern Commands

This repository features an intelligent pattern recommendation system using Claude Code's custom commands with **sequential thinking** for deep analysis.

### 4 Powerful Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/dp::analyze` | Deep pattern analysis with AI reasoning | `/dp::analyze Multi-format report system with growing complexity` |
| `/dp::check` | Quick pattern validation | `/dp::check strategy for 3 different sorting algorithms` |
| `/dp::refactor` | Code analysis for pattern opportunities | `/dp::refactor /path/to/your/project/` |
| `/dp::validate` | Anti-pattern detection & prevention | `/dp::validate Making User class a singleton` |

### Why This Changes Everything

❌ **Before**: "I think Factory pattern might work here... maybe?"  
✅ **After**: "Based on 8-step analysis: Strategy pattern recommended (confidence: HIGH) because you have 4+ algorithms exceeding threshold of 3..."

❌ **Before**: Hours researching if patterns apply to your situation  
✅ **After**: Instant expert analysis of your specific code and requirements

❌ **Before**: Accidentally creating anti-patterns and overengineering  
✅ **After**: AI prevents common mistakes and suggests simpler alternatives

### Prerequisites for AI Commands

The AI pattern commands require:
- **Claude Code CLI** installed ([Get it here](https://claude.ai/code))
- **Sequential thinking capability** enabled in Claude Code
- This repository cloned locally

## 🚀 Quick Start with AI

**Step 1**: Install Claude Code and clone this repo
```bash
# Install Claude Code first, then:
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial
```

**Step 2**: Navigate to this directory in Claude Code
```bash
# In Claude Code CLI:
cd /path/to/design-patterns-tutorial
```

**Step 3**: Start getting AI recommendations immediately
```bash
# Analyze your existing project
/dp::refactor /path/to/your/project/main.py

# Get recommendations for new features
/dp::analyze I need to handle 4 different authentication methods (OAuth, LDAP, local, SSO) with different validation rules

# Quick pattern checks
/dp::check observer for user activity tracking with multiple listeners

# Prevent mistakes before they happen
/dp::validate Using singleton for database connection in web app
```

**Step 4**: Follow the detailed implementation guidance provided by the AI

### Real-World AI Analysis Example

Input:
```bash
/dp::analyze Payment processing system with Credit Card, PayPal, Apple Pay, Google Pay, and Bank Transfer. Each has different validation, fees, processing times, and error handling.
```

AI Output:
```
🧠 Pattern Analysis: Multi-Provider Payment Processing System

## Problem Assessment  
- Complexity: High (5+ payment methods, different logic per method)
- Scale: 5 current providers, growth expected (crypto, BNPL)
- Growth Potential: High (fintech evolving rapidly)

## Pattern Evaluation
### Primary Recommendation: Strategy Pattern
Confidence: HIGH

Why this pattern fits:
✓ 5+ algorithms (exceeds threshold of 3)
✓ Runtime selection based on user choice/region
✓ Expected growth (new payment methods)
✓ Different validation/processing logic per provider

Implementation approach:
- Create PaymentProcessor interface  
- Implement strategy for each provider
- Use PaymentService as context
- Consider factory for processor creation

[... detailed implementation steps ...]
```

## 📖 Traditional Learning

Beyond AI recommendations, this is still the most comprehensive design patterns tutorial available:

- **Interactive Learning**: Hands-on Jupyter notebooks with runnable examples
- **Real-world Applications**: Practical use cases for each pattern  
- **Modern Python**: Using Python 3.11+ features and best practices
- **Comprehensive Coverage**: From basic to advanced patterns
- **Test-Driven**: All patterns include extensive unit tests
- **Production-Ready**: Following industry standards and conventions
- **Docker Support**: Containerized environment for easy setup
- **CI/CD Pipeline**: Automated testing and validation

## 🏗️ Design Patterns Covered

### Creational Patterns
1. **🔐 Singleton Pattern** - Ensuring a single instance
2. **🏭 Factory Pattern** - Object creation without specifying classes
3. **🏗️ Builder Pattern** - Constructing complex objects step by step

### Structural Patterns
4. **🔌 Adapter Pattern** - Making incompatible interfaces work together
5. **🎨 Decorator Pattern** - Adding functionality dynamically

### Behavioral Patterns
6. **👁️ Observer Pattern** - Event notification systems
7. **🎯 Strategy Pattern** - Interchangeable algorithms
8. **🎮 Command Pattern** - Encapsulating requests as objects
9. **🎰 State Pattern** - Object behavior based on state
10. **📚 Repository Pattern** - Data access abstraction

## 📋 Prerequisites

- Python 3.11 or higher
- Basic understanding of object-oriented programming
- Familiarity with Python classes and functions
- Docker (optional, but recommended)

## ⚡ Quick Start (Traditional Learning)

**Using Docker (Recommended):**

```bash
# Clone and start in one command
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial
docker compose up --build

# Access Jupyter at: http://localhost:8888/tree?token=design-patterns-2025
```

**Using Local Python:**

```bash
# Clone the repository
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial

# Install and run
pip install -r requirements.txt
jupyter lab notebooks/
```

> 💡 **Want AI recommendations instead?** See [🚀 Quick Start with AI](#-quick-start-with-ai) above!

## 🚀 Installation Options

### Option 1: Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Clone the repository
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial

# Build and run with Docker Compose
docker compose up --build

# Access Jupyter at http://localhost:8888/tree?token=design-patterns-2025
# Token: design-patterns-2025
```

**Docker Commands:**
```bash
# Start Jupyter service
docker compose up jupyter

# Run tests in container
docker compose --profile test up test-runner

# Stop all services
docker compose down

# Rebuild image
docker compose build --no-cache
```

### Option 2: Local Installation

If you prefer to install locally:

```bash
# Clone the repository
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# For development (includes testing and linting tools)
pip install -r requirements-dev.txt

# Start Jupyter Lab
jupyter lab
```

### Option 3: Poetry

If you use Poetry for dependency management:

```bash
# Clone the repository
git clone https://github.com/ahmadhasan2k8/design-patterns-tutorial.git
cd design-patterns-tutorial

# Install dependencies
poetry install

# Install with dev dependencies
poetry install --with dev

# Start Jupyter Lab
poetry run jupyter lab
```

## 📖 Usage

### 1. AI-Powered Pattern Recommendations (Recommended)

**For your own projects:**
```bash
# Navigate to this repo in Claude Code
cd /path/to/design-patterns-tutorial

# Analyze your code for opportunities
/dp::refactor /path/to/your/project/src/

# Get expert recommendations
/dp::analyze E-commerce system with multiple payment methods, shipping providers, and discount strategies

# Validate pattern decisions
/dp::check factory for creating different database connections

# Prevent anti-patterns
/dp::validate Making all service classes singletons for dependency injection
```

### 2. Interactive Learning (Traditional)

1. **Start Jupyter** using one of the installation methods above
2. **Navigate** to the `notebooks` directory
3. **Open** any pattern notebook (they're numbered in suggested order)
4. **Run** the cells interactively and experiment with the code

### 3. Using Pattern Implementations

```python
# Import patterns from the source code
from patterns import Singleton, ComputerBuilder, NotificationFactory

# Use Singleton pattern
class Config(Singleton):
    def __init__(self):
        super().__init__()
        self.debug = True

config1 = Config()
config2 = Config()
assert config1 is config2  # True

# Use Builder pattern
computer = (ComputerBuilder()
           .set_cpu("Intel i9")
           .set_memory("32GB")
           .set_storage("1TB SSD")
           .build())

# Use Factory pattern
notifier = NotificationFactory.create_notifier("email")
notifier.send("recipient@domain.com", "Hello World!")
```

### 4. Running Individual Notebooks

```bash
# Run specific notebook
jupyter nbconvert --to notebook --execute notebooks/01_singleton_pattern.ipynb

# Convert notebook to HTML
jupyter nbconvert --to html notebooks/01_singleton_pattern.ipynb
```

## 🧪 Testing & Validation

### Comprehensive Validation

Run the complete validation suite:

```bash
# Validate everything (notebooks, code, tests, Docker)
python validate.py

# Expected output:
# 🎉 All validations passed! The tutorial is ready to use.
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific pattern tests
pytest tests/test_patterns/test_singleton.py -v

# Run tests in Docker
docker compose --profile test up test-runner
```

### Code Quality Checks

```bash
# Format code with Black
black src tests

# Sort imports
isort src tests

# Type checking
mypy src --ignore-missing-imports

# Linting
flake8 src tests --max-line-length=88 --extend-ignore=E203,W503

# Security checks
bandit -r src

# Complexity analysis
radon cc src --total-average
```

### Notebook Validation

```bash
# Test that notebooks can be executed
pytest --nbval-lax notebooks/

# Check notebook structure
python -c "
import json
for nb in ['01_singleton_pattern.ipynb', '02_factory_pattern.ipynb']:
    with open(f'notebooks/{nb}') as f:
        data = json.load(f)
    print(f'✅ {nb}: {len(data[\"cells\"])} cells')
"
```

## 📁 Project Structure

```
design_patterns/
├── .claude/                    # 🤖 AI Pattern Commands
│   ├── commands/
│   │   └── dp/                 # Smart pattern analysis commands
│   │       ├── analyze.md      # Deep sequential thinking analysis
│   │       ├── check.md        # Quick pattern validation
│   │       ├── refactor.md     # Code analysis for opportunities
│   │       └── validate.md     # Anti-pattern detection
│   └── settings.local.json     # AI command permissions
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── notebooks/                  # Interactive Jupyter notebooks
│   ├── 01_singleton_pattern.ipynb
│   ├── 02_factory_pattern.ipynb
│   ├── 03_observer_pattern.ipynb
│   ├── 04_strategy_pattern.ipynb
│   ├── 05_decorator_pattern.ipynb
│   ├── 06_command_pattern.ipynb
│   ├── 07_repository_pattern.ipynb
│   ├── 08_builder_pattern.ipynb
│   ├── 09_adapter_pattern.ipynb
│   └── 10_state_pattern.ipynb
├── src/                        # Source code implementations
│   ├── __init__.py
│   └── patterns/
│       ├── __init__.py
│       ├── pattern_knowledge.py  # 🧠 AI knowledge base
│       ├── code_analyzer.py      # 🔍 AST-based code analysis
│       ├── repo_analyzer.py      # 📊 Repository-wide analysis
│       ├── refactoring_templates.py # 🔧 Refactoring guidance
│       ├── singleton.py
│       ├── factory.py
│       ├── observer.py
│       ├── strategy.py
│       ├── decorator.py
│       ├── command.py
│       ├── repository.py
│       ├── builder.py
│       ├── adapter.py
│       └── state.py
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_patterns/
│       ├── __init__.py
│       ├── test_singleton.py
│       ├── test_factory.py
│       ├── test_observer.py
│       ├── test_strategy.py
│       ├── test_decorator.py
│       ├── test_command.py
│       ├── test_repository.py
│       ├── test_builder.py
│       ├── test_adapter.py
│       └── test_state.py
├── docs/                       # Additional documentation
│   ├── pattern_decision_guide.md    # 🎯 Visual decision trees
│   ├── dp_commands_guide.md         # 📖 Command usage examples
│   └── extracted_pattern_knowledge.md # 📚 Raw pattern guidance
├── data/                       # Sample data files
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker image definition
├── pyproject.toml             # Project configuration
├── requirements.txt           # Core dependencies
├── requirements-dev.txt       # Development dependencies
├── validate.py                # Validation script
├── CLAUDE.md                  # AI assistant guidelines (enhanced)
└── README.md                  # This file
```

## 🎓 Learning Path

### 🤖 AI-First Approach (Recommended)
1. **Start with real problems**: Use `/dp::analyze` on your actual projects
2. **Learn by doing**: Get AI recommendations, then study the relevant notebooks
3. **Validate understanding**: Use `/dp::check` to test your pattern knowledge
4. **Prevent mistakes**: Use `/dp::validate` before implementing patterns

### 📚 Traditional Learning Path

#### Beginner Path (Start Here)
1. **🔐 Singleton Pattern** - Understanding single instances
2. **🏭 Factory Pattern** - Basic object creation
3. **🎯 Strategy Pattern** - Simple behavior switching

#### Intermediate Path
4. **👁️ Observer Pattern** - Event-driven programming
5. **🎨 Decorator Pattern** - Extending functionality
6. **🔌 Adapter Pattern** - Interface compatibility

#### Advanced Path
7. **🎮 Command Pattern** - Complex operations
8. **🎰 State Pattern** - State machines
9. **🏗️ Builder Pattern** - Complex construction
10. **📚 Repository Pattern** - Data layer abstraction

### Learning Tips

- **🤖 AI-first**: Start with AI analysis of your real code challenges
- **📖 Reference**: Use notebooks to understand implementation details
- **🧪 Practice**: Run the code - all examples are executable and interactive
- **📝 Tests**: Read test files for comprehensive usage examples
- **🔬 Experiment**: Modify examples to see how patterns work
- **🚀 Apply**: Implement AI-recommended patterns in your projects

### Which Approach Is Right for You?

**Choose AI-First if you:**
- Have existing projects that could benefit from patterns
- Want immediate, practical guidance for real problems
- Prefer learning by solving actual challenges
- Need to make pattern decisions quickly and confidently

**Choose Traditional if you:**
- Want comprehensive theoretical understanding first
- Prefer structured, linear learning progression
- Have time for systematic study
- Are building foundational knowledge

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and set up development environment
git clone https://github.com/yourusername/design-patterns-tutorial.git
cd design-patterns-tutorial

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run validation
python validate.py
```

### Development Commands

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src tests
isort src tests

# Type checking
mypy src --ignore-missing-imports

# Lint code
flake8 src tests --max-line-length=88

# Run security checks
bandit -r src

# Generate documentation
radon cc src --total-average
```

### Adding New Patterns

1. Create notebook in `notebooks/` directory
2. Implement pattern in `src/patterns/` directory
3. Add comprehensive tests in `tests/test_patterns/`
4. Update `src/patterns/__init__.py` to export new pattern
5. Run validation: `python validate.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contributing Guidelines

Please make sure to:
- **Update tests** as appropriate
- **Follow the existing code style** (run `black` and `isort`)
- **Add documentation** for new features
- **Run validation** before submitting: `python validate.py`
- **Update notebooks** if adding new patterns
- **Follow the pattern structure** established in existing implementations

### Code Standards

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all functions and methods
- Add comprehensive docstrings
- Write unit tests for all new functionality
- Maintain >90% test coverage

## 🔧 Troubleshooting

### Common Issues

**Docker issues:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild image
docker compose build --no-cache

# Check logs
docker compose logs jupyter
```

**Python issues:**
```bash
# Update pip
python -m pip install --upgrade pip

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Reinstall dependencies
pip install --force-reinstall -r requirements-dev.txt
```

**Jupyter issues:**
```bash
# Clear Jupyter cache
jupyter cache clear

# Restart Jupyter
jupyter lab --port=8888 --no-browser
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Gang of Four for the original design patterns
- Python Software Foundation for an amazing language
- Jupyter team for the interactive notebook environment
- Docker team for containerization platform
- Open source community for inspiration and tools

---

## 📊 Project Stats

### 🤖 AI-Powered Features
- **4 Smart Commands** for pattern analysis and recommendations
- **Sequential Thinking** integration for deep architectural analysis
- **Anti-Pattern Detection** to prevent common mistakes
- **8-Step Analysis Process** for complex pattern decisions
- **Real-time Code Scanning** for pattern opportunities

### 📚 Learning Resources  
- **10 Design Patterns** with comprehensive implementations
- **10 Interactive Notebooks** with real-world examples
- **10 Test Suites** with >90% code coverage
- **1,000+ Lines** of production-ready Python code
- **3 Comprehensive Guides** (decision trees, commands, extracted knowledge)
- **AST-based Code Analysis** for pattern detection

### 🛠️ Development Features
- **Docker Support** for easy deployment
- **CI/CD Pipeline** for automated testing
- **Full Documentation** with examples and best practices

---

## 🌟 What Makes This Special?

This is **the only design patterns tutorial** that:
- ✅ **Tells you WHEN to use patterns** (not just how)
- ✅ **Analyzes your actual code** for pattern opportunities  
- ✅ **Prevents anti-patterns** before you implement them
- ✅ **Uses AI reasoning** to provide expert-level recommendations
- ✅ **Works with any codebase** - not just example code

**Stop wondering if you're using patterns correctly. Start knowing.**

---

**Ready to revolutionize how you use design patterns? 🚀**

1. **For AI recommendations**: [🚀 Quick Start with AI](#-quick-start-with-ai)
2. **For traditional learning**: [⚡ Quick Start (Traditional Learning)](#-quick-start-traditional-learning)

**If this helps you write better code, please give it a ⭐️**