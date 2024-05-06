# Xnippet - Extendable Plugin Architecture with Snippets for Python

Welcome to `xnippet`, a robust framework designed to facilitate the integration of a plugin architecture into your projects. This system allows for the dynamic enhancement and customization of applications through plugins, enhancing project sustainability without expanding the core codebase. `xnippet` is ideal for those looking to add features for specific use cases or develop community-driven extensions while maintaining backward compatibility and minimizing dependencies.

This initiative stems from the need to evolve project features without the overhead of managing growing dependencies, thereby reducing maintenance challenges and allowing developers to focus on stabilizing and enriching the main codebase.

## **Plugins**
- **Independence**: Plugins can function as standalone applications, useful for personal data analysis projects. For dynamic functionality extension, your project should specify integration specifications, which ensure seamless plugin adoption.
- **Example**: For a practical implementation, see [BrkRaw](https://github.com/brkraw/brkraw.git), which utilizes `xnippet` for enhanced plugin integration.
- **Documentation**: Learn more about setting up and configuring plugins in our [Plugin Documentation](examples/docs/PLUGIN.md).

## Features of xnippet's Plugin Architecture
- **Snippets**: Unlike traditional plugin systems that require separate package installations, `xnippet` uses snippets, allowing for instant updates and modifications without restarting Python kernels. This approach saves significant development time and simplifies testing.
- **GitHub Integration**: `xnippet` leverages GitHub as a repository server, enabling real-time updates and collaboration without the need for repackaging and redistributing through channels like PyPi. This feature ensures that new functionalities are instantly available without the need for updating the main package.
- **Simplicity**: Our plugin architecture avoids the complexities of `setup.py`, `setup.cfg`, or `pyproject.toml` files, focusing instead on straightforward GitHub-based sharing and version control.

### **Presets** -- WIP
- **Functionality**: Presets simplify configuring plugins with multiple input arguments, ensuring consistent setups and facilitating hyperparameter testing in machine learning projects.
- **Documentation**: Detailed information is available in our [Preset Documentation](examples/docs/PRESET.md).

### **Specifications (Specs)** -- WIP
- **Purpose**: Tailored for data analysis projects, specifications help define and validate data types and structures, ensuring data integrity and facilitating detailed inspections and validations similar to systems like Pydantic.
- **Documentation**: Explore our [Specification Documentation](examples/docs/SPEC.md) for more details.

### **Recipes**  -- WIP
- **Utility**: Recipes allow for the automation of data preprocessing and metadata remapping, streamlining the integration and manipulation of datasets.
- **Documentation**: Learn how to create and use recipes with our [Recipe Documentation](examples/docs/RECIPE.md).

## Getting Started
To begin integrating `xnippet` into your project, refer to our comprehensive [Project Configuration Guide](examples/docs/PROJECT_CONFIG.md).

## Documentation
For detailed documentation on each component of the `xnippet` system, please visit the following links:
- [Project Configuration](examples/docs/PROJECT_CONFIG.md)
- [Plugins](examples/docs/PLUGIN.md)
  - [Presets](examples/docs/PRESET.md)
  - [Specifications for Dataset](examples/docs/SPEC.md)
  - [Recipes for Parsing and Remapping MetaData](examples/docs/RECIPE.md)

Explore these documents to fully understand how each module can be utilized and configured to enrich your project with our versatile plugin architecture.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

## License
`xnippet` is open-source software, freely distributed under the MIT license.
