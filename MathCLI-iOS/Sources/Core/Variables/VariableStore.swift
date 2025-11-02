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

    // Stack of scopes (each scope is a dictionary of variables)
    private var scopes: [[String: OperationResult]] = [[:]]

    // Persistent variables (saved across sessions)
    private var persistentVariables: [String: OperationResult] = [:]

    // Set of variable names that should be persisted
    private var persistentKeys: Set<String> = []

    private let persistenceKey = "MathCLI.PersistentVariables"
    private let persistenceKeysKey = "MathCLI.PersistentKeys"

    private init() {
        loadPersistentVariables()
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

    private func savePersistentVariables() {
        let defaults = UserDefaults.standard

        // Save persistent variable values
        var savedVars: [String: String] = [:]
        for (key, value) in persistentVariables {
            savedVars[key] = value.description
        }

        defaults.set(savedVars, forKey: persistenceKey)
        defaults.set(Array(persistentKeys), forKey: persistenceKeysKey)
    }

    private func loadPersistentVariables() {
        let defaults = UserDefaults.standard

        // Load persistent keys
        if let keys = defaults.array(forKey: persistenceKeysKey) as? [String] {
            persistentKeys = Set(keys)
        }

        // Load persistent variables
        if let savedVars = defaults.dictionary(forKey: persistenceKey) as? [String: String] {
            for (key, valueStr) in savedVars {
                if let numValue = Double(valueStr) {
                    persistentVariables[key] = .number(numValue)
                } else if valueStr == "true" {
                    persistentVariables[key] = .boolean(true)
                } else if valueStr == "false" {
                    persistentVariables[key] = .boolean(false)
                } else {
                    persistentVariables[key] = .string(valueStr)
                }
            }
        }
    }
}
