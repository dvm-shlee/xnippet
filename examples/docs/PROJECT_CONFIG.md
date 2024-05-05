# Project Configuration for Xnippy Integration

This document provides the basic configuration needed to integrate the `xnippy` plugin architecture into your project.

## Plugin Configuration

The configuration below is essential to set up the plugin system with `xnippy`. It defines the repositories, paths, and templates necessary for plugins, presets, specs, and recipes.

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

Ensure that each path and template is correctly set up in your project's structure to fully leverage the `xnippy` plugin system.