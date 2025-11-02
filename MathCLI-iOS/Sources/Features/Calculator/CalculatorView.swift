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
    @StateObject private var viewModel: CalculatorViewModel
    @FocusState private var isInputFocused: Bool
    @State private var scrollProxy: ScrollViewProxy?

    init() {
        _viewModel = StateObject(wrappedValue: CalculatorViewModel())
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
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
                    }
                    .onChange(of: viewModel.inputText) { _, _ in
                        viewModel.updateSuggestions()
                    }

                // Execute button
                Button {
                    viewModel.executeCommand()
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
