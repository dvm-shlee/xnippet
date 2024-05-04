# Xnippy

**Status: 🚧 Work in Progress 🚧**
This project is currently under development. Features and documentation may be incomplete or subject to change.

Xnippy is a standalone module developed as an extension of BrkRaw. It enhances the extensibility of Python-based projects through several key features:

- **Standardized Configuration**: Streamlines project settings to facilitate uniformity across environments.
- **Sharing Code Snippets**: Allows for the live sharing and importing of code snippets via a GitHub repository. These snippets can be utilized directly without the need for local installation, thus simplifying code usage and integration.

## **Types of Snippets**

### **Plugin Snippets**:

- Designed to enhance Python applications by adding new features without modifying the existing codebase or increasing dependencies.
- These snippets are capable of searching and importing functions or classes for immediate use, either from online sources or local storage (available globally or per project).
- Utilizes YAML for manifest packaging, with each snippet consisting of a single Python file and an accompanying manifest.

### **Preset Snippets**:

- Small YAML documents that serve as preset configurations for plugins or applications, streamlining the setup process.

### **Spec Snippets:**

- YAML files that define data specifications in a datasheet format, complete with regex-aware type restrictions for each field.
- Particularly useful for managing dataframes with customizable field types, providing robust parsing and inspection capabilities.

### Recipe snippets

- YAML-based snippets for parsing metadata from metadata storing pyrhon object, allowing for flexible data parsing routes.
- Supports the definition of conditional parsing paths, temporary variables, and pre-processing scripts within the data parsing workflow.
- All operations are Python-based, with an option to execute inline startup scripts to handle any necessary dependencies.
