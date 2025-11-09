//
//  Session.swift
//  MathCLI
//
//  SwiftData model for calculator sessions
//

import Foundation
import SwiftData

@Model
final class Session {
    @Attribute(.unique) var id: UUID
    var name: String
    var createdAt: Date
    var isActive: Bool

    @Relationship(deleteRule: .cascade, inverse: \HistoryEntry.session)
    var entries: [HistoryEntry] = []

    init(name: String? = nil, createdAt: Date = Date(), isActive: Bool = false) {
        self.id = UUID()
        self.createdAt = createdAt
        self.isActive = isActive

        // Generate unique name if not provided
        if let name = name {
            self.name = name
        } else {
            let formatter = DateFormatter()
            formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
            self.name = "Session \(formatter.string(from: createdAt))"
        }
    }

    var displayName: String {
        return name
    }

    var entryCount: Int {
        return entries.count
    }
}

// MARK: - Session Manager

@MainActor
class SessionManager: ObservableObject {
    @Published var sessions: [Session] = []
    @Published var activeSession: Session?

    private let modelContext: ModelContext

    init(modelContext: ModelContext) {
        self.modelContext = modelContext
        loadSessions()

        // Create initial session if none exist
        if sessions.isEmpty {
            createSession()
        }

        // Set active session to the most recent one or first available
        if activeSession == nil {
            activeSession = sessions.first(where: { $0.isActive }) ?? sessions.first
            activeSession?.isActive = true
            saveContext()
        }
    }

    func createSession(name: String? = nil) {
        // Deactivate current session
        if let current = activeSession {
            current.isActive = false
        }

        // Create new session
        let session = Session(name: name, isActive: true)
        modelContext.insert(session)
        sessions.insert(session, at: 0)
        activeSession = session

        saveContext()
    }

    func switchToSession(_ session: Session) {
        // Don't switch if already active
        if activeSession?.id == session.id {
            return
        }

        // Deactivate all sessions
        for s in sessions {
            s.isActive = false
        }

        // Activate selected session
        session.isActive = true
        activeSession = session

        // Force UI update
        objectWillChange.send()

        saveContext()
    }

    func renameSession(_ session: Session, newName: String) {
        session.name = newName
        saveContext()
    }

    func deleteSession(_ session: Session) {
        // Prevent deleting the last session
        guard sessions.count > 1 else { return }

        // If deleting active session, switch to another
        if session == activeSession {
            if let index = sessions.firstIndex(where: { $0.id == session.id }) {
                let newIndex = index > 0 ? index - 1 : 1
                switchToSession(sessions[newIndex])
            }
        }

        // Remove from array and context
        if let index = sessions.firstIndex(where: { $0.id == session.id }) {
            sessions.remove(at: index)
        }
        modelContext.delete(session)

        saveContext()
    }

    func getSessionHistory(_ session: Session) -> [HistoryEntry] {
        return session.entries.sorted(by: { $0.timestamp > $1.timestamp })
    }

    private func loadSessions() {
        let descriptor = FetchDescriptor<Session>(
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )

        do {
            sessions = try modelContext.fetch(descriptor)
            activeSession = sessions.first(where: { $0.isActive })
        } catch {
            print("Failed to load sessions: \(error)")
            sessions = []
        }
    }

    private func saveContext() {
        do {
            try modelContext.save()
        } catch {
            print("Failed to save context: \(error)")
        }
    }
}
