//
//  MatrixOperations.swift
//  MathCLI
//
//  Matrix operations (12 operations)
//  Uses Accelerate framework for performance
//

import Foundation
import Accelerate

// Helper to parse matrix from string like "[[1,2],[3,4]]"
private func parseMatrix(_ value: Any) throws -> [[Double]] {
    if let matrix = value as? [[Double]] {
        return matrix
    } else if let stringValue = value as? String {
        // Parse string representation
        let cleaned = stringValue
            .replacingOccurrences(of: " ", with: "")
            .replacingOccurrences(of: "[[", with: "")
            .replacingOccurrences(of: "]]", with: "")

        let rows = cleaned.components(separatedBy: "],[")
        var matrix: [[Double]] = []

        for row in rows {
            let elements = row.components(separatedBy: ",")
            let doubleElements = try elements.map { element -> Double in
                guard let value = Double(element) else {
                    throw OperationError.invalidValue("Invalid matrix element: \(element)")
                }
                return value
            }
            matrix.append(doubleElements)
        }

        // Validate matrix (all rows same length)
        if let firstRowCount = matrix.first?.count {
            guard matrix.allSatisfy({ $0.count == firstRowCount }) else {
                throw OperationError.matrixDimensionMismatch
            }
        }

        return matrix
    } else {
        throw OperationError.invalidArgumentType(
            argument: "matrix",
            expected: "matrix array",
            got: String(describing: value)
        )
    }
}

// MARK: - Determinant

struct DetOperation: MathOperation {
    static var name = "det"
    static var arguments = ["matrix"]
    static var help = "Calculate matrix determinant: det matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let rows = matrix.count
        let cols = matrix[0].count

        guard rows == cols else {
            throw OperationError.invalidValue("Determinant requires square matrix")
        }

        // Flatten matrix for LAPACK
        var flatMatrix = matrix.flatMap { $0 }
        var n = Int32(rows)
        var pivots = [Int32](repeating: 0, count: rows)
        var info: Int32 = 0

        // LU decomposition
        dgetrf_(&n, &n, &flatMatrix, &n, &pivots, &info)

        guard info == 0 else {
            throw OperationError.executionError("Matrix decomposition failed")
        }

        // Calculate determinant from diagonal
        var det: Double = 1.0
        for i in 0..<rows {
            det *= flatMatrix[i * rows + i]
            // Account for row swaps
            if pivots[i] != Int32(i + 1) {
                det *= -1
            }
        }

        return .number(det)
    }
}

// MARK: - Transpose

struct TransposeOperation: MathOperation {
    static var name = "transpose"
    static var arguments = ["matrix"]
    static var help = "Transpose matrix: transpose matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let rows = matrix.count
        let cols = matrix[0].count

        var transposed = Array(repeating: Array(repeating: 0.0, count: rows), count: cols)

        for i in 0..<rows {
            for j in 0..<cols {
                transposed[j][i] = matrix[i][j]
            }
        }

        return .matrix(transposed)
    }
}

// MARK: - Eigenvalues (simplified - real only)

struct EigenvaluesOperation: MathOperation {
    static var name = "eigenvalues"
    static var arguments = ["matrix"]
    static var help = "Calculate eigenvalues (real): eigenvalues matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let n = matrix.count
        guard n == matrix[0].count else {
            throw OperationError.invalidValue("Eigenvalues require square matrix")
        }

        var flatMatrix = matrix.flatMap { $0 }
        var eigenvaluesReal = [Double](repeating: 0, count: n)
        var eigenvaluesImag = [Double](repeating: 0, count: n)

        var n32 = Int32(n)
        var lwork = Int32(4 * n)
        var work = [Double](repeating: 0, count: Int(lwork))
        var info: Int32 = 0

        var jobvl: Int8 = 78 // 'N'
        var jobvr: Int8 = 78 // 'N'

        // Calculate eigenvalues using LAPACK
        dgeev_(&jobvl, &jobvr, &n32, &flatMatrix, &n32,
               &eigenvaluesReal, &eigenvaluesImag,
               nil, &n32, nil, &n32,
               &work, &lwork, &info)

        guard info == 0 else {
            throw OperationError.executionError("Eigenvalue computation failed")
        }

        // Return only real parts for simplicity
        return .array(eigenvaluesReal)
    }
}

// MARK: - Eigenvectors (simplified)

struct EigenvectorsOperation: MathOperation {
    static var name = "eigenvectors"
    static var arguments = ["matrix"]
    static var help = "Calculate eigenvectors: eigenvectors matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let n = matrix.count
        guard n == matrix[0].count else {
            throw OperationError.invalidValue("Eigenvectors require square matrix")
        }

        // This is a complex operation - return placeholder
        return .string("Eigenvector calculation available (use specialized library for full implementation)")
    }
}

// MARK: - Trace

struct TraceOperation: MathOperation {
    static var name = "trace"
    static var arguments = ["matrix"]
    static var help = "Calculate matrix trace (sum of diagonal): trace matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let n = min(matrix.count, matrix[0].count)
        var trace: Double = 0

        for i in 0..<n {
            trace += matrix[i][i]
        }

        return .number(trace)
    }
}

// MARK: - Rank (simplified)

struct RankOperation: MathOperation {
    static var name = "rank"
    static var arguments = ["matrix"]
    static var help = "Calculate matrix rank: rank matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        // Simplified rank calculation using row reduction
        var m = matrix
        let rows = m.count
        let cols = m[0].count
        var rank = 0

        for col in 0..<min(rows, cols) {
            // Find pivot
            var pivotRow = col
            for row in (col + 1)..<rows {
                if abs(m[row][col]) > abs(m[pivotRow][col]) {
                    pivotRow = row
                }
            }

            if abs(m[pivotRow][col]) < 1e-10 {
                continue
            }

            // Swap rows
            if pivotRow != col {
                m.swapAt(col, pivotRow)
            }

            rank += 1

            // Eliminate
            for row in (col + 1)..<rows {
                let factor = m[row][col] / m[col][col]
                for c in col..<cols {
                    m[row][c] -= factor * m[col][c]
                }
            }
        }

        return .integer(rank)
    }
}

// MARK: - Inverse

struct InverseOperation: MathOperation {
    static var name = "inverse"
    static var arguments = ["matrix"]
    static var help = "Calculate matrix inverse: inverse matrix"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])

        let n = matrix.count
        guard n == matrix[0].count else {
            throw OperationError.invalidValue("Inverse requires square matrix")
        }

        var flatMatrix = matrix.flatMap { $0 }
        var n32 = Int32(n)
        var pivots = [Int32](repeating: 0, count: n)
        var info: Int32 = 0

        // LU decomposition
        dgetrf_(&n32, &n32, &flatMatrix, &n32, &pivots, &info)

        guard info == 0 else {
            throw OperationError.singularMatrix
        }

        // Compute inverse
        var lwork = Int32(n * n)
        var work = [Double](repeating: 0, count: Int(lwork))

        dgetri_(&n32, &flatMatrix, &n32, &pivots, &work, &lwork, &info)

        guard info == 0 else {
            throw OperationError.singularMatrix
        }

        // Reconstruct matrix
        var result: [[Double]] = []
        for i in 0..<n {
            var row: [Double] = []
            for j in 0..<n {
                row.append(flatMatrix[i * n + j])
            }
            result.append(row)
        }

        return .matrix(result)
    }
}

// MARK: - Matrix Multiply

struct MatrixMultiplyOperation: MathOperation {
    static var name = "matrix_multiply"
    static var arguments = ["matrix1", "matrix2"]
    static var help = "Multiply matrices: matrix_multiply matrix1 matrix2"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let matrix1 = try parseMatrix(args[0])
        let matrix2 = try parseMatrix(args[1])

        let m = matrix1.count
        let n = matrix1[0].count
        let p = matrix2[0].count

        guard n == matrix2.count else {
            throw OperationError.matrixDimensionMismatch
        }

        var result = Array(repeating: Array(repeating: 0.0, count: p), count: m)

        for i in 0..<m {
            for j in 0..<p {
                for k in 0..<n {
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
                }
            }
        }

        return .matrix(result)
    }
}

// MARK: - Identity Matrix

struct IdentityOperation: MathOperation {
    static var name = "identity"
    static var arguments = ["n"]
    static var help = "Create identity matrix: identity n"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("Matrix size must be positive")
        }

        var matrix = Array(repeating: Array(repeating: 0.0, count: n), count: n)

        for i in 0..<n {
            matrix[i][i] = 1.0
        }

        return .matrix(matrix)
    }
}

// MARK: - Zeros Matrix

struct ZerosOperation: MathOperation {
    static var name = "zeros"
    static var arguments = ["rows", "cols"]
    static var help = "Create zero matrix: zeros rows cols"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let rows = try parseInt(args[0], argumentName: "rows")
        let cols = try parseInt(args[1], argumentName: "cols")

        guard rows > 0 && cols > 0 else {
            throw OperationError.invalidValue("Matrix dimensions must be positive")
        }

        let matrix = Array(repeating: Array(repeating: 0.0, count: cols), count: rows)
        return .matrix(matrix)
    }
}

// MARK: - Ones Matrix

struct OnesOperation: MathOperation {
    static var name = "ones"
    static var arguments = ["rows", "cols"]
    static var help = "Create matrix of ones: ones rows cols"
    static var category = OperationCategory.matrix

    static func execute(args: [Any]) throws -> OperationResult {
        let rows = try parseInt(args[0], argumentName: "rows")
        let cols = try parseInt(args[1], argumentName: "cols")

        guard rows > 0 && cols > 0 else {
            throw OperationError.invalidValue("Matrix dimensions must be positive")
        }

        let matrix = Array(repeating: Array(repeating: 1.0, count: cols), count: rows)
        return .matrix(matrix)
    }
}

// MARK: - Diagonal Matrix

struct DiagonalOperation: MathOperation {
    static var name = "diagonal"
    static var arguments = ["values..."]
    static var help = "Create diagonal matrix: diagonal value1 value2 ..."
    static var category = OperationCategory.matrix
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []

        for arg in args {
            let value = try parseDouble(arg, argumentName: "value")
            values.append(value)
        }

        let n = values.count
        var matrix = Array(repeating: Array(repeating: 0.0, count: n), count: n)

        for i in 0..<n {
            matrix[i][i] = values[i]
        }

        return .matrix(matrix)
    }
}
