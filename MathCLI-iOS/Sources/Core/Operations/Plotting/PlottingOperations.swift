//
//  PlottingOperations.swift
//  MathCLI
//
//  Plotting operations - prepare chart data for Swift Charts (8 operations)
//

import Foundation

// Note: These operations prepare data for plotting
// Actual visualization will be handled by Swift Charts in the UI layer

// MARK: - Plot Histogram

struct PlotHistOperation: MathOperation {
    static var name = "plot_hist"
    static var arguments = ["bins", "values..."]
    static var help = "Prepare histogram data: plot_hist bins val1 val2 val3 ..."
    static var category = OperationCategory.plotting
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let bins = try parseInt(args[0], argumentName: "bins")
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        guard !values.isEmpty && bins > 0 else {
            throw OperationError.invalidValue("Need values and positive bins")
        }

        let min = values.min()!
        let max = values.max()!
        let binWidth = (max - min) / Double(bins)

        var histogram = Array(repeating: 0, count: bins)

        for value in values {
            let binIndex = min(Int((value - min) / binWidth), bins - 1)
            histogram[binIndex] += 1
        }

        return .string("Histogram: \(bins) bins, range [\(min), \(max)], counts: \(histogram)")
    }
}

// MARK: - Plot Box

struct PlotBoxOperation: MathOperation {
    static var name = "plot_box"
    static var arguments = ["values..."]
    static var help = "Prepare box plot data: plot_box val1 val2 val3 ..."
    static var category = OperationCategory.plotting
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        let sorted = values.sorted()
        let count = sorted.count

        let min = sorted.first!
        let max = sorted.last!
        let q1 = sorted[count / 4]
        let median = count % 2 == 0 ?
            (sorted[count / 2 - 1] + sorted[count / 2]) / 2 :
            sorted[count / 2]
        let q3 = sorted[3 * count / 4]

        return .string("Box Plot: Min=\(min), Q1=\(q1), Median=\(median), Q3=\(q3), Max=\(max)")
    }
}

// MARK: - Plot Scatter

struct PlotScatterOperation: MathOperation {
    static var name = "plot_scatter"
    static var arguments = ["x_values", "y_values"]
    static var help = "Prepare scatter plot: plot_scatter x_vals y_vals"
    static var category = OperationCategory.plotting

    static func execute(args: [Any]) throws -> OperationResult {
        let xValues = try parseDoubleArray(args[0], argumentName: "x_values")
        let yValues = try parseDoubleArray(args[1], argumentName: "y_values")

        guard xValues.count == yValues.count else {
            throw OperationError.invalidValue("X and Y arrays must have same length")
        }

        let points = zip(xValues, yValues).map { "(\($0), \($1))" }.joined(separator: ", ")
        return .string("Scatter Plot: \(xValues.count) points: \(points)")
    }
}

// MARK: - Plot Heatmap

struct PlotHeatmapOperation: MathOperation {
    static var name = "plot_heatmap"
    static var arguments = ["matrix"]
    static var help = "Prepare heatmap from matrix: plot_heatmap matrix"
    static var category = OperationCategory.plotting

    static func execute(args: [Any]) throws -> OperationResult {
        // Parse matrix
        let matrixStr = args[0] as? String ?? String(describing: args[0])

        return .string("Heatmap prepared from matrix: \(matrixStr)")
    }
}

// MARK: - Plot (Generic)

struct PlotOperation: MathOperation {
    static var name = "plot"
    static var arguments = ["values..."]
    static var help = "Generic plot of values: plot val1 val2 val3 ..."
    static var category = OperationCategory.plotting
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        return .string("Plot: \(values.count) data points")
    }
}

// MARK: - Plot Line

struct PlotLineOperation: MathOperation {
    static var name = "plot_line"
    static var arguments = ["values..."]
    static var help = "Prepare line plot: plot_line val1 val2 val3 ..."
    static var category: OperationCategory = .plotting
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        let min = values.min()!
        let max = values.max()!
        let mean = values.reduce(0, +) / Double(values.count)

        return .string("Line Plot: \(values.count) points, range [\(min), \(max)], mean=\(mean)")
    }
}

// MARK: - Plot Bar

struct PlotBarOperation: MathOperation {
    static var name = "plot_bar"
    static var arguments = ["values..."]
    static var help = "Prepare bar chart: plot_bar val1 val2 val3 ..."
    static var category = OperationCategory.plotting
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        return .string("Bar Chart: \(values.count) bars")
    }
}

// MARK: - Plot Data

struct PlotDataOperation: MathOperation {
    static var name = "plot_data"
    static var arguments = ["data_source", "x_column", "y_column"]
    static var help = "Plot data from source: plot_data source x_col y_col"
    static var category = OperationCategory.plotting

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let dataSource = args[0] as? String ?? String(describing: args[0])
        let xCol = args.count > 1 ? (args[1] as? String ?? "x") : "x"
        let yCol = args.count > 2 ? (args[2] as? String ?? "y") : "y"

        return .string("Plot from '\(dataSource)': x=\(xCol), y=\(yCol)")
    }
}
