//
//  VariableStore.swift
//  MathCLI
//
//  Variable storage with scoping and persistence support
//

import Foundation

/// Manages variables with scoping and persistence
class VariableStore {
    static let shared = VariableStore()

    // Current session ID for scoping variables
    private var currentSessionId: UUID?

    // Stack of scopes (each scope is a dictionary of variables)
    private var scopes: [[String: OperationResult]] = [[:]]

    // Persistent variables (saved across sessions) - now session-specific
    private var persistentVariables: [String: OperationResult] = [:]

    // Set of variable names that should be persisted
    private var persistentKeys: Set<String> = []

    private let persistenceKey = "MathCLI.PersistentVariables"
    private let persistenceKeysKey = "MathCLI.PersistentKeys"

    private init() {
        // Variables will be loaded when session is set
    }

    /// Set the current session and load its variables
    func setSession(_ sessionId: UUID?) {
        // Save current session's variables before switching
        if let currentId = currentSessionId {
            saveSessionVariables(for: currentId)
        }

        // Switch to new session
        currentSessionId = sessionId

        // Load new session's variables
        if let sessionId = sessionId {
            loadSessionVariables(for: sessionId)
        } else {
            scopes = [[:]]
            persistentVariables = [:]
            persistentKeys = []
        }
    }

    /// Get the current session ID
    func getCurrentSessionId() -> UUID? {
        return currentSessionId
    }

    /// Set a variable in the current scope
    func set(name: String, value: OperationResult, persist: Bool = false) {
        guard !scopes.isEmpty else {
            scopes.append([name: value])
            return
        }

        scopes[scopes.count - 1][name] = value

        if persist {
            persistentKeys.insert(name)
            persistentVariables[name] = value
            savePersistentVariables()
        }
    }

    /// Get a variable value (searches from current scope upwards)
    func get(name: String) -> OperationResult? {
        // Search in scopes from innermost to outermost
        for scope in scopes.reversed() {
            if let value = scope[name] {
                return value
            }
        }

        // Check persistent variables
        return persistentVariables[name]
    }

    /// Remove a variable from current scope
    func unset(name: String) {
        guard !scopes.isEmpty else { return }
        scopes[scopes.count - 1].removeValue(forKey: name)

        // Also remove from persistent if it exists
        if persistentKeys.contains(name) {
            persistentKeys.remove(name)
            persistentVariables.removeValue(forKey: name)
            savePersistentVariables()
        }
    }

    /// Get all variables in current scope
    func getAllVariables() -> [String: OperationResult] {
        var allVars: [String: OperationResult] = [:]

        // Merge all scopes (outer scopes first, then override with inner)
        for scope in scopes {
            allVars.merge(scope) { _, new in new }
        }

        // Add persistent variables
        allVars.merge(persistentVariables) { _, new in new }

        return allVars
    }

    /// Get all variable names
    func getAllVariableNames() -> [String] {
        return Array(getAllVariables().keys).sorted()
    }

    /// Clear all variables in current scope
    func clearCurrentScope() {
        guard !scopes.isEmpty else { return }
        scopes[scopes.count - 1].removeAll()
    }

    /// Clear all variables including persistent
    func clearAll() {
        scopes = [[:]]
        persistentVariables.removeAll()
        persistentKeys.removeAll()
        savePersistentVariables()
    }

    /// Push a new scope onto the stack
    func pushScope() {
        scopes.append([:])
    }

    /// Pop the current scope from the stack
    func popScope() {
        guard scopes.count > 1 else { return }
        scopes.removeLast()
    }

    /// Make a variable persistent
    func persist(name: String) {
        guard let value = get(name) else { return }
        persistentKeys.insert(name)
        persistentVariables[name] = value
        savePersistentVariables()
    }

    /// Get persistent variable names
    func getPersistentVariableNames() -> [String] {
        return Array(persistentKeys).sorted()
    }

    /// Check if a variable exists
    func exists(name: String) -> Bool {
        return get(name) != nil
    }

    /// Export all variables to dictionary
    func exportVariables() -> [String: String] {
        let allVars = getAllVariables()
        var exported: [String: String] = [:]

        for (key, value) in allVars {
            exported[key] = value.description
        }

        return exported
    }

    /// Import variables from dictionary
    func importVariables(_ variables: [String: String], merge: Bool = true) {
        if !merge {
            clearAll()
        }

        for (key, valueStr) in variables {
            // Try to parse as number
            if let numValue = Double(valueStr) {
                set(name: key, value: .number(numValue))
            } else if valueStr == "true" {
                set(name: key, value: .boolean(true))
            } else if valueStr == "false" {
                set(name: key, value: .boolean(false))
            } else {
                set(name: key, value: .string(valueStr))
            }
        }
    }

    // MARK: - Persistence

    private func sessionPersistenceKey(for sessionId: UUID) -> String {
        return "\(persistenceKey).\(sessionId.uuidString)"
    }

    private func sessionKeysKey(for sessionId: UUID) -> String {
        return "\(persistenceKeysKey).\(sessionId.uuidString)"
    }

    private func saveSessionVariables(for sessionId: UUID) {
        let defaults = UserDefaults.standard

        // Save persistent variable values
        var savedVars: [String: String] = [:]
        for (key, value) in persistentVariables {
            savedVars[key] = value.description
        }

        defaults.set(savedVars, forKey: sessionPersistenceKey(for: sessionId))
        defaults.set(Array(persistentKeys), forKey: sessionKeysKey(for: sessionId))

        // Save current scope variables (session-specific)
        var scopeVars: [String: String] = [:]
        for scope in scopes {
            for (key, value) in scope {
                scopeVars[key] = value.description
            }
        }
        defaults.set(scopeVars, forKey: "MathCLI.SessionScopes.\(sessionId.uuidString)")
    }

    private func loadSessionVariables(for sessionId: UUID) {
        let defaults = UserDefaults.standard

        // Load persistent keys
        if let keys = defaults.array(forKey: sessionKeysKey(for: sessionId)) as? [String] {
            persistentKeys = Set(keys)
        } else {
            persistentKeys = []
        }

        // Load persistent variables
        persistentVariables = [:]
        if let savedVars = defaults.dictionary(forKey: sessionPersistenceKey(for: sessionId)) as? [String: String] {
            for (key, valueStr) in savedVars {
                persistentVariables[key] = parseValue(valueStr)
            }
        }

        // Load scope variables
        scopes = [[:]]
        if let scopeVars = defaults.dictionary(forKey: "MathCLI.SessionScopes.\(sessionId.uuidString)") as? [String: String] {
            for (key, valueStr) in scopeVars {
                scopes[0][key] = parseValue(valueStr)
            }
        }
    }

    private func parseValue(_ valueStr: String) -> OperationResult {
        if let numValue = Double(valueStr) {
            return .number(numValue)
        } else if valueStr == "true" {
            return .boolean(true)
        } else if valueStr == "false" {
            return .boolean(false)
        } else {
            return .string(valueStr)
        }
    }

    private func savePersistentVariables() {
        guard let sessionId = currentSessionId else { return }
        saveSessionVariables(for: sessionId)
    }

    private func loadPersistentVariables() {
        guard let sessionId = currentSessionId else { return }
        loadSessionVariables(for: sessionId)
    }
}
