## 6. User Interaction Diagram

This diagram provides an overview of the different ways users can interact with the Math CLI application, showing the main features and how they lead to calculation results.

```mermaid
graph LR
    User --> A[Basic CLI Mode]
    User --> B[Interactive Mode]
    User --> C[Plugin Management]

    A --> A1[Single Operations]
    A --> A2[Help & Documentation]

    B --> B1[Standard Operations]
    B --> B2[History Management]
    B --> B3[Previous Result Reference]
    B --> B4[Chained Calculations]

    C --> C1[Use Built-in Plugins]
    C --> C2[Add Custom Plugins]
    C --> C3[Create New Plugins]

    B1 --> D[Result]
    B2 --> D
    B3 --> D
    B4 --> D
    A1 --> D

    style D fill:#8fd,stroke:#6c8
```

### User Interaction Paths

#### Basic CLI Mode
For simple, one-off calculations:
- **Single Operations**: Execute a single mathematical operation directly from the command line
- **Help & Documentation**: Access information about available operations and usage

#### Interactive Mode
For performing multiple calculations in succession:
- **Standard Operations**: Execute single operations one after another
- **History Management**: View, recall, and manage calculation history
- **Previous Result Reference**: Reference previous calculation results using `$` or `ans`
- **Chained Calculations**: Perform multiple operations in sequence with automatic result passing

#### Plugin Management
For extending the application's functionality:
- **Use Built-in Plugins**: Utilize the standard mathematical operations
- **Add Custom Plugins**: Add existing plugins from external sources
- **Create New Plugins**: Develop custom mathematical operations

All these interaction paths eventually lead to calculation results, which are the primary output of the application.
