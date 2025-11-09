//
//  MathCLIApp.swift
//  MathCLI
//
//  Main app entry point
//

import SwiftUI
import SwiftData

@main
struct MathCLIApp: App {
    let modelContainer: ModelContainer
    @StateObject private var sessionManager: SessionManager

    init() {
        do {
            // Initialize model container with both Session and HistoryEntry
            let container = try ModelContainer(for: Session.self, HistoryEntry.self)
            modelContainer = container

            // Initialize session manager
            let manager = SessionManager(modelContext: container.mainContext)
            _sessionManager = StateObject(wrappedValue: manager)
        } catch {
            fatalError("Failed to initialize ModelContainer: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .modelContainer(modelContainer)
                .environmentObject(sessionManager)
        }
    }
}

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            CalculatorView()
                .tabItem {
                    Label("Calculator", systemImage: "function")
                }
                .tag(0)

            HistoryView()
                .tabItem {
                    Label("History", systemImage: "clock")
                }
                .tag(1)

            OperationBrowserView()
                .tabItem {
                    Label("Operations", systemImage: "list.bullet")
                }
                .tag(2)

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
    }
}
