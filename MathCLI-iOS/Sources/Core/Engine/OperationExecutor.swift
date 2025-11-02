//
//  OperationExecutor.swift
//  MathCLI
//
//  Executes mathematical operations with variable substitution
//

import Foundation

/// Executes operations and manages the calculation context
class OperationExecutor {
    private let registry: OperationRegistry
    private let variableStore: VariableStore
    private let functionRegistry: FunctionRegistry

    var lastResult: OperationResult = .void

    init(registry: OperationRegistry = .shared,
         variableStore: VariableStore = .shared,
         functionRegistry: FunctionRegistry = .shared) {
        self.registry = registry
        self.variableStore = variableStore
        self.functionRegistry = functionRegistry
    }

    /// Execute a command string
    /// - Parameter command: The command to execute (e.g., "add 5 10" or "multiply $x $y")
    /// - Returns: Result of the execution
    /// - Throws: OperationError if execution fails
    func execute(command: String) throws -> OperationResult {
        let trimmed = command.trimmingCharacters(in: .whitespacesAndNewlines)

        guard !trimmed.isEmpty else {
            return .void
        }

        // Check for chain operations (separated by |)
        if trimmed.contains("|") {
            return try executeChain(trimmed)
        }

        // Parse command into components
        let components = parseCommand(trimmed)
        guard !components.isEmpty else {
            return .void
        }

        let operationName = components[0]
        var args = Array(components.dropFirst())

        // Substitute variables and special references
        args = try substituteVariables(args)

        // Check if it's a user-defined function
        if let userFunction = functionRegistry.getFunction(name: operationName) {
            return try executeUserFunction(userFunction, args: args)
        }

        // Get the operation from registry
        guard let operation = registry.getOperation(name: operationName) else {
            throw OperationError.operationNotFound(operationName)
        }

        // Validate argument count (skip for variadic operations)
        if !operation.isVariadic && args.count != operation.arguments.count {
            throw OperationError.invalidArgumentCount(
                expected: operation.arguments.count,
                got: args.count
            )
        }

        // Execute the operation
        let result = try operation.execute(args: args)

        // Store as last result
        lastResult = result
        variableStore.set(name: "ans", value: result)
        variableStore.set(name: "$", value: result)

        return result
    }

    /// Execute a chain of operations (e.g., "add 5 10 | multiply 2 | sqrt")
    private func executeChain(_ command: String) throws -> OperationResult {
        let operations = command.components(separatedBy: "|").map {
            $0.trimmingCharacters(in: .whitespacesAndNewlines)
        }

        var result: OperationResult = .void

        for (index, operation) in operations.enumerated() {
            if index == 0 {
                // First operation executes normally
                result = try execute(command: operation)
            } else {
                // Subsequent operations use previous result as first argument
                let components = parseCommand(operation)
                guard !components.isEmpty else { continue }

                let operationName = components[0]
                var args = Array(components.dropFirst())

                // Prepend the previous result
                args.insert(resultToString(result), at: 0)

                // Execute with substitution
                args = try substituteVariables(args)

                guard let op = registry.getOperation(name: operationName) else {
                    throw OperationError.operationNotFound(operationName)
                }

                result = try op.execute(args: args)
            }
        }

        lastResult = result
        return result
    }

    /// Parse command string into components, respecting quotes
    private func parseCommand(_ command: String) -> [String] {
        var components: [String] = []
        var current = ""
        var inQuotes = false

        for char in command {
            if char == "\"" {
                inQuotes.toggle()
            } else if char.isWhitespace && !inQuotes {
                if !current.isEmpty {
                    components.append(current)
                    current = ""
                }
            } else {
                current.append(char)
            }
        }

        if !current.isEmpty {
            components.append(current)
        }

        return components
    }

    /// Substitute variable references in arguments
    private func substituteVariables(_ args: [String]) throws -> [String] {
        return try args.map { arg in
            // Check for variable reference
            if arg.hasPrefix("$") {
                let varName = String(arg.dropFirst())

                // Special case for $ and ans
                if varName.isEmpty || varName == "ans" {
                    return resultToString(lastResult)
                }

                // Get from variable store
                guard let value = variableStore.get(name: varName) else {
                    throw OperationError.variableNotFound(varName)
                }

                return resultToString(value)
            }

            return arg
        }
    }

    /// Convert OperationResult to String for argument passing
    private func resultToString(_ result: OperationResult) -> String {
        switch result {
        case .number(let value):
            return "\(value)"
        case .integer(let value):
            return "\(value)"
        case .string(let value):
            return value
        case .boolean(let value):
            return value ? "true" : "false"
        case .array(let values):
            return values.map { "\($0)" }.joined(separator: ",")
        default:
            return result.description
        }
    }

    /// Execute a user-defined function
    private func executeUserFunction(_ function: UserFunction, args: [String]) throws -> OperationResult {
        guard args.count == function.parameters.count else {
            throw OperationError.invalidArgumentCount(
                expected: function.parameters.count,
                got: args.count
            )
        }

        // Create new scope
        variableStore.pushScope()

        // Bind parameters to arguments
        for (param, arg) in zip(function.parameters, args) {
            // Try to parse as number, otherwise store as string
            if let numValue = Double(arg) {
                variableStore.set(name: param, value: .number(numValue))
            } else {
                variableStore.set(name: param, value: .string(arg))
            }
        }

        // Execute function body
        let result: OperationResult
        do {
            result = try execute(command: function.body)
        } catch {
            variableStore.popScope()
            throw error
        }

        // Pop scope
        variableStore.popScope()

        return result
    }
}
