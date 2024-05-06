## **Plugin Configuration Guide: "plugin_example"**

### **Overview**
This guide provides detailed instructions on configuring `plugin_example`, a specialized plugin designed for computational tasks within the `xnippet` software package. This document outlines essential information regarding dependencies, source files, and execution specifics necessary for proper integration and operation.

### **Plugin Structure**

**Directory Layout:**
```plaintext
plugin_root/
├── manifest.yaml
├── plugin_example.py
├── utils.py
├── preset/
│   └── preset1.yaml
├── recipe/
│   └── recipe1.yaml
└── spec/
    └── spec.yaml
```

**`manifest.yaml` Configuration:**
```yaml
package: xnippet>=0.1.0
plugin:
  name: plugin_example
  version: 0.1.0
  description: "This plugin function calculates (a+b)+(a*b) and returns result in numpy array."

meta:
  authors:
    - name: Xoani
      email: xoani@xoani.org
  license: MIT
  documentation: "README.md"
  citation: "CITATION.cff"

source:
  include:
    - utils.py
  entry_point: plugin_example.py:example_func

dependencies:
  - numpy

features:
  preset:
    path: preset
  recipe:
    path: recipe
  spec:
    path: spec
```

### **Explanation of Configuration Elements**

- **`package`**: Specifies `xnippet` as the required framework with a minimum version of 0.1.0 for compatibility.

- **`plugin`**:
  - **`name`**: Identifier for the plugin, `plugin_example`.
  - **`version`**: Specifies the version of the plugin, 0.1.0.
  - **`description`**: Provides a concise description of the plugin's core functionality.

- **`meta`**:
  - **`authors`**: Lists the plugin’s authors along with their contact information to facilitate communication and collaboration.
  - **`license`**: Specifies the type of license under which the plugin is distributed.
  - **`documentation`**: References the main documentation file.
  - **`citation`**: Indicates the location of the citation file if applicable.

- **`source`**:
  - **`include`**: Names auxiliary files required for the plugin's functionality.
  - **`entry_point`**: Designates `plugin_example.py:example_func` as the primary function or class for execution, ensuring it is loaded last for proper initialization.

- **`dependencies`**: External Python modules that the plugin depends on, such as `numpy`.

### **Usage Guidelines**

To ensure the plugin operates effectively, adhere to the following steps during installation and execution:
1. **Install Dependencies**: Confirm that all required modules, especially `numpy`, are installed.
2. **Verify Plugin Dependencies**: Ensure that any necessary plugins, like `plugin_template`, are both installed and properly configured.
3. **Sequential Source Loading**: Load all specified source files in the order listed, ensuring `plugin_example.py:example_func` is loaded last.

### **Additional Notes**
- Maintaining the specified order in the `source` section is critical to ensure that the functionality of the `entry_point` depends on all previously loaded utilities and dependencies.
