# Contributing to PostgreSQL Database Manager

Thank you for your interest in contributing to PostgreSQL Database Manager! We welcome contributions from the community and are grateful for any help you can provide.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and helpful
- **Be professional** in all interactions
- **Focus on constructive feedback**
- **Respect different viewpoints** and experiences

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- PostgreSQL (for testing)
- Basic knowledge of Python and GUI development

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/postgresql-database-manager.git
   cd postgresql-database-manager
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Test the setup**
   ```bash
   python db_manager.py
   ```

## 🤝 How to Contribute

### Ways to Contribute

- 🐛 **Bug Reports**: Report bugs using GitHub Issues
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve documentation and examples
- 🔧 **Code Contributions**: Fix bugs or implement new features
- 🧪 **Testing**: Help with testing and quality assurance
- 🎨 **UI/UX**: Improve the user interface and experience

### Contribution Workflow

1. **Check existing issues** to avoid duplicates
2. **Create an issue** to discuss major changes
3. **Fork and create a branch** for your work
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request** with a clear description

## 💻 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some specific guidelines:

#### Code Formatting
```python
# Use black for automatic formatting
black db_manager.py

# Use flake8 for linting
flake8 db_manager.py
```

#### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DatabaseManager`)
- **Functions/Methods**: `snake_case` (e.g., `check_connection`)
- **Variables**: `snake_case` (e.g., `connection_string`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_PORT`)

#### Documentation
```python
def backup_database(connection_string: str, output_file: str) -> bool:
    """
    Backup a PostgreSQL database to a file.

    Args:
        connection_string (str): PostgreSQL connection string
        output_file (str): Path to output backup file

    Returns:
        bool: True if backup successful, False otherwise

    Raises:
        ConnectionError: If database connection fails
        FileNotFoundError: If output directory doesn't exist
    """
    pass
```

#### Type Hints
Use type hints for function parameters and return values:
```python
from typing import Optional, Dict, List

def get_database_info(conn_str: str) -> Optional[Dict[str, str]]:
    pass
```

### UI Guidelines

- **Consistent Spacing**: Use consistent padding and margins
- **Color Scheme**: Follow the CustomTkinter dark theme
- **Accessibility**: Ensure good contrast and readable fonts
- **Responsive Design**: UI should work on different screen sizes

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=db_manager

# Run specific test file
pytest tests/test_database.py
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies (databases, file system)

```python
def test_connection_string_validation():
    """Test that connection string validation works correctly."""
    # Test valid connection string
    assert validate_connection_string("postgresql://user:pass@host:5432/db")

    # Test invalid connection string
    assert not validate_connection_string("invalid_string")
```

### Manual Testing Checklist
- [ ] Application starts without errors
- [ ] All tabs are accessible and functional
- [ ] Database connections work correctly
- [ ] File operations work as expected
- [ ] Error messages are user-friendly
- [ ] Administrator privileges work correctly

## 📤 Pull Request Process

### Before Submitting

1. **Update documentation** if you changed functionality
2. **Add tests** for new features
3. **Run the test suite** and ensure all tests pass
4. **Check code formatting** with black and flake8
5. **Update CHANGELOG.md** with your changes

### Pull Request Template

When submitting a pull request, please include:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation review** if applicable
5. **Merge** after approval

## 🐛 Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, PostgreSQL version
- **Screenshots**: If applicable
- **Error Messages**: Full error messages or logs

### Feature Requests

When requesting features, please include:

- **Problem Statement**: What problem does this solve?
- **Proposed Solution**: How would you like this to work?
- **Alternatives**: Any alternative solutions you've considered
- **Use Cases**: Specific examples of how this would be used

## 📚 Development Resources

### Useful Links
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

### Development Tools
- **IDE**: VSCode, PyCharm, or your preferred editor
- **Database**: PostgreSQL with sample databases for testing
- **Git GUI**: GitKraken, SourceTree, or command line
- **Testing**: pytest for unit testing

## 🆘 Getting Help

If you need help with contributing:

- **GitHub Discussions**: Ask questions in our discussions
- **GitHub Issues**: Create an issue with the "question" label
- **Documentation**: Check our comprehensive documentation
- **Code Comments**: Look at inline code documentation

## 🎉 Recognition

We appreciate all contributors! Contributors will be:

- **Listed** in our README.md contributors section
- **Mentioned** in release notes for significant contributions
- **Credited** in the application's about section

Thank you for contributing to PostgreSQL Database Manager! 🚀
