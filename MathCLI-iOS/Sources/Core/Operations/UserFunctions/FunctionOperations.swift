//
//  FunctionOperations.swift
//  MathCLI
//
//  User-defined function operations (3 operations)
//

import Foundation

// MARK: - Define Function

struct DefOperation: MathOperation {
    static var name = "def"
    static var arguments = ["name", "parameters...", "body"]
    static var help = "Define a function: def name param1 param2 ... = body"
    static var category = OperationCategory.userFunctions

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 3 else {
            throw OperationError.invalidArgumentCount(expected: 3, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])
        let body = args.last as? String ?? String(describing: args.last!)

        // Everything between name and body are parameters
        let parameters = args.dropFirst().dropLast().map { arg in
            arg as? String ?? String(describing: arg)
        }

        FunctionRegistry.shared.define(name: name, parameters: parameters, body: body)
        return .void
    }
}

// MARK: - List Functions

struct FuncsOperation: MathOperation {
    static var name = "funcs"
    static var arguments = []
    static var help = "List all user-defined functions: funcs"
    static var category = OperationCategory.userFunctions

    static func execute(args: [Any]) throws -> OperationResult {
        let functions = FunctionRegistry.shared.getAllFunctions()

        if functions.isEmpty {
            return .string("No user-defined functions")
        }

        let funcList = functions.map { function in
            let params = function.parameters.joined(separator: ", ")
            return "\(function.name)(\(params)) = \(function.body)"
        }.joined(separator: "\n")

        return .string(funcList)
    }
}

// MARK: - Undefine Function

struct UndefOperation: MathOperation {
    static var name = "undef"
    static var arguments = ["name"]
    static var help = "Delete a user-defined function: undef name"
    static var category = OperationCategory.userFunctions

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let name = args[0] as? String ?? String(describing: args[0])

        guard FunctionRegistry.shared.exists(name: name) else {
            throw OperationError.functionNotFound(name)
        }

        FunctionRegistry.shared.undefine(name: name)
        return .void
    }
}
