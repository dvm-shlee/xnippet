# Project Configuration for Xnippet Integration

This document outlines the necessary steps and configurations required to integrate the `xnippet` plugin architecture into your project effectively.

## Example Directory Layout

Here is an example of how your project directory might be structured to accommodate the integration of `xnippet`:

```plaintext
project_root/
├── pyproject.toml
├── README.md
├── main_module/
│   ├── config.yaml
│   ├── __init__.py
│   └── sub_module.py
└── tests/
    └── test.py
```

## Plugin Configuration

Below is an essential configuration snippet for `config.yaml`, which sets up the plugin system with `xnippet`. It specifies the repositories, paths, and templates needed for plugins, presets, specs, and recipes.

```yaml
xnippet:
  repo:
    - name: xnippet
      url: https://github.com/xoani/xnippet.git
      plugin:
        path: example/plugin
        template:
          - plugin_template
```

### Configuration Breakdown:

- **`xnippet`**: Defines the overall container for xnippet settings.
  - **`repo`**:
    - **`name`**: Identifier for the repository, `xnippet`.
    - **`url`**: URL where the plugin repository is hosted.
    - **`plugin`**:
      - **`path`**: Directory path to the plugins within the repository.
      - **`template`**: Names of templates used for the plugin structure.

Ensure that each path and template specified matches the actual structure within your project to fully leverage the capabilities of the `xnippet` plugin system.

## Integration into Your Project

To initialize `xnippet` effectively within your project, it is crucial to set up an instance in the root `__init__.py` file. This setup ensures that `xnippet` is activated upon loading your project modules.

### Example `__init__.py` Configuration

```python
from xnippet import XnippetManager

__version__ = '0.1.0'
config = XnippetManager(package_name=__package__,
                        package_version=__version__,
                        package_file=__file__,
                        config_filename='config.yaml')

__all__ = ['__version__', 'config']
```

### Key Elements:

- **`XnippetManager`**: An instance of `Manager`, which handles the loading and management of configuration settings.
- **`__version__`**: Specifies the version of your package.
- **`config`**: Initializes the configuration manager with relevant details about the package and the location of the `config.yaml`.

This setup provides a robust foundation for integrating `xnippet` into your project, enabling the dynamic loading of plugins and their configurations, which can significantly enhance the modularity and extensibility of your application.
