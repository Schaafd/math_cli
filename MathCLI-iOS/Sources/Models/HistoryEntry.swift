//
//  HistoryEntry.swift
//  MathCLI
//
//  SwiftData model for calculation history
//

import Foundation
import SwiftData

@Model
final class HistoryEntry {
    @Attribute(.unique) var id: UUID
    var command: String
    var result: String
    var timestamp: Date
    var isBookmarked: Bool
    var bookmarkName: String?

    init(command: String, result: String, timestamp: Date = Date(), isBookmarked: Bool = false, bookmarkName: String? = nil) {
        self.id = UUID()
        self.command = command
        self.result = result
        self.timestamp = timestamp
        self.isBookmarked = isBookmarked
        self.bookmarkName = bookmarkName
    }

    var displayText: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return "[\(formatter.string(from: timestamp))] \(command) = \(result)"
    }
}

// MARK: - History Manager

@MainActor
class HistoryManager: ObservableObject {
    @Published var entries: [HistoryEntry] = []

    private let modelContext: ModelContext
    private let maxEntries: Int

    init(modelContext: ModelContext, maxEntries: Int = 1000) {
        self.modelContext = modelContext
        self.maxEntries = maxEntries
        loadHistory()
    }

    func addEntry(command: String, result: String) {
        let entry = HistoryEntry(command: command, result: result)
        modelContext.insert(entry)
        entries.insert(entry, at: 0)

        // Trim history if it exceeds max
        if entries.count > maxEntries {
            let toRemove = entries.suffix(entries.count - maxEntries)
            for entry in toRemove {
                modelContext.delete(entry)
            }
            entries = Array(entries.prefix(maxEntries))
        }

        saveHistory()
    }

    func bookmark(entry: HistoryEntry, name: String) {
        entry.isBookmarked = true
        entry.bookmarkName = name
        saveHistory()
    }

    func removeBookmark(entry: HistoryEntry) {
        entry.isBookmarked = false
        entry.bookmarkName = nil
        saveHistory()
    }

    func deleteEntry(_ entry: HistoryEntry) {
        if let index = entries.firstIndex(where: { $0.id == entry.id }) {
            entries.remove(at: index)
        }
        modelContext.delete(entry)
        saveHistory()
    }

    func clearHistory() {
        for entry in entries {
            modelContext.delete(entry)
        }
        entries.removeAll()
        saveHistory()
    }

    func getBookmarks() -> [HistoryEntry] {
        return entries.filter { $0.isBookmarked }
    }

    func searchHistory(query: String) -> [HistoryEntry] {
        let lowercaseQuery = query.lowercased()
        return entries.filter {
            $0.command.lowercased().contains(lowercaseQuery) ||
            $0.result.lowercased().contains(lowercaseQuery)
        }
    }

    private func loadHistory() {
        let descriptor = FetchDescriptor<HistoryEntry>(
            sortBy: [SortDescriptor(\.timestamp, order: .reverse)]
        )

        do {
            entries = try modelContext.fetch(descriptor)
        } catch {
            print("Failed to load history: \(error)")
            entries = []
        }
    }

    private func saveHistory() {
        do {
            try modelContext.save()
        } catch {
            print("Failed to save history: \(error)")
        }
    }

    // Export history to various formats
    func exportToJSON() -> String {
        let data = entries.map { entry in
            [
                "command": entry.command,
                "result": entry.result,
                "timestamp": ISO8601DateFormatter().string(from: entry.timestamp),
                "bookmarked": entry.isBookmarked
            ]
        }

        guard let jsonData = try? JSONSerialization.data(withJSONObject: data, options: .prettyPrinted),
              let jsonString = String(data: jsonData, encoding: .utf8) else {
            return "[]"
        }

        return jsonString
    }

    func exportToMarkdown() -> String {
        var markdown = "# Math CLI History\n\n"
        markdown += "Exported: \(Date().formatted())\n\n"

        for entry in entries {
            markdown += "## \(entry.timestamp.formatted())\n"
            markdown += "```\n"
            markdown += "\(entry.command)\n"
            markdown += "```\n"
            markdown += "**Result:** `\(entry.result)`\n\n"
        }

        return markdown
    }
}
