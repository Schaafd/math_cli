//
//  main.swift
//  MathCLI Command-Line Tool
//
//  A simple command-line interface for testing MathCLI operations
//  Run with: swift run mathcli-tool
//

import Foundation
#if canImport(MathCLICore)
import MathCLICore
#endif

// ANSI color codes for terminal output
struct Colors {
    static let reset = "\u{001B}[0m"
    static let red = "\u{001B}[31m"
    static let green = "\u{001B}[32m"
    static let yellow = "\u{001B}[33m"
    static let blue = "\u{001B}[34m"
    static let magenta = "\u{001B}[35m"
    static let cyan = "\u{001B}[36m"
}

// Print welcome banner
func printWelcome() {
    print("\(Colors.cyan)")
    print("╔════════════════════════════════════════╗")
    print("║        MathCLI Command-Line Tool      ║")
    print("║         iOS Operations Tester         ║")
    print("╚════════════════════════════════════════╝")
    print(Colors.reset)
    print("\(Colors.yellow)Type 'help' for commands, 'quit' to exit\(Colors.reset)")
    print()
}

// Print help
func printHelp() {
    print("\(Colors.green)Available Commands:\(Colors.reset)")
    print("  help              - Show this help")
    print("  list              - List all operations")
    print("  categories        - Show operation categories")
    print("  search <query>    - Search for operations")
    print("  vars              - Show variables")
    print("  funcs             - Show user-defined functions")
    print("  clear             - Clear screen")
    print("  quit              - Exit")
    print()
    print("\(Colors.green)Usage:\(Colors.reset)")
    print("  Just type any operation with arguments:")
    print("    add 5 3")
    print("    sqrt 16")
    print("    sin 1.57")
    print()
}

// Main REPL function
func runREPL() {
    let executor = OperationExecutor.shared
    let registry = OperationRegistry.shared

    printWelcome()

    while true {
        // Print prompt
        print("\(Colors.blue)mathcli>\(Colors.reset) ", terminator: "")

        // Read input
        guard let input = readLine()?.trimmingCharacters(in: .whitespaces) else {
            continue
        }

        // Skip empty input
        if input.isEmpty {
            continue
        }

        // Handle special commands
        if input == "quit" || input == "exit" {
            print("\(Colors.yellow)Goodbye!\(Colors.reset)")
            break
        }

        if input == "help" {
            printHelp()
            continue
        }

        if input == "clear" {
            print("\u{001B}[2J\u{001B}[H", terminator: "")
            printWelcome()
            continue
        }

        if input == "list" {
            let operations = registry.getAllOperationNames()
            print("\(Colors.green)All Operations (\(operations.count)):\(Colors.reset)")
            for (index, name) in operations.enumerated() {
                print("  \(index + 1). \(name)")
            }
            print()
            continue
        }

        if input == "categories" {
            let categories = registry.getAvailableCategories()
            print("\(Colors.green)Operation Categories:\(Colors.reset)")
            for category in categories {
                let ops = registry.getOperations(in: category)
                print("  \(category.rawValue) (\(ops.count) operations)")
            }
            print()
            continue
        }

        if input.hasPrefix("search ") {
            let query = String(input.dropFirst(7))
            let results = registry.searchOperations(query: query)
            print("\(Colors.green)Search Results for '\(query)':\(Colors.reset)")
            if results.isEmpty {
                print("  No operations found")
            } else {
                for (name, opType) in results {
                    print("  \(name) - \(opType.help)")
                }
            }
            print()
            continue
        }

        if input == "vars" {
            let store = VariableStore.shared
            let vars = store.getAllVariables()
            print("\(Colors.green)Variables:\(Colors.reset)")
            if vars.isEmpty {
                print("  No variables defined")
            } else {
                for (name, value) in vars {
                    print("  \(name) = \(value)")
                }
            }
            print()
            continue
        }

        if input == "funcs" {
            let funcRegistry = FunctionRegistry.shared
            let funcs = funcRegistry.getAllFunctions()
            print("\(Colors.green)User-Defined Functions:\(Colors.reset)")
            if funcs.isEmpty {
                print("  No functions defined")
            } else {
                for (name, _) in funcs {
                    print("  \(name)()")
                }
            }
            print()
            continue
        }

        // Execute operation
        do {
            let result = try executor.execute(command: input)
            print("\(Colors.green)Result:\(Colors.reset) \(formatResult(result))")
        } catch let error as OperationError {
            print("\(Colors.red)Error:\(Colors.reset) \(error.localizedDescription)")
        } catch {
            print("\(Colors.red)Error:\(Colors.reset) \(error.localizedDescription)")
        }
        print()
    }
}

// Format result for display
func formatResult(_ result: OperationResult) -> String {
    switch result {
    case .number(let value):
        return String(format: "%.10g", value)
    case .integer(let value):
        return "\(value)"
    case .string(let value):
        return value
    case .boolean(let value):
        return value ? "true" : "false"
    case .array(let values):
        return "[\(values.map { String(format: "%.6g", $0) }.joined(separator: ", "))]"
    case .matrix(let rows):
        var result = "[\n"
        for row in rows {
            result += "  [\(row.map { String(format: "%.6g", $0) }.joined(separator: ", "))]\n"
        }
        result += "]"
        return result
    case .complex(let real, let imaginary):
        if imaginary >= 0 {
            return "\(String(format: "%.6g", real)) + \(String(format: "%.6g", imaginary))i"
        } else {
            return "\(String(format: "%.6g", real)) - \(String(format: "%.6g", abs(imaginary)))i"
        }
    case .dictionary(let dict):
        return dict.description
    case .dataFrame(let data):
        return "DataFrame: \(data.description)"
    case .void:
        return "(no output)"
    }
}

// Run the REPL
runREPL()
