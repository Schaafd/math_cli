//
//  ExportOperations.swift
//  MathCLI
//
//  Export and import operations (6 operations)
//

import Foundation

// MARK: - Export Session

struct ExportSessionOperation: MathOperation {
    static var name = "export_session"
    static var arguments = ["filepath", "format"]
    static var help = "Export session (vars + funcs): export_session filepath [format]"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])
        let format = args.count > 1 ? (args[1] as? String ?? "json") : "json"

        // Get variables and functions
        let variables = VariableStore.shared.exportVariables()
        let functions = FunctionRegistry.shared.exportFunctions()

        // Create session data
        let sessionData: [String: Any] = [
            "exported_at": ISO8601DateFormatter().string(from: Date()),
            "version": "1.0",
            "variables": variables,
            "functions": functions
        ]

        // Export based on format
        switch format.lowercased() {
        case "json":
            if let jsonData = try? JSONSerialization.data(withJSONObject: sessionData, options: .prettyPrinted),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                try jsonString.write(toFile: filepath, atomically: true, encoding: .utf8)
            }

        case "markdown", "md":
            var markdown = "# Math CLI Session Export\n\n"
            markdown += "Exported: \(Date())\n\n"
            markdown += "## Variables\n\n"
            for (key, value) in variables {
                markdown += "- `\(key)` = `\(value)`\n"
            }
            markdown += "\n## Functions\n\n"
            for function in functions {
                if let name = function["name"] as? String,
                   let params = function["parameters"] as? [String],
                   let body = function["body"] as? String {
                    markdown += "- `\(name)(\(params.joined(separator: ", ")))` = `\(body)`\n"
                }
            }
            try markdown.write(toFile: filepath, atomically: true, encoding: .utf8)

        default:
            throw OperationError.invalidValue("Unsupported format: \(format). Use 'json' or 'markdown'")
        }

        return .string("Session exported to \(filepath)")
    }
}

// MARK: - Import Session

struct ImportSessionOperation: MathOperation {
    static var name = "import_session"
    static var arguments = ["filepath", "merge"]
    static var help = "Import session: import_session filepath [merge]"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])
        let merge = args.count > 1 ? ((args[1] as? String ?? "false").lowercased() == "true") : true

        // Read file
        guard let jsonString = try? String(contentsOfFile: filepath, encoding: .utf8) else {
            throw OperationError.fileNotFound(filepath)
        }

        guard let jsonData = jsonString.data(using: .utf8),
              let sessionData = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any] else {
            throw OperationError.importError("Invalid JSON format")
        }

        // Import variables
        if let variables = sessionData["variables"] as? [String: String] {
            VariableStore.shared.importVariables(variables, merge: merge)
        }

        // Import functions
        if let functions = sessionData["functions"] as? [[String: Any]] {
            FunctionRegistry.shared.importFunctions(functions, merge: merge)
        }

        return .string("Session imported from \(filepath)")
    }
}

// MARK: - Export Variables

struct ExportVarsOperation: MathOperation {
    static var name = "export_vars"
    static var arguments = ["filepath"]
    static var help = "Export variables to JSON: export_vars filepath"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])
        let variables = VariableStore.shared.exportVariables()

        let data: [String: Any] = [
            "exported_at": ISO8601DateFormatter().string(from: Date()),
            "variables": variables
        ]

        if let jsonData = try? JSONSerialization.data(withJSONObject: data, options: .prettyPrinted),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            try jsonString.write(toFile: filepath, atomically: true, encoding: .utf8)
        }

        return .string("Variables exported to \(filepath)")
    }
}

// MARK: - Import Variables

struct ImportVarsOperation: MathOperation {
    static var name = "import_vars"
    static var arguments = ["filepath"]
    static var help = "Import variables from JSON: import_vars filepath"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])

        guard let jsonString = try? String(contentsOfFile: filepath, encoding: .utf8) else {
            throw OperationError.fileNotFound(filepath)
        }

        guard let jsonData = jsonString.data(using: .utf8),
              let data = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any],
              let variables = data["variables"] as? [String: String] else {
            throw OperationError.importError("Invalid variables file")
        }

        VariableStore.shared.importVariables(variables, merge: true)
        return .string("Variables imported from \(filepath)")
    }
}

// MARK: - Export Functions

struct ExportFuncsOperation: MathOperation {
    static var name = "export_funcs"
    static var arguments = ["filepath"]
    static var help = "Export user functions to JSON: export_funcs filepath"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])
        let functions = FunctionRegistry.shared.exportFunctions()

        let data: [String: Any] = [
            "exported_at": ISO8601DateFormatter().string(from: Date()),
            "functions": functions
        ]

        if let jsonData = try? JSONSerialization.data(withJSONObject: data, options: .prettyPrinted),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            try jsonString.write(toFile: filepath, atomically: true, encoding: .utf8)
        }

        return .string("Functions exported to \(filepath)")
    }
}

// MARK: - Import Functions

struct ImportFuncsOperation: MathOperation {
    static var name = "import_funcs"
    static var arguments = ["filepath"]
    static var help = "Import user functions from JSON: import_funcs filepath"
    static var category = OperationCategory.export

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])

        guard let jsonString = try? String(contentsOfFile: filepath, encoding: .utf8) else {
            throw OperationError.fileNotFound(filepath)
        }

        guard let jsonData = jsonString.data(using: .utf8),
              let data = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any],
              let functions = data["functions"] as? [[String: Any]] else {
            throw OperationError.importError("Invalid functions file")
        }

        FunctionRegistry.shared.importFunctions(functions, merge: true)
        return .string("Functions imported from \(filepath)")
    }
}
