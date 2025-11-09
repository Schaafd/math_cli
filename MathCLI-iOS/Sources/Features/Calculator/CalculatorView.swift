//
//  CalculatorView.swift
//  MathCLI
//
//  Main calculator view with hybrid terminal-modern UI
//

import SwiftUI
import SwiftData

struct CalculatorView: View {
    @Environment(\.modelContext) private var modelContext
    @EnvironmentObject private var sessionManager: SessionManager
    @StateObject private var viewModel: CalculatorViewModel
    @State private var historyManager: HistoryManager?
    @FocusState private var isInputFocused: Bool
    @State private var scrollProxy: ScrollViewProxy?
    @State private var showingRenameSheet = false
    @State private var sessionToRename: Session?
    @State private var newSessionName = ""

    init() {
        _viewModel = StateObject(wrappedValue: CalculatorViewModel())
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Session tabs at the top
                sessionTabBar

                Divider()

                // Terminal-style output area
                terminalOutput

                Divider()

                // Modern input controls
                inputArea
            }
            .background(Color(uiColor: .systemBackground))
            .navigationTitle("Math CLI")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button("New Session", systemImage: "plus.circle") {
                            createNewSession()
                        }
                        Divider()
                        Button("Clear Output", systemImage: "trash") {
                            viewModel.outputLines.removeAll()
                        }
                        Button("Show Variables", systemImage: "x.squareroot") {
                            viewModel.inputText = "vars"
                            viewModel.executeCommand()
                        }
                        Button("Show Help", systemImage: "questionmark.circle") {
                            viewModel.inputText = "help"
                            viewModel.executeCommand()
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
            .sheet(isPresented: $showingRenameSheet) {
                renameSessionSheet
            }
            .onAppear {
                setupCurrentSession()
            }
            .onChange(of: sessionManager.activeSession) { _, newSession in
                switchToSession(newSession)
            }
        }
    }

    // MARK: - Session Tab Bar

    private var sessionTabBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                // Debug: Show session count
                if sessionManager.sessions.isEmpty {
                    Text("No sessions - Debug")
                        .font(.caption)
                        .foregroundColor(.red)
                }

                ForEach(sessionManager.sessions) { session in
                    SessionTab(
                        session: session,
                        isActive: session.id == sessionManager.activeSession?.id,
                        onTap: {
                            sessionManager.switchToSession(session)
                        },
                        onClose: {
                            sessionManager.deleteSession(session)
                        },
                        onRename: {
                            sessionToRename = session
                            newSessionName = session.name
                            showingRenameSheet = true
                        }
                    )
                }

                // Add new session button
                Button {
                    createNewSession()
                } label: {
                    Image(systemName: "plus")
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundColor(.secondary)
                        .frame(width: 32, height: 32)
                        .background(Color(uiColor: .tertiarySystemBackground))
                        .cornerRadius(6)
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
        }
        .frame(minHeight: 50)
        .background(Color(uiColor: .secondarySystemBackground))
    }

    private var renameSessionSheet: some View {
        NavigationStack {
            Form {
                TextField("Session Name", text: $newSessionName)
                    .textInputAutocapitalization(.words)
            }
            .navigationTitle("Rename Session")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        showingRenameSheet = false
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        if let session = sessionToRename, !newSessionName.isEmpty {
                            sessionManager.renameSession(session, newName: newSessionName)
                        }
                        showingRenameSheet = false
                    }
                    .disabled(newSessionName.isEmpty)
                }
            }
        }
        .presentationDetents([.height(200)])
    }

    // MARK: - Helper Methods

    private func setupCurrentSession() {
        print("🔍 CalculatorView.setupCurrentSession: Called")
        print("🔍 CalculatorView: SessionManager has \(sessionManager.sessions.count) sessions")
        print("🔍 CalculatorView: Active session: \(sessionManager.activeSession?.name ?? "nil")")

        // Initialize history manager if needed
        if historyManager == nil {
            historyManager = HistoryManager(modelContext: modelContext)
        }

        if let session = sessionManager.activeSession {
            historyManager?.setCurrentSession(session)
            viewModel.historyManager = historyManager
            VariableStore.shared.setSession(session.id)
            print("🔍 CalculatorView.setupCurrentSession: Setup complete for session: \(session.name)")
        } else {
            print("🔍 CalculatorView.setupCurrentSession: WARNING - No active session!")
        }
    }

    private func switchToSession(_ session: Session?) {
        guard let session = session else { return }

        // Initialize history manager if needed
        if historyManager == nil {
            historyManager = HistoryManager(modelContext: modelContext)
        }

        // Switch history manager to new session
        historyManager?.setCurrentSession(session)
        viewModel.historyManager = historyManager

        // Load new session's variables
        VariableStore.shared.setSession(session.id)

        // Haptic feedback
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()

        // Clear output (optional - could preserve per session)
        viewModel.outputLines.removeAll()
        viewModel.addOutputLine("📋 Switched to \(session.name)", type: .info)

        // Show variable count if any
        let vars = VariableStore.shared.getAllVariables()
        if !vars.isEmpty {
            viewModel.addOutputLine("\(vars.count) variable\(vars.count == 1 ? "" : "s") loaded", type: .info)
        }

        viewModel.addOutputLine("", type: .info)

        // Refocus input
        isInputFocused = true
    }

    private func createNewSession() {
        // Haptic feedback
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)

        sessionManager.createSession()
        if let newSession = sessionManager.activeSession {
            switchToSession(newSession)
        }
    }

    // MARK: - Terminal Output

    private var terminalOutput: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 4) {
                    ForEach(viewModel.outputLines) { line in
                        HStack(alignment: .top, spacing: 8) {
                            // Timestamp
                            Text(line.timestamp, style: .time)
                                .font(.system(.caption, design: .monospaced))
                                .foregroundColor(.secondary)
                                .frame(width: 60, alignment: .leading)

                            // Output text
                            Text(line.text)
                                .font(.system(.body, design: .monospaced))
                                .foregroundColor(line.color)
                                .textSelection(.enabled)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 2)
                        .id(line.id)
                    }
                }
                .padding(.vertical, 12)
            }
            .background(Color(uiColor: .secondarySystemBackground))
            .onAppear {
                scrollProxy = proxy
            }
            .onChange(of: viewModel.outputLines.count) { _, _ in
                if let lastLine = viewModel.outputLines.last {
                    withAnimation {
                        proxy.scrollTo(lastLine.id, anchor: .bottom)
                    }
                }
            }
        }
    }

    // MARK: - Input Area

    private var inputArea: some View {
        VStack(spacing: 0) {
            // Suggestions
            if viewModel.showSuggestions {
                suggestionBar
            }

            // Input field
            HStack(spacing: 12) {
                // Prompt indicator
                Text(">")
                    .font(.system(.title2, design: .monospaced))
                    .foregroundColor(.green)

                // Text field
                TextField("Enter operation...", text: $viewModel.inputText)
                    .font(.system(.body, design: .monospaced))
                    .textInputAutocapitalization(.never)
                    .autocorrectionDisabled()
                    .focused($isInputFocused)
                    .onSubmit {
                        viewModel.executeCommand()
                        isInputFocused = true
                    }
                    .onChange(of: viewModel.inputText) { _, _ in
                        viewModel.updateSuggestions()
                    }

                // Execute button
                Button {
                    viewModel.executeCommand()
                    isInputFocused = true
                } label: {
                    Image(systemName: "arrow.up.circle.fill")
                        .font(.title2)
                        .foregroundColor(viewModel.inputText.isEmpty ? .gray : .blue)
                }
                .disabled(viewModel.inputText.isEmpty)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)

            // Quick action toolbar
            quickActionToolbar
        }
        .background(Color(uiColor: .systemBackground))
        .onAppear {
            isInputFocused = true
        }
    }

    // MARK: - Suggestion Bar

    private var suggestionBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(viewModel.suggestions, id: \.self) { suggestion in
                    Button {
                        viewModel.selectSuggestion(suggestion)
                    } label: {
                        Text(suggestion)
                            .font(.system(.footnote, design: .monospaced))
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Color.blue.opacity(0.2))
                            .cornerRadius(8)
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
        }
        .background(Color(uiColor: .tertiarySystemBackground))
    }

    // MARK: - Quick Action Toolbar

    private var quickActionToolbar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                // Common operations
                QuickActionButton(title: "+", operation: "add") {
                    insertOperation("add ")
                }

                QuickActionButton(title: "−", operation: "subtract") {
                    insertOperation("subtract ")
                }

                QuickActionButton(title: "×", operation: "multiply") {
                    insertOperation("multiply ")
                }

                QuickActionButton(title: "÷", operation: "divide") {
                    insertOperation("divide ")
                }

                QuickActionButton(title: "^", operation: "power") {
                    insertOperation("power ")
                }

                QuickActionButton(title: "√", operation: "sqrt") {
                    insertOperation("sqrt ")
                }

                QuickActionButton(title: "sin", operation: "sin") {
                    insertOperation("sin ")
                }

                QuickActionButton(title: "cos", operation: "cos") {
                    insertOperation("cos ")
                }

                QuickActionButton(title: "π", operation: "pi") {
                    insertOperation("pi")
                }

                QuickActionButton(title: "$", operation: "last result") {
                    insertOperation("$ ")
                }

                QuickActionButton(title: "|", operation: "chain") {
                    insertOperation(" | ")
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
        }
        .background(Color(uiColor: .secondarySystemBackground))
    }

    private func insertOperation(_ text: String) {
        viewModel.inputText += text
        isInputFocused = true
    }
}

// MARK: - Session Tab

struct SessionTab: View {
    let session: Session
    let isActive: Bool
    let onTap: () -> Void
    let onClose: () -> Void
    let onRename: () -> Void

    var body: some View {
        HStack(spacing: 4) {
            // Session name
            Button(action: onTap) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(session.name)
                        .font(.system(.caption, design: .default))
                        .fontWeight(isActive ? .semibold : .regular)
                        .foregroundColor(isActive ? .primary : .secondary)
                        .lineLimit(1)

                    Text("\(session.entryCount) entries")
                        .font(.system(.caption2, design: .monospaced))
                        .foregroundColor(.secondary)
                }
                .padding(.leading, 8)
                .padding(.vertical, 6)
            }
            .buttonStyle(.plain)
            .contextMenu {
                Button("Rename", systemImage: "pencil") {
                    onRename()
                }
                Button("Close", systemImage: "xmark", role: .destructive) {
                    onClose()
                }
            }

            // Close button
            Button(action: onClose) {
                Image(systemName: "xmark")
                    .font(.system(size: 10, weight: .semibold))
                    .foregroundColor(.secondary)
                    .frame(width: 16, height: 16)
            }
            .buttonStyle(.plain)
            .padding(.trailing, 6)
        }
        .background(
            RoundedRectangle(cornerRadius: 6)
                .fill(isActive ? Color.blue.opacity(0.15) : Color(uiColor: .tertiarySystemBackground))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 6)
                .stroke(isActive ? Color.blue.opacity(0.5) : Color.clear, lineWidth: 1)
        )
    }
}

// MARK: - Quick Action Button

struct QuickActionButton: View {
    let title: String
    let operation: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 2) {
                Text(title)
                    .font(.system(.body, design: .monospaced))
                    .fontWeight(.semibold)

                Text(operation)
                    .font(.system(.caption2, design: .monospaced))
                    .foregroundColor(.secondary)
            }
            .frame(minWidth: 44)
            .padding(.horizontal, 8)
            .padding(.vertical, 6)
            .background(Color(uiColor: .tertiarySystemBackground))
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Preview

#Preview {
    CalculatorView()
        .modelContainer(for: HistoryEntry.self, inMemory: true)
}
