## 5. Interactive Mode State Diagram

This state diagram illustrates the different states and transitions within the interactive mode, showing how the application responds to different types of user input.

```mermaid
stateDiagram-v2
    [*] --> WaitingForCommand

    WaitingForCommand --> ProcessingHelp: help command
    ProcessingHelp --> WaitingForCommand

    WaitingForCommand --> ProcessingHistory: history command
    ProcessingHistory --> WaitingForCommand

    WaitingForCommand --> ProcessingChain: chain command
    ProcessingChain --> WaitingForCommand: success/update last_result
    ProcessingChain --> WaitingForCommand: error/restore last_result

    WaitingForCommand --> ProcessingOperation: standard operation
    ProcessingOperation --> WaitingForCommand

    WaitingForCommand --> [*]: exit/quit command

    state ProcessingChain {
        [*] --> SaveOriginalResult
        SaveOriginalResult --> ExecutingStep
        ExecutingStep --> UpdateLastResult: step succeeds
        UpdateLastResult --> NextStep
        NextStep --> ExecutingStep: more steps
        ExecutingStep --> ChainError: step fails
        NextStep --> FinalizeChain: all steps done
        ChainError --> RestoreOriginalResult
        FinalizeChain --> [*]: update session last_result
        RestoreOriginalResult --> [*]
    }
```

### Interactive Mode States

#### WaitingForCommand
The default state where the application is waiting for user input. From this state, the application can transition to:
- **ProcessingHelp**: When the user enters the "help" command
- **ProcessingHistory**: When the user enters a history-related command
- **ProcessingChain**: When the user enters a chain command
- **ProcessingOperation**: When the user enters a standard operation
- **Exit**: When the user enters "exit" or "quit"

#### ProcessingHelp
Handles the display of help information, then returns to the WaitingForCommand state.

#### ProcessingHistory
Processes history commands (view, get specific entry, clear), then returns to the WaitingForCommand state.

#### ProcessingChain
A complex state that handles chained calculations, with its own internal states:
- **SaveOriginalResult**: Stores the current last_result to enable proper error handling
- **ExecutingStep**: Executes a single step in the chain
- **UpdateLastResult**: Updates the temporary last_result with the current step's result
- **NextStep**: Prepares for the next operation in the chain
- **ChainError**: Handles errors that occur during chain execution
- **FinalizeChain**: Finalizes successful chain execution, updates session's last_result
- **RestoreOriginalResult**: Restores the original last_result if chain execution fails

The chain processing now has two distinct exit paths:
1. Success path: Finalizes the chain and updates the session's last_result
2. Error path: Restores the original last_result to maintain consistency

#### ProcessingOperation
Executes a single mathematical operation, then returns to the WaitingForCommand state.
