## 4. Command Execution Sequence Diagram

This sequence diagram visualizes the flow of a command through the system, from user input to result output, illustrating the interactions between the major components.

```mermaid
sequenceDiagram
    participant User
    participant InteractiveMode
    participant PluginManager
    participant MathOperation
    participant HistoryManager

    User->>InteractiveMode: Enter command

    alt History command
        InteractiveMode->>HistoryManager: Get/clear history
        HistoryManager-->>InteractiveMode: Return history data
        InteractiveMode->>User: Display history
    else Chain command
        InteractiveMode->>InteractiveMode: Split chain by pipes
        loop For each operation in chain
            InteractiveMode->>PluginManager: Execute operation
            PluginManager->>MathOperation: Call execute method
            MathOperation-->>PluginManager: Return result
            PluginManager-->>InteractiveMode: Return result
            InteractiveMode->>User: Display intermediate result
        end
        InteractiveMode->>HistoryManager: Add chain to history
        InteractiveMode->>User: Display final result
    else Standard operation
        InteractiveMode->>PluginManager: Execute operation
        PluginManager->>MathOperation: Call execute method
        MathOperation-->>PluginManager: Return result
        PluginManager-->>InteractiveMode: Return result
        InteractiveMode->>HistoryManager: Add to history
        InteractiveMode->>User: Display result
    end
```

### Command Execution Process

#### Initial Command Entry
1. **User enters command**: The user types a command in the interactive mode.

#### History Command Flow
If the user enters a history-related command:
1. **InteractiveMode calls HistoryManager**: The interactive mode calls the appropriate method on the HistoryManager.
2. **HistoryManager returns data**: The requested history information is returned.
3. **InteractiveMode displays history**: The history information is formatted and displayed to the user.

#### Chain Command Flow
If the user enters a chain command (`chain ...`):
1. **InteractiveMode splits the chain**: The command is split into individual operations at pipe (`|`) symbols.
2. **For each operation in the chain**:
   - **InteractiveMode calls PluginManager**: The operation is executed through the PluginManager.
   - **PluginManager calls MathOperation**: The appropriate MathOperation's execute method is called.
   - **MathOperation returns result**: The mathematical operation is performed and the result returned.
   - **PluginManager returns result to InteractiveMode**: The result is passed back to the interactive mode.
   - **InteractiveMode displays intermediate result**: Each step's result is shown to the user.
3. **InteractiveMode adds chain to history**: The entire chain command and final result are added to history.
4. **InteractiveMode displays final result**: The final result of the chain is shown to the user.

#### Standard Operation Flow
If the user enters a standard operation:
1. **InteractiveMode calls PluginManager**: The operation is executed through the PluginManager.
2. **PluginManager calls MathOperation**: The appropriate MathOperation's execute method is called.
3. **MathOperation returns result**: The mathematical operation is performed and the result returned.
4. **PluginManager returns result to InteractiveMode**: The result is passed back to the interactive mode.
5. **InteractiveMode adds to history**: The command and result are added to the history.
6. **InteractiveMode displays result**: The result is shown to the user.
