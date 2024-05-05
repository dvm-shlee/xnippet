## PyTest

### 1. Fixtures for Setup and Teardown
Pytest fixtures are a powerful feature for creating reusable setup and teardown code. Fixtures can be used to manage resources like database connections or temporary files, or to create consistent test states.

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15
```

### 2. Parameterization
The parametrize decorator enables you to run a test function with different sets of data, making it easy to test multiple scenarios with the same test logic.
```python
import pytest

@pytest.mark.parametrize(
    "test_input,expected", 
    [(5, 25),(-3, 9),(2, 4)])
def test_square(test_input, expected):
    assert test_input**2 == expected
```
### 3. Mocking
Mocking is essential for isolating tests by replacing parts of your system under test with mock objects and asserting how they have been used. Pytest integrates with the unittest.mock library provided by Python’s standard library.

```python
from unittest.mock import MagicMock
import pytest

def test_function_that_calls_method():
    mock = MagicMock(return_value=42)
    assert mock() == 42
    mock.assert_called_once()
```

### 4. Exception Testing
Pytest makes it easy to assert that certain code raises an exception using the pytest.raises context manager.

```python
import pytest
def test_raises_exception():
    with pytest.raises(ValueError):
        raise ValueError("Invalid value")
```

### 5. Using Marks for Test Selection
Marks in pytest allow you to tag tests and selectively run them based on these tags. This is useful for categorizing tests (e.g., slow, integration).

```python
import pytest

@pytest.mark.slow
def test_large_file_processing():
    pass

# You can run these tests with `pytest -m slow`
```

### 6. Test Coverage
Pytest can be integrated with coverage tools to measure the coverage of your tests, ensuring that all parts of your program are tested. You can use the pytest-cov plugin for this purpose.

```bash
pytest --cov=my_package
```

### 7. Plugins
Pytest has a vast ecosystem of plugins that extend its functionality. For example, pytest-django for Django applications, pytest-asyncio for testing asyncio code, and many others that provide additional fixtures, configuration options, and hooks.

### 8. Asserting with `pytest` idioms
Although using plain assert statements is common and recommended with pytest, you can enhance assertions by providing an additional message using the built-in assert statement, which is supported in Python:

```python
def test_set_comparison():
    set_a = {1, 2, 3}
    set_b = {1, 2, 4}
    assert set_a == set_b, f"Expected {set_a} to equal {set_b}"
```


In pytest, the `addfinalizer` method is a powerful tool used within fixtures to register cleanup functions that should be executed after a fixture is no longer in use. This method is part of the fixture's request object, which provides a context for the fixture in the test framework. The `addfinalizer` method allows for more flexible and robust teardown logic compared to using the `yield` statement in fixtures.

### Key Features of `addfinalizer`

- **Multiple Finalizers**: You can add multiple finalizer functions to a single fixture. This is particularly useful when a fixture sets up multiple resources that each need their own specific cleanup logic.
- **Guaranteed Execution**: Finalizers are guaranteed to be executed even if the setup part of the fixture encounters an error. This ensures that all resources are properly cleaned up, preventing leaks or unintended side effects.
- **Error Handling**: Errors in the finalizer functions do not stop other finalizers from being executed. Each finalizer is run independently.

### When to Use `addfinalizer`

Use `addfinalizer` when:
- You need to register multiple cleanup actions that might not necessarily follow a simple LIFO (Last In, First Out) order.
- Your fixture setup logic might raise an exception, and you still need to ensure cleanup occurs.
- You want to avoid nesting too much logic between `yield` statements, keeping setup and teardown logic clearly separated.

### Example of Using `addfinalizer`

Here’s an example that demonstrates how to use `addfinalizer` within a pytest fixture:

```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_file(request):
    # Create a temporary file
    temp = tempfile.NamedTemporaryFile(delete=False)

    def cleanup_temp_file():
        print("Cleaning up the temp file.")
        os.remove(temp.name)

    # Register the cleanup function
    request.addfinalizer(cleanup_temp_file)

    return temp.name

def test_temp_file(temp_file):
    # Write something to the temp file
    with open(temp_file, 'w') as f:
        f.write('Hello, world!')

    # Read back from the file to check contents
    with open(temp_file, 'r') as f:
        content = f.read()
    assert content == 'Hello, world!'
```

In this example:
- A temporary file is created using Python's `tempfile.NamedTemporaryFile` with `delete=False` to keep the file around after the file object is closed.
- The `cleanup_temp_file` function is defined to remove the file and is registered as a finalizer. This function will be called to clean up the temporary file after the test using the fixture has completed.
- The `temp_file` fixture returns the path to the temporary file, which is then used in a test function.

### Conclusion

The `addfinalizer` method is an integral part of pytest's powerful fixture system, providing a reliable way to handle resource cleanup. It ensures that tests remain clean and independent by making sure that all resources allocated during a test are properly cleaned up afterward, even if errors occur during setup or test execution. This method enhances the robustness of test suites, especially those involving complex or multiple resource setups.