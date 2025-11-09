//
//  HistoryView.swift
//  MathCLI
//
//  View for browsing calculation history organized by sessions
//

import SwiftUI
import SwiftData

struct HistoryView: View {
    @Environment(\.modelContext) private var modelContext
    @EnvironmentObject private var sessionManager: SessionManager
    @Query(sort: \Session.createdAt, order: .reverse) private var allSessions: [Session]
    @State private var selectedSession: Session?
    @State private var searchText = ""
    @State private var showBookmarksOnly = false

    var activeSessions: [Session] {
        allSessions.filter { $0.isActive }
    }

    var inactiveSessions: [Session] {
        allSessions.filter { !$0.isActive }
    }

    var body: some View {
        NavigationStack {
            List {
                // Active Sessions Section
                if !activeSessions.isEmpty {
                    Section("Active Session") {
                        ForEach(activeSessions) { session in
                            SessionRow(
                                session: session,
                                isActive: true,
                                onTap: {
                                    selectedSession = session
                                },
                                onReopen: nil
                            )
                        }
                    }
                }

                // Inactive Sessions Section
                if !inactiveSessions.isEmpty {
                    Section("Past Sessions") {
                        ForEach(inactiveSessions) { session in
                            SessionRow(
                                session: session,
                                isActive: false,
                                onTap: {
                                    selectedSession = session
                                },
                                onReopen: {
                                    reopenSession(session)
                                }
                            )
                        }
                        .onDelete(perform: deleteInactiveSessions)
                    }
                }

                // Empty state
                if allSessions.isEmpty {
                    ContentUnavailableView(
                        "No Sessions",
                        systemImage: "clock.badge.questionmark",
                        description: Text("Start calculating to create your first session")
                    )
                }
            }
            .navigationTitle("Sessions")
            .navigationDestination(item: $selectedSession) { session in
                SessionDetailView(session: session)
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button {
                            exportAllSessions()
                        } label: {
                            Label("Export All", systemImage: "square.and.arrow.up")
                        }

                        Divider()

                        Button(role: .destructive) {
                            clearInactiveSessions()
                        } label: {
                            Label("Clear Inactive Sessions", systemImage: "trash")
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
        }
    }

    private func reopenSession(_ session: Session) {
        sessionManager.switchToSession(session)
        // Show a confirmation
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)
    }

    private func deleteInactiveSessions(at offsets: IndexSet) {
        for index in offsets {
            let session = inactiveSessions[index]
            sessionManager.deleteSession(session)
        }
    }

    private func clearInactiveSessions() {
        for session in inactiveSessions {
            sessionManager.deleteSession(session)
        }
    }

    private func exportAllSessions() {
        // TODO: Implement export functionality
        print("Export all sessions")
    }
}

// MARK: - Session Row

struct SessionRow: View {
    let session: Session
    let isActive: Bool
    let onTap: () -> Void
    let onReopen: (() -> Void)?

    var body: some View {
        Button(action: onTap) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text(session.name)
                            .font(.headline)
                            .foregroundColor(.primary)

                        if isActive {
                            Image(systemName: "circle.fill")
                                .font(.system(size: 8))
                                .foregroundColor(.green)
                        }
                    }

                    Text(session.createdAt, style: .date)
                        .font(.caption)
                        .foregroundColor(.secondary)

                    Text("\(session.entryCount) calculation\(session.entryCount == 1 ? "" : "s")")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                if !isActive, let onReopen = onReopen {
                    Button {
                        onReopen()
                    } label: {
                        Text("Reopen")
                            .font(.subheadline)
                            .fontWeight(.semibold)
                            .foregroundColor(.white)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 6)
                            .background(Color.blue)
                            .cornerRadius(8)
                    }
                    .buttonStyle(.plain)
                }

                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Session Detail View

struct SessionDetailView: View {
    @Environment(\.modelContext) private var modelContext
    let session: Session
    @State private var searchText = ""
    @State private var showBookmarksOnly = false

    var filteredEntries: [HistoryEntry] {
        var entries = session.entries.sorted(by: { $0.timestamp > $1.timestamp })

        if showBookmarksOnly {
            entries = entries.filter { $0.isBookmarked }
        }

        if !searchText.isEmpty {
            entries = entries.filter { entry in
                entry.command.localizedCaseInsensitiveContains(searchText) ||
                entry.result.localizedCaseInsensitiveContains(searchText)
            }
        }

        return entries
    }

    var body: some View {
        List {
            ForEach(filteredEntries) { entry in
                HistoryEntryRow(entry: entry)
                    .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                        Button(role: .destructive) {
                            deleteEntry(entry)
                        } label: {
                            Label("Delete", systemImage: "trash")
                        }
                    }
                    .swipeActions(edge: .leading) {
                        Button {
                            toggleBookmark(entry)
                        } label: {
                            Label(
                                entry.isBookmarked ? "Remove Bookmark" : "Bookmark",
                                systemImage: entry.isBookmarked ? "bookmark.fill" : "bookmark"
                            )
                        }
                        .tint(.orange)
                    }
                    .contextMenu {
                        Button {
                            copyToClipboard(entry)
                        } label: {
                            Label("Copy Calculation", systemImage: "doc.on.doc")
                        }

                        Button {
                            copyResultToClipboard(entry)
                        } label: {
                            Label("Copy Result", systemImage: "number")
                        }
                    }
            }

            if filteredEntries.isEmpty {
                ContentUnavailableView(
                    searchText.isEmpty ? "No Calculations" : "No Results",
                    systemImage: searchText.isEmpty ? "function" : "magnifyingglass",
                    description: Text(searchText.isEmpty ? "This session has no calculations yet" : "Try a different search term")
                )
            }
        }
        .searchable(text: $searchText, prompt: "Search calculations")
        .navigationTitle(session.name)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Menu {
                    Button {
                        showBookmarksOnly.toggle()
                    } label: {
                        Label(
                            showBookmarksOnly ? "Show All" : "Show Bookmarks",
                            systemImage: showBookmarksOnly ? "list.bullet" : "bookmark"
                        )
                    }

                    Divider()

                    Button {
                        exportSession()
                    } label: {
                        Label("Export Session", systemImage: "square.and.arrow.up")
                    }

                    Button(role: .destructive) {
                        clearSessionHistory()
                    } label: {
                        Label("Clear Session History", systemImage: "trash")
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
        }
    }

    private func deleteEntry(_ entry: HistoryEntry) {
        modelContext.delete(entry)
    }

    private func toggleBookmark(_ entry: HistoryEntry) {
        entry.isBookmarked.toggle()
    }

    private func clearSessionHistory() {
        for entry in session.entries {
            modelContext.delete(entry)
        }
    }

    private func exportSession() {
        // TODO: Implement export functionality
        print("Export session: \(session.name)")
    }

    private func copyToClipboard(_ entry: HistoryEntry) {
        UIPasteboard.general.string = entry.command
    }

    private func copyResultToClipboard(_ entry: HistoryEntry) {
        UIPasteboard.general.string = entry.result
    }
}

struct HistoryEntryRow: View {
    let entry: HistoryEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                if entry.isBookmarked {
                    Image(systemName: "bookmark.fill")
                        .foregroundColor(.orange)
                        .font(.caption)
                }

                Text(entry.timestamp, style: .time)
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Text(entry.timestamp, style: .date)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Text(entry.command)
                .font(.system(.body, design: .monospaced))
                .foregroundColor(.cyan)

            Text(entry.result)
                .font(.system(.body, design: .monospaced))
                .foregroundColor(.green)
                .lineLimit(3)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    HistoryView()
        .modelContainer(for: HistoryEntry.self, inMemory: true)
}
