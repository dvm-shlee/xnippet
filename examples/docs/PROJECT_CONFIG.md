# Project Configuration for Xnippy Integration

This document outlines the necessary steps and configurations required to integrate the `xnippy` plugin architecture into your project effectively.

## Example Directory Layout

Here is an example of how your project directory might be structured to accommodate the integration of `xnippy`:

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

Below is an essential configuration snippet for `config.yaml`, which sets up the plugin system with `xnippy`. It specifies the repositories, paths, and templates needed for plugins, presets, specs, and recipes.

```yaml
plugin:
  repo:
    - name: xnippy
      url: https://github.com/xoani/xnippy.git
      plugin:
        path: example/plugin
        template:
          - plugin_template
```

### Configuration Breakdown:

- **`plugin`**: Defines the overall container for plugin settings.
  - **`repo`**:
    - **`name`**: Identifier for the repository, `xnippy`.
    - **`url`**: URL where the plugin repository is hosted.
    - **`plugin`**:
      - **`path`**: Directory path to the plugins within the repository.
      - **`template`**: Names of templates used for the plugin structure.

Ensure that each path and template specified matches the actual structure within your project to fully leverage the capabilities of the `xnippy` plugin system.

## Integration into Your Project

To initialize `xnippy` effectively within your project, it is crucial to set up an instance in the root `__init__.py` file. This setup ensures that `xnippy` is activated upon loading your project modules.

### Example `__init__.py` Configuration

```python
from xnippy import Xnippy as ConfigManager

__version__ = '0.1.0'
config = ConfigManager(package_name=__package__,
                       package_version=__version__,
                       package_file=__file__,
                       config_filename='config.yaml')

__all__ = ['__version__', 'config']
```

### Key Elements:

- **`ConfigManager`**: An instance of `Xnippy`, which handles the loading and management of configuration settings.
- **`__version__`**: Specifies the version of your package.
- **`config`**: Initializes the configuration manager with relevant details about the package and the location of the `config.yaml`.

This setup provides a robust foundation for integrating `xnippy` into your project, enabling the dynamic loading of plugins and their configurations, which can significantly enhance the modularity and extensibility of your application.
