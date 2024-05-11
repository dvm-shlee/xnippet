# Xnippet - Extendable Plugin Architecture with Snippets for Python

**Xnippet** is a standalone module designed to enhance the extensibility of Python-based projects, particularly in data analysis. Its key features include:

- **Extensibility**: Functions as a new type of package manager that uses your GitHub repository for code version control, allowing the addition of features without modifying the existing codebase or increasing dependencies.
- **Standardized Configuration**: Facilitates consistent settings across various environments and projects. Configurations and snippets can be inherited by subdirectories, maintaining uniformity across projects within the same directory. This feature is inspired by tools like pyenv.
- **Sharing Code Snippets**: Enables a live searchable interface for code snippets stored in specified GitHub repositories. This feature supports the importing and direct use of snippets without local installation, enhancing online plugin functionality.
- **Dependencies Control**: Manages dependencies on a per-snippet basis, checking and resolving dependencies during download or online import. This includes resolving Python dependencies via PyPI, managing snippet dependencies within your repository, and verifying the availability of external executables.

## **Types of Snippets**
### Simple Snippets:

- Python code that can be seamlessly imported and used within any module without specific entry-points.

### **Plugin Snippets**:

- Builds on Simple Snippets by adding entry-points to serve specific roles, ideal for developing Python packages with a straightforward plugin architecture.
- Employs YAML for manifest packaging, with each snippet consisting of a single Python file and an accompanying manifest.
## Getting Started
To begin integrating `xnippet` into your project, refer to our comprehensive [Project Configuration Guide](examples/docs/PROJECT_CONFIG.md).

## Documentation
For detailed documentation on each component of the `xnippet` system, please visit the following links:
- [Project Configuration](examples/docs/PROJECT_CONFIG.md)
- [Plugins](examples/docs/PLUGIN.md)
  - [Presets](examples/docs/PRESET.md)
  - [Data Schema](examples/docs/SCHEMA.md)
  - [Recipes for Parsing and Remapping MetaData](examples/docs/RECIPE.md)

Explore these documents to fully understand how each module can be utilized and configured to enrich your project with our versatile plugin architecture.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

## License
`xnippet` is open-source software, freely distributed under the MIT license.
