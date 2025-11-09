//
//  CalculatorViewModel.swift
//  MathCLI
//
//  View model for calculator logic
//

import Foundation
import SwiftUI
import Combine

@MainActor
class CalculatorViewModel: ObservableObject {
    @Published var inputText: String = ""
    @Published var outputLines: [OutputLine] = []
    @Published var suggestions: [String] = []
    @Published var showSuggestions: Bool = false
    @Published var errorMessage: String?

    private let executor: OperationExecutor
    private let registry: OperationRegistry
    private let variableStore: VariableStore
    var historyManager: HistoryManager?

    struct OutputLine: Identifiable {
        let id = UUID()
        let type: LineType
        let text: String
        let timestamp: Date

        enum LineType {
            case command
            case result
            case error
            case info
        }

        var color: Color {
            switch type {
            case .command: return .cyan
            case .result: return .green
            case .error: return .red
            case .info: return .orange
            }
        }
    }

    init(historyManager: HistoryManager? = nil) {
        self.executor = OperationExecutor()
        self.registry = OperationRegistry.shared
        self.variableStore = VariableStore.shared
        self.historyManager = historyManager

        // Add welcome message
        addOutputLine("Welcome to Math CLI", type: .info)
        addOutputLine("Type an operation or 'help' for commands", type: .info)
        addOutputLine("", type: .info)
    }

    func executeCommand() {
        let command = inputText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !command.isEmpty else { return }

        // Add command to output
        addOutputLine("> \(command)", type: .command)

        // Handle special commands
        if handleSpecialCommand(command) {
            inputText = ""
            return
        }

        // Execute the command
        do {
            let result = try executor.execute(command: command)

            // Add result to output
            let resultText = result.description
            if !resultText.isEmpty {
                addOutputLine(resultText, type: .result)
            }

            // Add to history
            historyManager?.addEntry(command: command, result: resultText)

            errorMessage = nil
        } catch {
            let errorText = error.localizedDescription
            addOutputLine(errorText, type: .error)
            errorMessage = errorText

            // Suggest similar operations if not found
            if case OperationError.operationNotFound(let name) = error {
                suggestSimilarOperations(name)
            }
        }

        inputText = ""
    }

    func updateSuggestions() {
        let trimmed = inputText.trimmingCharacters(in: .whitespacesAndNewlines)

        guard !trimmed.isEmpty else {
            suggestions = []
            showSuggestions = false
            return
        }

        // Get operation name (first word)
        let components = trimmed.components(separatedBy: " ")
        let operationName = components[0]

        // Search for matching operations
        let matches = registry.searchOperations(query: operationName)

        suggestions = matches.prefix(5).map { $0.0 }
        showSuggestions = !suggestions.isEmpty && !trimmed.contains(" ")
    }

    func selectSuggestion(_ suggestion: String) {
        inputText = suggestion + " "
        suggestions = []
        showSuggestions = false
    }

    func addOutputLine(_ text: String, type: OutputLine.LineType) {
        let line = OutputLine(type: type, text: text, timestamp: Date())
        outputLines.append(line)

        // Limit output lines to prevent memory issues
        if outputLines.count > 500 {
            outputLines.removeFirst(100)
        }
    }

    private func handleSpecialCommand(_ command: String) -> Bool {
        let components = command.components(separatedBy: " ")
        let cmd = components[0].lowercased()

        switch cmd {
        case "help":
            showHelp()
            return true

        case "clear", "cls":
            clearOutput()
            return true

        case "vars":
            showVariables()
            return true

        case "funcs":
            showFunctions()
            return true

        case "categories":
            showCategories()
            return true

        case "ops", "operations":
            if components.count > 1 {
                showOperationsInCategory(components[1])
            } else {
                showAllOperations()
            }
            return true

        default:
            return false
        }
    }

    private func showHelp() {
        addOutputLine("Available Commands:", type: .info)
        addOutputLine("  help - Show this help message", type: .info)
        addOutputLine("  clear - Clear output", type: .info)
        addOutputLine("  vars - Show all variables", type: .info)
        addOutputLine("  funcs - Show all user functions", type: .info)
        addOutputLine("  categories - Show operation categories", type: .info)
        addOutputLine("  ops [category] - Show operations", type: .info)
        addOutputLine("", type: .info)
        addOutputLine("Examples:", type: .info)
        addOutputLine("  add 5 10", type: .info)
        addOutputLine("  set x 42", type: .info)
        addOutputLine("  multiply $x 2", type: .info)
        addOutputLine("  add 5 10 | multiply 2", type: .info)
    }

    private func clearOutput() {
        outputLines.removeAll()
        addOutputLine("Output cleared", type: .info)
    }

    private func showVariables() {
        let vars = variableStore.getAllVariables()

        if vars.isEmpty {
            addOutputLine("No variables defined", type: .info)
        } else {
            addOutputLine("Variables:", type: .info)
            for (name, value) in vars.sorted(by: { $0.key < $1.key }) {
                addOutputLine("  \(name) = \(value.description)", type: .info)
            }
        }
    }

    private func showFunctions() {
        let functions = FunctionRegistry.shared.getAllFunctions()

        if functions.isEmpty {
            addOutputLine("No user functions defined", type: .info)
        } else {
            addOutputLine("User Functions:", type: .info)
            for function in functions {
                let params = function.parameters.joined(separator: ", ")
                addOutputLine("  \(function.name)(\(params)) = \(function.body)", type: .info)
            }
        }
    }

    private func showCategories() {
        let categories = registry.getAvailableCategories()
        addOutputLine("Operation Categories:", type: .info)
        for category in categories {
            let count = registry.getOperations(in: category).count
            addOutputLine("  \(category.rawValue) (\(count) operations)", type: .info)
        }
    }

    private func showAllOperations() {
        let allOps = registry.getAllOperationNames()
        addOutputLine("All Operations (\(allOps.count)):", type: .info)

        let columns = 3
        var current = ""
        for (index, op) in allOps.enumerated() {
            current += op.padding(toLength: 25, withPad: " ", startingAt: 0)
            if (index + 1) % columns == 0 {
                addOutputLine("  \(current)", type: .info)
                current = ""
            }
        }
        if !current.isEmpty {
            addOutputLine("  \(current)", type: .info)
        }
    }

    private func showOperationsInCategory(_ categoryName: String) {
        guard let category = OperationCategory.allCases.first(where: {
            $0.rawValue.lowercased() == categoryName.lowercased()
        }) else {
            addOutputLine("Category not found: \(categoryName)", type: .error)
            return
        }

        let ops = registry.getOperations(in: category)
        addOutputLine("\(category.rawValue) Operations:", type: .info)
        for (name, _) in ops {
            addOutputLine("  \(name)", type: .info)
        }
    }

    private func suggestSimilarOperations(_ name: String) {
        let similar = registry.searchOperations(query: name)
        if !similar.isEmpty {
            addOutputLine("Did you mean:", type: .info)
            for (opName, _) in similar.prefix(3) {
                addOutputLine("  \(opName)", type: .info)
            }
        }
    }
}
