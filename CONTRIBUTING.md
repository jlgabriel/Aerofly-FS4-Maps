# Contributing to Aerofly FS4 Maps

Thank you for your interest in contributing to Aerofly FS4 Maps! This document provides guidelines for contributing to the project.

## 🌟 How to Contribute

There are many ways to contribute to this project:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code fixes
- ✨ Implement new features

## 📋 Contribution Process

### 1. Fork and Clone

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/Aerofly-FS4-Maps.git
   cd Aerofly-FS4-Maps
   ```

### 2. Create a Branch

Create a branch for your contribution:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-name
```

### 3. Make Your Changes

- Write clean and well-documented code
- Follow Python style conventions (PEP 8)
- Add comments where necessary
- Update documentation if relevant

### 4. Commits

Use descriptive commit messages:

```bash
git commit -m "Add: New auto-zoom functionality"
git commit -m "Fix: Correction in heading calculation"
git commit -m "Docs: Update README with new instructions"
```

Recommended prefixes:
- `Add:` - New functionality
- `Fix:` - Bug fix
- `Update:` - Update existing code
- `Docs:` - Documentation changes
- `Refactor:` - Code refactoring
- `Test:` - Add or modify tests
- `Style:` - Formatting changes

### 5. Push and Pull Request

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub
3. Clearly describe the changes made
4. Reference any related issues

## 🐛 Reporting Bugs

If you find a bug, please open an issue with:

- **Descriptive title**
- **Problem description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **System information**:
  - Operating system
  - Python version
  - Aerofly FS4 version
- **Screenshots** (if applicable)
- **Logs or error messages**

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Observe the error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**System Information:**
 - OS: [e.g. Windows 10, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Aerofly FS4 Version: [e.g. 1.0.0.0]
```

## 💡 Suggesting Features

To suggest new features, open an issue with:

- **Clear title**
- **Detailed description** of the feature
- **Use case**: Why is this feature useful?
- **Mockups or examples** (if applicable)

## 🔧 Style Guide

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Variable and function names in `snake_case`
- Class names in `PascalCase`
- Constants in `UPPER_CASE`
- Add docstrings to classes and functions

Example:

```python
class MyClass:
    """Brief description of the class.

    More detailed description if needed.
    """

    def my_method(self, param: str) -> int:
        """Brief description of the method.

        Args:
            param: Description of the parameter

        Returns:
            Description of the return value
        """
        pass
```

### Type Hints

Use type hints when possible:

```python
from typing import Optional, Dict, List

def process_data(data: List[str]) -> Dict[str, int]:
    """Process the data and return a dictionary."""
    pass
```

### Comments

- Write clear and concise comments
- Explain the "why", not the "what"
- Keep comments up to date

## 🧪 Testing

If you add new functionality:

- Consider adding tests
- Ensure existing code doesn't break
- Test with different configurations

## 📝 Documentation

If you modify functionality:

- Update README.md
- Update code comments
- Update docstrings

## 🤝 Code of Conduct

### Our Commitment

We are committed to making participation in our project a harassment-free experience for everyone.

### Our Standards

**Acceptable behavior:**
- Use welcoming and inclusive language
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the community

**Unacceptable behavior:**
- Sexualized language or imagery
- Trolling, insulting comments
- Public or private harassment
- Publishing others' private information

## ❓ Questions

If you have questions about contributing, you can:

- Open an issue with the "question" label
- Contact the project maintainer

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## 🙏 Acknowledgments

All contributors will be recognized in the project. Thank you for your contribution!

---

**Happy coding! ✈️**
