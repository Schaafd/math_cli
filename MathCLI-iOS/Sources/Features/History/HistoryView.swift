//
//  HistoryView.swift
//  MathCLI
//
//  View for browsing calculation history
//

import SwiftUI
import SwiftData

struct HistoryView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \HistoryEntry.timestamp, order: .reverse) private var historyEntries: [HistoryEntry]
    @State private var searchText = ""
    @State private var showBookmarksOnly = false

    var filteredEntries: [HistoryEntry] {
        var entries = historyEntries

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
        NavigationStack {
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
                }
            }
            .searchable(text: $searchText, prompt: "Search history")
            .navigationTitle("History")
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

                        Button(role: .destructive) {
                            clearHistory()
                        } label: {
                            Label("Clear History", systemImage: "trash")
                        }

                        Button {
                            exportHistory()
                        } label: {
                            Label("Export", systemImage: "square.and.arrow.up")
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
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

    private func clearHistory() {
        for entry in historyEntries {
            modelContext.delete(entry)
        }
    }

    private func exportHistory() {
        // TODO: Implement export functionality
        print("Export history")
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
