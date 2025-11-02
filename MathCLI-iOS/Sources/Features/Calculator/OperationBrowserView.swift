//
//  OperationBrowserView.swift
//  MathCLI
//
//  Browse all available operations by category
//

import SwiftUI

struct OperationBrowserView: View {
    @State private var searchText = ""
    @State private var selectedCategory: OperationCategory?

    private let registry = OperationRegistry.shared

    var filteredCategories: [OperationCategory] {
        registry.getAvailableCategories()
    }

    var body: some View {
        NavigationStack {
            List {
                ForEach(filteredCategories, id: \.self) { category in
                    NavigationLink {
                        CategoryDetailView(category: category)
                    } label: {
                        CategoryRow(category: category)
                    }
                }
            }
            .searchable(text: $searchText, prompt: "Search operations")
            .navigationTitle("Operations")
        }
    }
}

struct CategoryRow: View {
    let category: OperationCategory

    private let registry = OperationRegistry.shared

    var operationCount: Int {
        registry.getOperations(in: category).count
    }

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(category.rawValue)
                    .font(.headline)

                Text("\(operationCount) operations")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            Image(systemName: categoryIcon)
                .foregroundColor(.blue)
                .font(.title2)
        }
        .padding(.vertical, 4)
    }

    private var categoryIcon: String {
        switch category {
        case .basicArithmetic: return "plus.forwardslash.minus"
        case .trigonometry: return "waveform"
        case .advancedMath: return "function"
        case .statistics: return "chart.bar"
        case .complexNumbers: return "number.circle"
        case .matrix: return "grid"
        case .calculus: return "infinity"
        case .numberTheory: return "number.square"
        case .combinatorics: return "shuffle"
        case .geometry: return "triangle"
        case .constants: return "c.circle"
        case .conversions: return "arrow.left.arrow.right"
        case .variables: return "x.squareroot"
        case .controlFlow: return "arrow.triangle.branch"
        case .userFunctions: return "curlybraces"
        case .scripts: return "doc.text"
        case .dataAnalysis: return "tablecells"
        case .dataTransform: return "arrow.up.arrow.down"
        case .plotting: return "chart.xyaxis.line"
        case .export: return "square.and.arrow.up"
        }
    }
}

struct CategoryDetailView: View {
    let category: OperationCategory

    private let registry = OperationRegistry.shared

    var operations: [(String, any MathOperation.Type)] {
        registry.getOperations(in: category)
    }

    var body: some View {
        List {
            ForEach(operations, id: \.0) { operation in
                OperationDetailRow(
                    name: operation.0,
                    operationType: operation.1
                )
            }
        }
        .navigationTitle(category.rawValue)
    }
}

struct OperationDetailRow: View {
    let name: String
    let operationType: any MathOperation.Type

    @State private var showDetails = false

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(name)
                    .font(.system(.body, design: .monospaced))
                    .fontWeight(.semibold)

                Spacer()

                Button {
                    showDetails.toggle()
                } label: {
                    Image(systemName: showDetails ? "chevron.up" : "chevron.down")
                        .foregroundColor(.blue)
                }
            }

            if showDetails {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Help:")
                        .font(.caption)
                        .foregroundColor(.secondary)

                    Text(operationType.help)
                        .font(.system(.caption, design: .monospaced))

                    if !operationType.arguments.isEmpty {
                        Text("Arguments:")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .padding(.top, 4)

                        Text(operationType.arguments.joined(separator: ", "))
                            .font(.system(.caption, design: .monospaced))
                    }

                    if operationType.isVariadic {
                        Text("Accepts variable number of arguments")
                            .font(.caption)
                            .foregroundColor(.orange)
                            .padding(.top, 4)
                    }
                }
                .padding(.leading, 8)
                .padding(.vertical, 4)
            }
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    OperationBrowserView()
}
