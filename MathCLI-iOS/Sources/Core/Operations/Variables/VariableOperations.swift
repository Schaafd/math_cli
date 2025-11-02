//
//  VariableOperations.swift
//  MathCLI
//
//  Variable management operations (6 operations)
//

import Foundation

// MARK: - Set Variable

struct SetOperation: MathOperation {
    static var name = "set"
    static var arguments = ["name", "value"]
    static var help = "Set a variable: set name value"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])
        let value = try parseDouble(args[1], argumentName: "value")

        VariableStore.shared.set(name: name, value: .number(value))
        return .void
    }
}

// MARK: - Persist Variable

struct PersistOperation: MathOperation {
    static var name = "persist"
    static var arguments = ["name"]
    static var help = "Make a variable persistent: persist name"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])

        guard VariableStore.shared.exists(name: name) else {
            throw OperationError.variableNotFound(name)
        }

        VariableStore.shared.persist(name: name)
        return .void
    }
}

// MARK: - Get Variable

struct GetOperation: MathOperation {
    static var name = "get"
    static var arguments = ["name"]
    static var help = "Get a variable value: get name"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])

        guard let value = VariableStore.shared.get(name: name) else {
            throw OperationError.variableNotFound(name)
        }

        return value
    }
}

// MARK: - List Variables

struct VarsOperation: MathOperation {
    static var name = "vars"
    static var arguments = []
    static var help = "List all variables: vars"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        let vars = VariableStore.shared.getAllVariables()

        if vars.isEmpty {
            return .string("No variables defined")
        }

        let varList = vars.map { "\($0.key) = \($0.value.description)" }.joined(separator: "\n")
        return .string(varList)
    }
}

// MARK: - Unset Variable

struct UnsetOperation: MathOperation {
    static var name = "unset"
    static var arguments = ["name"]
    static var help = "Delete a variable: unset name"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])
        VariableStore.shared.unset(name: name)
        return .void
    }
}

// MARK: - Clear All Variables

struct ClearVarsOperation: MathOperation {
    static var name = "clear_vars"
    static var arguments = []
    static var help = "Clear all variables: clear_vars"
    static var category = OperationCategory.variables

    static func execute(args: [Any]) throws -> OperationResult {
        VariableStore.shared.clearAll()
        return .void
    }
}
