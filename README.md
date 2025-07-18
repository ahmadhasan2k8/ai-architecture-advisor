# Design Patterns Tutorial 🎨

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable/)
[![CI/CD](https://github.com/yourusername/design-patterns-tutorial/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/design-patterns-tutorial/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)](https://github.com/yourusername/design-patterns-tutorial/actions)

A comprehensive, interactive tutorial on design patterns using Python. This repository contains Jupyter notebooks that explain 10 essential design patterns with real-world examples and production-ready implementations.

## 📚 Table of Contents

- [Overview](#overview)
- [Design Patterns Covered](#design-patterns-covered)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation Options](#installation-options)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Installation](#option-2-local-installation)
  - [Option 3: Poetry](#option-3-poetry)
- [Usage](#usage)
- [Testing & Validation](#testing--validation)
- [Project Structure](#project-structure)
- [Learning Path](#learning-path)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Design patterns are proven solutions to common programming problems. This tutorial provides:

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

## ⚡ Quick Start

**Using Docker (Recommended):**

```bash
# Clone and start in one command
git clone https://github.com/yourusername/design-patterns-tutorial.git
cd design-patterns-tutorial
docker compose up --build

# Access Jupyter at: http://localhost:8888/tree?token=design-patterns-2025
```

**Using Local Python:**

```bash
# Clone the repository
git clone https://github.com/yourusername/design-patterns-tutorial.git
cd design-patterns-tutorial

# Install and run
pip install -r requirements.txt
jupyter lab notebooks/
```

## 🚀 Installation Options

### Option 1: Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/design-patterns-tutorial.git
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
git clone https://github.com/yourusername/design-patterns-tutorial.git
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
git clone https://github.com/yourusername/design-patterns-tutorial.git
cd design-patterns-tutorial

# Install dependencies
poetry install

# Install with dev dependencies
poetry install --with dev

# Start Jupyter Lab
poetry run jupyter lab
```

## 📖 Usage

### 1. Interactive Learning

1. **Start Jupyter** using one of the installation methods above
2. **Navigate** to the `notebooks` directory
3. **Open** any pattern notebook (they're numbered in suggested order)
4. **Run** the cells interactively and experiment with the code

### 2. Using Pattern Implementations

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

### 3. Running Individual Notebooks

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
├── data/                       # Sample data files
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker image definition
├── pyproject.toml             # Project configuration
├── requirements.txt           # Core dependencies
├── requirements-dev.txt       # Development dependencies
├── validate.py                # Validation script
├── CLAUDE.md                  # AI assistant guidelines
└── README.md                  # This file
```

## 🎓 Learning Path

### Beginner Path (Start Here)
1. **🔐 Singleton Pattern** - Understanding single instances
2. **🏭 Factory Pattern** - Basic object creation
3. **🎯 Strategy Pattern** - Simple behavior switching

### Intermediate Path
4. **👁️ Observer Pattern** - Event-driven programming
5. **🎨 Decorator Pattern** - Extending functionality
6. **🔌 Adapter Pattern** - Interface compatibility

### Advanced Path
7. **🎮 Command Pattern** - Complex operations
8. **🎰 State Pattern** - State machines
9. **🏗️ Builder Pattern** - Complex construction
10. **📚 Repository Pattern** - Data layer abstraction

### Learning Tips

- **Start with notebooks**: Each pattern has a dedicated Jupyter notebook
- **Run the code**: All examples are executable and interactive
- **Read the tests**: Test files show comprehensive usage examples
- **Experiment**: Modify examples to see how patterns work
- **Apply patterns**: Try implementing patterns in your own projects

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

- **10 Design Patterns** with comprehensive implementations
- **10 Interactive Notebooks** with real-world examples
- **10 Test Suites** with >90% code coverage
- **1,000+ Lines** of production-ready Python code
- **Docker Support** for easy deployment
- **CI/CD Pipeline** for automated testing
- **Full Documentation** with examples and best practices

---

**Happy Learning! 🚀 If you find this tutorial helpful, please give it a ⭐️**

**Ready to start?** Choose your preferred installation method above and dive into the world of design patterns!