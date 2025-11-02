//
//  ScriptOperations.swift
//  MathCLI
//
//  Script execution operations (2 operations)
//

import Foundation

// MARK: - Run Script

struct RunOperation: MathOperation {
    static var name = "run"
    static var arguments = ["filepath"]
    static var help = "Run a .mathcli script file: run filepath"
    static var category = OperationCategory.scripts

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])

        // Read file
        guard let scriptContent = try? String(contentsOfFile: filepath, encoding: .utf8) else {
            throw OperationError.fileNotFound(filepath)
        }

        // Split into lines
        let lines = scriptContent.components(separatedBy: .newlines)

        // Execute line by line
        let executor = OperationExecutor()
        var lastResult: OperationResult = .void

        for line in lines {
            let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)

            // Skip empty lines and comments
            if trimmed.isEmpty || trimmed.hasPrefix("#") {
                continue
            }

            // Execute line
            do {
                lastResult = try executor.execute(command: trimmed)
            } catch {
                throw OperationError.executionError("Script error on line: \(line) - \(error.localizedDescription)")
            }
        }

        return lastResult
    }
}

// MARK: - Eval

struct EvalOperation: MathOperation {
    static var name = "eval"
    static var arguments = ["expression"]
    static var help = "Evaluate an expression string: eval expression"
    static var category = OperationCategory.scripts

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let expression = args[0] as? String ?? String(describing: args[0])

        let executor = OperationExecutor()
        return try executor.execute(command: expression)
    }
}
