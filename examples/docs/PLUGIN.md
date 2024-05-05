## **Plugin Configuration Guide: "plugin_example"**

### **Overview**
This guide provides detailed instructions on configuring `plugin_example`, a plugin tailored for specific computational tasks within the `xnippy` software package. Here, you will find essential information on dependencies, source files, and execution specifics necessary for proper setup and integration.

### **Plugin Details**

**`manifest.yaml` Configuration:**
```yaml
package: xnippy>=0.1.0
plugin:
  name: plugin_example
  version: 0.1.0
  description: "This plugin function calculates (a+b)+(a*b)."

meta:
  authors:
    - name: Xoani
      email: xoani@xoani.org

source:
  include:
    - utils.py
  entry_point: plugin_example.py:example_func

dependencies:
  module:
    - numpy
  plugin:
    - plugin_template==0.1.0
```

### **Explanation of Configuration Elements**

- **`package`**: Specifies `xnippy` as the required software package and the minimum compatible version (0.1.0).

- **`plugin`**:
  - **`name`**: The identifier for the plugin, `plugin_example`.
  - **`version`**: The current version of the plugin, 0.1.0.
  - **`description`**: A concise description of the plugin’s functionality, specifically highlighting its ability to perform the operation `(a+b)+(a*b)`.

- **`meta`**:
  - **`authors`**: Lists the contact information for the plugin’s author(s) to facilitate communication and collaboration.

- **`source`**:
  - **`include`**: Specifies auxiliary files required by the plugin.
  - **`entry_point`**: Designates `plugin_example.py:example_func` as the primary function or class to be executed. This must be the last entry to ensure all dependencies are loaded beforehand.

- **`dependencies`**:
  - **`module`**: External Python modules that the plugin depends on, such as `numpy`.
  - **`plugin`**: Other plugins required for this plugin’s operation, specified with exact versions for compatibility (e.g., `plugin_template==0.1.0`).

### **Usage Guidelines**

To ensure the plugin operates effectively, adhere to the following steps during installation and execution:
1. Confirm that all module dependencies, especially `numpy`, are correctly installed.
2. Check that any required plugins, like `plugin_template`, are both installed and configured properly.
3. Sequentially load all specified source files, with `plugin_example.py:example_func` loaded last to guarantee all necessary utilities and dependencies are available for execution.

### **Additional Notes**
- It is imperative to maintain the specified order in the `source` section to ensure the functionality of the `entry_point` relies on all previously loaded utilities and dependencies.
