"""Matrix operations plugin for Math CLI using NumPy."""

from core.base_operations import MathOperation
import numpy as np
from typing import List, Union


class MatrixCreateOperation(MathOperation):
    """Create a matrix from a flat list of values."""

    name = "matrix"
    args = ["rows", "cols", "*values"]
    help = "Create matrix: matrix 2 2 1 2 3 4 creates [[1,2],[3,4]]"
    category = "matrix"

    @classmethod
    def execute(cls, rows: int, cols: int, *values) -> np.ndarray:
        """Create a matrix.

        Args:
            rows: Number of rows
            cols: Number of columns
            *values: Matrix values (row-major order)

        Returns:
            NumPy array

        Raises:
            ValueError: If wrong number of values provided
        """
        if len(values) != rows * cols:
            raise ValueError(f"Expected {rows * cols} values, got {len(values)}")

        return np.array(values).reshape(rows, cols)


class MatrixAddOperation(MathOperation):
    """Add two matrices (requires pre-created matrices - simplified version)."""

    name = "madd"
    args = ["*values"]
    help = "Add matrices: madd rows cols m1_vals... m2_vals..."
    category = "matrix"

    @classmethod
    def execute(cls, *values) -> str:
        """Add two matrices - simplified placeholder."""
        return "Matrix addition requires matrix variables (Phase 5.3)"


class MatrixMultiplyOperation(MathOperation):
    """Multiply two matrices."""

    name = "mmul"
    args = ["*values"]
    help = "Multiply matrices: mmul r1 c1 m1... r2 c2 m2..."
    category = "matrix"

    @classmethod
    def execute(cls, *values) -> np.ndarray:
        """Multiply two matrices.

        Format: mmul rows1 cols1 matrix1_values... rows2 cols2 matrix2_values...
        """
        if len(values) < 4:
            raise ValueError("Need at least rows1, cols1, rows2, cols2")

        # Parse first matrix
        rows1 = int(values[0])
        cols1 = int(values[1])
        size1 = rows1 * cols1
        m1_values = values[2:2+size1]

        if len(m1_values) != size1:
            raise ValueError(f"Expected {size1} values for first matrix")

        matrix1 = np.array(m1_values).reshape(rows1, cols1)

        # Parse second matrix
        offset = 2 + size1
        if len(values) < offset + 2:
            raise ValueError("Missing second matrix dimensions")

        rows2 = int(values[offset])
        cols2 = int(values[offset+1])
        size2 = rows2 * cols2
        m2_values = values[offset+2:offset+2+size2]

        if len(m2_values) != size2:
            raise ValueError(f"Expected {size2} values for second matrix")

        matrix2 = np.array(m2_values).reshape(rows2, cols2)

        # Check dimensions for multiplication
        if cols1 != rows2:
            raise ValueError(f"Cannot multiply {rows1}x{cols1} by {rows2}x{cols2} matrix")

        return np.matmul(matrix1, matrix2)


class MatrixTransposeOperation(MathOperation):
    """Transpose a matrix."""

    name = "transpose"
    args = ["rows", "cols", "*values"]
    help = "Transpose matrix: transpose 2 3 1 2 3 4 5 6"
    category = "matrix"

    @classmethod
    def execute(cls, rows: int, cols: int, *values) -> np.ndarray:
        """Transpose a matrix.

        Args:
            rows: Number of rows
            cols: Number of columns
            *values: Matrix values

        Returns:
            Transposed matrix
        """
        if len(values) != rows * cols:
            raise ValueError(f"Expected {rows * cols} values, got {len(values)}")

        matrix = np.array(values).reshape(rows, cols)
        return matrix.T


class MatrixDeterminantOperation(MathOperation):
    """Calculate determinant of a square matrix."""

    name = "det"
    args = ["n", "*values"]
    help = "Calculate determinant: det 2 1 2 3 4"
    category = "matrix"

    @classmethod
    def execute(cls, n: int, *values) -> float:
        """Calculate determinant.

        Args:
            n: Size of square matrix (n x n)
            *values: Matrix values

        Returns:
            Determinant value

        Raises:
            ValueError: If matrix is not square or wrong size
        """
        if len(values) != n * n:
            raise ValueError(f"Expected {n * n} values for {n}x{n} matrix, got {len(values)}")

        matrix = np.array(values).reshape(n, n)
        return float(np.linalg.det(matrix))


class MatrixInverseOperation(MathOperation):
    """Calculate inverse of a square matrix."""

    name = "inverse"
    args = ["n", "*values"]
    help = "Calculate matrix inverse: inverse 2 1 2 3 4"
    category = "matrix"

    @classmethod
    def execute(cls, n: int, *values) -> np.ndarray:
        """Calculate matrix inverse.

        Args:
            n: Size of square matrix (n x n)
            *values: Matrix values

        Returns:
            Inverse matrix

        Raises:
            ValueError: If matrix is singular or wrong size
        """
        if len(values) != n * n:
            raise ValueError(f"Expected {n * n} values for {n}x{n} matrix, got {len(values)}")

        matrix = np.array(values).reshape(n, n)

        try:
            return np.linalg.inv(matrix)
        except np.linalg.LinAlgError:
            raise ValueError("Matrix is singular and cannot be inverted")


class MatrixEigenvaluesOperation(MathOperation):
    """Calculate eigenvalues of a square matrix."""

    name = "eigenvalues"
    args = ["n", "*values"]
    help = "Calculate eigenvalues: eigenvalues 2 1 2 3 4"
    category = "matrix"

    @classmethod
    def execute(cls, n: int, *values) -> np.ndarray:
        """Calculate eigenvalues.

        Args:
            n: Size of square matrix (n x n)
            *values: Matrix values

        Returns:
            Array of eigenvalues
        """
        if len(values) != n * n:
            raise ValueError(f"Expected {n * n} values for {n}x{n} matrix, got {len(values)}")

        matrix = np.array(values).reshape(n, n)
        eigenvalues, _ = np.linalg.eig(matrix)
        return eigenvalues


class MatrixTraceOperation(MathOperation):
    """Calculate trace (sum of diagonal elements) of a square matrix."""

    name = "trace"
    args = ["n", "*values"]
    help = "Calculate trace: trace 2 1 2 3 4"
    category = "matrix"

    @classmethod
    def execute(cls, n: int, *values) -> float:
        """Calculate trace.

        Args:
            n: Size of square matrix (n x n)
            *values: Matrix values

        Returns:
            Trace (sum of diagonal)
        """
        if len(values) != n * n:
            raise ValueError(f"Expected {n * n} values for {n}x{n} matrix, got {len(values)}")

        matrix = np.array(values).reshape(n, n)
        return float(np.trace(matrix))


class MatrixRankOperation(MathOperation):
    """Calculate rank of a matrix."""

    name = "rank"
    args = ["rows", "cols", "*values"]
    help = "Calculate matrix rank: rank 2 3 1 2 3 4 5 6"
    category = "matrix"

    @classmethod
    def execute(cls, rows: int, cols: int, *values) -> int:
        """Calculate matrix rank.

        Args:
            rows: Number of rows
            cols: Number of columns
            *values: Matrix values

        Returns:
            Rank of the matrix
        """
        if len(values) != rows * cols:
            raise ValueError(f"Expected {rows * cols} values, got {len(values)}")

        matrix = np.array(values).reshape(rows, cols)
        return int(np.linalg.matrix_rank(matrix))


class IdentityMatrixOperation(MathOperation):
    """Create an identity matrix."""

    name = "identity"
    args = ["n"]
    help = "Create nxn identity matrix: identity 3"
    category = "matrix"

    @classmethod
    def execute(cls, n: int) -> np.ndarray:
        """Create identity matrix.

        Args:
            n: Size of identity matrix

        Returns:
            n x n identity matrix
        """
        return np.eye(n)


class ZeroMatrixOperation(MathOperation):
    """Create a zero matrix."""

    name = "zeros"
    args = ["rows", "cols"]
    help = "Create matrix of zeros: zeros 2 3"
    category = "matrix"

    @classmethod
    def execute(cls, rows: int, cols: int) -> np.ndarray:
        """Create zero matrix.

        Args:
            rows: Number of rows
            cols: Number of columns

        Returns:
            Matrix of zeros
        """
        return np.zeros((rows, cols))


class OnesMatrixOperation(MathOperation):
    """Create a matrix of ones."""

    name = "ones"
    args = ["rows", "cols"]
    help = "Create matrix of ones: ones 2 3"
    category = "matrix"

    @classmethod
    def execute(cls, rows: int, cols: int) -> np.ndarray:
        """Create ones matrix.

        Args:
            rows: Number of rows
            cols: Number of columns

        Returns:
            Matrix of ones
        """
        return np.ones((rows, cols))


# All operations are automatically discovered by the plugin manager
