//
//  SettingsView.swift
//  MathCLI
//
//  App settings and preferences
//

import SwiftUI

struct SettingsView: View {
    @AppStorage("decimalPlaces") private var decimalPlaces = 6
    @AppStorage("historyLimit") private var historyLimit = 1000
    @AppStorage("enableHaptics") private var enableHaptics = true
    @AppStorage("enableSuggestions") private var enableSuggestions = true
    @AppStorage("theme") private var selectedTheme = "default"
    @AppStorage("iCloudSync") private var iCloudSync = false

    var body: some View {
        NavigationStack {
            List {
                // Display Settings
                Section("Display") {
                    Stepper("Decimal Places: \(decimalPlaces)", value: $decimalPlaces, in: 0...15)

                    Picker("Theme", selection: $selectedTheme) {
                        Text("Default").tag("default")
                        Text("Dark").tag("dark")
                        Text("Light").tag("light")
                        Text("Ocean").tag("ocean")
                        Text("Forest").tag("forest")
                        Text("Sunset").tag("sunset")
                        Text("Synthwave").tag("synthwave")
                        Text("High Contrast").tag("high-contrast")
                    }
                }

                // Calculator Settings
                Section("Calculator") {
                    Toggle("Show Suggestions", isOn: $enableSuggestions)
                    Toggle("Haptic Feedback", isOn: $enableHaptics)

                    Stepper("History Limit: \(historyLimit)", value: $historyLimit, in: 100...5000, step: 100)
                }

                // iCloud Settings
                Section("iCloud") {
                    Toggle("iCloud Sync", isOn: $iCloudSync)

                    if iCloudSync {
                        Text("Sync calculation history, variables, and functions across your devices")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                // Data Management
                Section("Data") {
                    Button("Export Session") {
                        exportSession()
                    }

                    Button("Import Session") {
                        importSession()
                    }

                    Button("Clear All Variables", role: .destructive) {
                        clearVariables()
                    }

                    Button("Clear All Functions", role: .destructive) {
                        clearFunctions()
                    }
                }

                // About
                Section("About") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }

                    HStack {
                        Text("Operations")
                        Spacer()
                        Text("\(OperationRegistry.shared.count)")
                            .foregroundColor(.secondary)
                    }

                    Link("Documentation", destination: URL(string: "https://github.com/yourusername/mathcli-ios")!)

                    Link("Report Issue", destination: URL(string: "https://github.com/yourusername/mathcli-ios/issues")!)
                }
            }
            .navigationTitle("Settings")
        }
    }

    private func exportSession() {
        // TODO: Implement export
        print("Export session")
    }

    private func importSession() {
        // TODO: Implement import
        print("Import session")
    }

    private func clearVariables() {
        VariableStore.shared.clearAll()
    }

    private func clearFunctions() {
        FunctionRegistry.shared.clearAll()
    }
}

#Preview {
    SettingsView()
}
