# Build Instructions

This guide covers building the Workout Tracker application into a standalone executable and running tests.

## Table of Contents

- [Running Tests](#running-tests)
- [Building Standalone Executable](#building-standalone-executable)
- [Development Setup](#development-setup)

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=workout_tracker --cov-report=html

# Run specific test file
pytest tests/test_workout_service.py

# Run with verbose output
pytest -v
```

### Test Coverage

After running with `--cov-report=html`, open `htmlcov/index.html` in your browser to view the coverage report.

### Writing New Tests

Tests are located in the `tests/` directory. Each test file corresponds to a module in the application:

- `test_workout_service.py` - Tests for workout CRUD operations
- `test_analytics_service.py` - Tests for analytics and statistics

To add a new test:

1. Create or open the appropriate test file
2. Write test functions prefixed with `test_`
3. Use pytest fixtures for database setup
4. Run `pytest` to verify

Example:
```python
def test_new_feature(setup_database):
    """Test description."""
    # Arrange
    data = prepare_test_data()

    # Act
    result = function_to_test(data)

    # Assert
    assert result == expected_value
```

## Building Standalone Executable

### Prerequisites

- Python 3.8+
- PyInstaller 5.13+
- All runtime dependencies installed

### Install Build Tools

```bash
pip install pyinstaller
```

### Build Process

#### Option 1: Using the Spec File (Recommended)

```bash
# Build using the provided spec file
pyinstaller workout_tracker.spec

# The executable will be in dist/
```

#### Option 2: Command Line

```bash
# One-file executable
pyinstaller --onefile --windowed --name=WorkoutTracker workout_tracker/main.py

# One-directory executable (faster startup)
pyinstaller --onedir --windowed --name=WorkoutTracker workout_tracker/main.py
```

### Build Options Explained

- `--onefile`: Creates a single executable file (slower startup, easier distribution)
- `--onedir`: Creates a directory with the executable and dependencies (faster startup)
- `--windowed`: No console window (GUI only)
- `--name`: Name of the executable
- `--icon`: Path to .ico file for Windows icon

### Custom Icon

To add a custom icon:

1. Create or obtain a `.ico` file
2. Update `workout_tracker.spec`:
   ```python
   icon='path/to/icon.ico'
   ```
3. Rebuild with `pyinstaller workout_tracker.spec`

### Platform-Specific Builds

#### Windows

```bash
# Build on Windows
pyinstaller workout_tracker.spec

# Output: dist/WorkoutTracker.exe
```

#### macOS

```bash
# Build on macOS
pyinstaller workout_tracker.spec

# Output: dist/WorkoutTracker.app
```

#### Linux

```bash
# Build on Linux
pyinstaller workout_tracker.spec

# Output: dist/WorkoutTracker
```

**Note**: You must build on each target platform. Cross-compilation is not supported.

### Testing the Build

```bash
# Navigate to dist directory
cd dist

# Run the executable
# Windows
./WorkoutTracker.exe

# macOS
open WorkoutTracker.app

# Linux
./WorkoutTracker
```

### Troubleshooting Builds

#### Missing Modules

If the executable fails with "ModuleNotFoundError":

1. Add the module to `hiddenimports` in `workout_tracker.spec`:
   ```python
   hiddenimports=['missing_module'],
   ```
2. Rebuild

#### File Not Found Errors

If data files are missing:

1. Add them to `datas` in `workout_tracker.spec`:
   ```python
   datas=[('path/to/file', 'destination/in/exe')],
   ```
2. Rebuild

#### Large Executable Size

To reduce size:

1. Use `--onedir` instead of `--onefile`
2. Remove unused dependencies
3. Use UPX compression (enabled by default)

## Development Setup

### Install All Dependencies

```bash
# Runtime dependencies
pip install -r workout_tracker/requirements.txt

# Development dependencies (testing, building, code quality)
pip install -r requirements-dev.txt
```

### Code Quality Tools

#### Black (Code Formatter)

```bash
# Format all Python files
black workout_tracker tests

# Check without making changes
black --check workout_tracker tests
```

#### Flake8 (Linter)

```bash
# Lint all Python files
flake8 workout_tracker tests

# Ignore specific errors
flake8 --ignore=E501,W503 workout_tracker tests
```

#### MyPy (Type Checker)

```bash
# Type check the codebase
mypy workout_tracker
```

### Git Hooks (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run tests before commit
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Continuous Integration

Example GitHub Actions workflow (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        pip install -r workout_tracker/requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: pytest --cov=workout_tracker
```

## Distribution

### Creating a Release

1. **Tag the version**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Build executables** for each platform

3. **Create release package**:
   ```bash
   # Include the executable and README
   zip WorkoutTracker-v1.0.0-Windows.zip dist/WorkoutTracker.exe README.md LICENSE
   ```

4. **Upload to GitHub Releases**

### Installation Package (Optional)

For Windows, you can create an installer using:
- **Inno Setup** (free, Windows)
- **NSIS** (free, Windows)
- **WiX Toolset** (free, Windows)

Example Inno Setup script available on request.

## Performance Optimization

### Reducing Startup Time

1. Use `--onedir` instead of `--onefile`
2. Minimize imports in `main.py`
3. Use lazy imports where possible

### Reducing Size

1. Remove unused dependencies from `requirements.txt`
2. Use `--exclude-module` for unneeded packages
3. Enable UPX compression

## Support

For build issues:
- Check the [PyInstaller documentation](https://pyinstaller.org/)
- Review `build.log` for detailed error messages
- Ensure all dependencies are correctly specified

---

**Happy building! 🛠️**
