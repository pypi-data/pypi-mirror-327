# buildeasy: Transform Files into Python Classes

**buildeasy** is a Python package that enables users to seamlessly convert Python files into class-based instances, allowing for a more structured and object-oriented approach to module management.

## Features
- Automatically instantiates a class when defined as a subclass of `buildeasy`.
- Injects the created instance directly into `sys.modules`, effectively replacing the module.
- Supports parameterized initialization of the class.
- Exposes public methods dynamically within the module instance.
- Maintains compatibility with key module attributes.

## How It Works
By subclassing `buildeasy`, the package intercepts the class definition process, retrieves module-level attributes, and replaces the module with an instance of the class. This enables direct access to instance properties and methods at the module level.

## Example Usage
```python
# my_module.py
from buildeasy import buildeasy

class MyModule(buildeasy):
    def __init__(self, name="buildeasy"):
        self.name = name

    def greet(self):
        return f"Hello from {self.name}!"

# Usage
import my_module  # The module itself is now an instance of MyModule
print(my_module.greet())  # Outputs: "Hello from buildeasy"
print(my_module.name)  # Outputs: "buildeasy"
```

## Why Use buildeasy?
- Simplifies module-based state management.
- Encourages an object-oriented approach to organizing code.
- Eliminates the need for explicit instantiation in module scripts.

## Installation
```sh
pip install buildeasy
```

## License
This project is licensed under the MIT License.