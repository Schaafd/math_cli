"""Tests for Phase 5.1: Advanced Mathematical Operations."""

import pytest
import numpy as np
from core.plugin_manager import PluginManager


class TestComplexNumbers:
    """Test complex number operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_complex_creation(self):
        """Test creating complex numbers."""
        result = self.manager.execute_operation('complex', 3, 4)
        assert result == complex(3, 4)

    def test_complex_addition(self):
        """Test adding complex numbers."""
        result = self.manager.execute_operation('cadd', 3, 4, 1, 2)
        assert result == complex(4, 6)

    def test_complex_multiplication(self):
        """Test multiplying complex numbers."""
        result = self.manager.execute_operation('cmul', 3, 4, 1, 2)
        expected = complex(3, 4) * complex(1, 2)
        assert result == expected

    def test_complex_magnitude(self):
        """Test magnitude calculation."""
        result = self.manager.execute_operation('magnitude', 3, 4)
        assert result == 5.0

    def test_complex_phase(self):
        """Test phase calculation."""
        result = self.manager.execute_operation('phase', 1, 0)
        assert abs(result) < 1e-10  # Phase of 1+0i is 0

    def test_complex_conjugate(self):
        """Test conjugate."""
        result = self.manager.execute_operation('conjugate', 3, 4)
        assert result == complex(3, -4)

    def test_complex_division_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError):
            self.manager.execute_operation('cdiv', 1, 1, 0, 0)

    def test_complex_sqrt(self):
        """Test complex square root."""
        result = self.manager.execute_operation('csqrt', -1, 0)
        # sqrt(-1) = i = 0+1j
        assert abs(result.real) < 1e-10
        assert abs(result.imag - 1.0) < 1e-10


class TestMatrixOperations:
    """Test matrix operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_matrix_creation(self):
        """Test creating a matrix."""
        result = self.manager.execute_operation('matrix', 2, 2, 1, 2, 3, 4)
        expected = np.array([[1, 2], [3, 4]])
        assert np.array_equal(result, expected)

    def test_matrix_transpose(self):
        """Test matrix transpose."""
        result = self.manager.execute_operation('transpose', 2, 3, 1, 2, 3, 4, 5, 6)
        expected = np.array([[1, 4], [2, 5], [3, 6]])
        assert np.array_equal(result, expected)

    def test_matrix_determinant(self):
        """Test determinant calculation."""
        result = self.manager.execute_operation('det', 2, 1, 2, 3, 4)
        expected = -2.0  # det([[1,2],[3,4]]) = 1*4 - 2*3 = -2
        assert abs(result - expected) < 1e-10

    def test_identity_matrix(self):
        """Test identity matrix creation."""
        result = self.manager.execute_operation('identity', 3)
        expected = np.eye(3)
        assert np.array_equal(result, expected)

    def test_zero_matrix(self):
        """Test zero matrix creation."""
        result = self.manager.execute_operation('zeros', 2, 3)
        expected = np.zeros((2, 3))
        assert np.array_equal(result, expected)

    def test_ones_matrix(self):
        """Test ones matrix creation."""
        result = self.manager.execute_operation('ones', 2, 2)
        expected = np.ones((2, 2))
        assert np.array_equal(result, expected)

    def test_matrix_trace(self):
        """Test trace calculation."""
        result = self.manager.execute_operation('trace', 2, 1, 2, 3, 4)
        expected = 5.0  # trace([[1,2],[3,4]]) = 1 + 4 = 5
        assert abs(result - expected) < 1e-10

    def test_matrix_rank(self):
        """Test rank calculation."""
        result = self.manager.execute_operation('rank', 2, 2, 1, 2, 2, 4)
        expected = 1  # rank([[1,2],[2,4]]) = 1 (linearly dependent)
        assert result == expected

    def test_singular_matrix_inverse(self):
        """Test that singular matrix raises error."""
        with pytest.raises(ValueError):
            self.manager.execute_operation('inverse', 2, 1, 2, 2, 4)


class TestStatistics:
    """Test statistical operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_mean(self):
        """Test mean calculation."""
        result = self.manager.execute_operation('mean', 1, 2, 3, 4, 5)
        assert result == 3.0

    def test_median(self):
        """Test median calculation."""
        result = self.manager.execute_operation('median', 1, 2, 3, 4, 5)
        assert result == 3.0

    def test_mode(self):
        """Test mode calculation."""
        result = self.manager.execute_operation('mode', 1, 2, 2, 3, 3, 3)
        assert result == 3.0

    def test_stdev(self):
        """Test standard deviation."""
        result = self.manager.execute_operation('stdev', 2, 4, 4, 4, 5, 5, 7, 9)
        # Sample stdev of this dataset
        assert abs(result - 2.138) < 0.01

    def test_variance(self):
        """Test variance calculation."""
        result = self.manager.execute_operation('variance', 2, 4, 4, 4, 5, 5, 7, 9)
        # Sample variance
        assert abs(result - 4.571) < 0.01

    def test_range_calculation(self):
        """Test range calculation."""
        result = self.manager.execute_operation('range', 1, 5, 3, 9, 2)
        assert result == 8.0  # 9 - 1 = 8

    def test_percentile(self):
        """Test percentile calculation."""
        result = self.manager.execute_operation('percentile', 50, 1, 2, 3, 4, 5)
        assert result == 3.0  # 50th percentile (median) is 3

    def test_correlation(self):
        """Test correlation coefficient."""
        # Perfect positive correlation
        result = self.manager.execute_operation('correlation', 3, 1, 2, 3, 2, 4, 6)
        assert abs(result - 1.0) < 0.01

    def test_zscore(self):
        """Test z-score calculation."""
        result = self.manager.execute_operation('zscore', 10, 5, 6, 7, 8, 9, 10, 11)
        # z-score should be positive since 10 is above mean
        assert result > 0

    def test_quartiles(self):
        """Test quartile calculation."""
        result = self.manager.execute_operation('quartiles', 1, 2, 3, 4, 5, 6, 7, 8, 9)
        q1, q2, q3 = result
        assert q1 < q2 < q3
        assert q2 == 5.0  # Median

    def test_normal_cdf(self):
        """Test normal CDF."""
        # P(X <= 0) for standard normal should be 0.5
        result = self.manager.execute_operation('normal_cdf', 0, 0, 1)
        assert abs(result - 0.5) < 0.01

    def test_linear_regression(self):
        """Test linear regression."""
        # y = 2x + 1: points (1,3), (2,5), (3,7)
        result = self.manager.execute_operation('linear_regression', 3, 1, 2, 3, 3, 5, 7)
        slope, intercept, r_value, p_value, std_err = result
        assert abs(slope - 2.0) < 0.01
        assert abs(intercept - 1.0) < 0.01
        assert abs(r_value - 1.0) < 0.01  # Perfect correlation


class TestCalculus:
    """Test calculus operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_derivative(self):
        """Test symbolic derivative."""
        result = self.manager.execute_operation('derivative', 'x**2', 'x')
        assert '2*x' in result

    def test_integrate_symbolic(self):
        """Test symbolic integration."""
        result = self.manager.execute_operation('integrate_symbolic', 'x', 'x')
        assert 'x**2' in result or 'x²' in result

    def test_integrate_definite(self):
        """Test definite integration."""
        # Integral of x^2 from 0 to 1 is 1/3
        result = self.manager.execute_operation('integrate', 'x**2', 0, 1)
        assert abs(result - 1/3) < 0.01

    def test_limit(self):
        """Test limit calculation."""
        # lim (sin(x)/x) as x->0 = 1
        result = self.manager.execute_operation('limit', 'sin(x)/x', 'x', 0)
        assert '1' in str(result)

    def test_taylor_series(self):
        """Test Taylor series expansion."""
        result = self.manager.execute_operation('taylor', 'exp(x)', 'x', 0, 5)
        # Should contain terms like 1 + x + x^2/2 + ...
        assert 'x' in result

    def test_second_derivative(self):
        """Test second derivative."""
        result = self.manager.execute_operation('derivative2', 'x**3', 'x')
        assert '6*x' in result

    def test_simplify(self):
        """Test expression simplification."""
        result = self.manager.execute_operation('simplify', '(x+1)**2 - (x**2 + 2*x + 1)')
        assert result == '0'

    def test_expand(self):
        """Test expression expansion."""
        result = self.manager.execute_operation('expand', '(x+1)**2')
        assert 'x**2' in result and '2*x' in result

    def test_factor(self):
        """Test factoring."""
        result = self.manager.execute_operation('factor', 'x**2 - 1')
        assert 'x - 1' in result and 'x + 1' in result


class TestNumberTheory:
    """Test number theory operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_is_prime_true(self):
        """Test prime detection for primes."""
        result = self.manager.execute_operation('is_prime', 17)
        assert result is True

    def test_is_prime_false(self):
        """Test prime detection for composites."""
        result = self.manager.execute_operation('is_prime', 18)
        assert result is False

    def test_prime_factors(self):
        """Test prime factorization."""
        result = self.manager.execute_operation('prime_factors', 84)
        # 84 = 2^2 * 3 * 7
        assert result[2] == 2
        assert result[3] == 1
        assert result[7] == 1

    def test_gcd(self):
        """Test GCD calculation."""
        result = self.manager.execute_operation('gcd', 48, 18)
        assert result == 6

    def test_lcm(self):
        """Test LCM calculation."""
        result = self.manager.execute_operation('lcm', 12, 18)
        assert result == 36

    def test_mod_power(self):
        """Test modular exponentiation."""
        result = self.manager.execute_operation('mod_power', 3, 4, 5)
        # 3^4 = 81, 81 mod 5 = 1
        assert result == 1

    def test_permutations(self):
        """Test permutations."""
        result = self.manager.execute_operation('permutations', 5, 3)
        assert result == 60  # P(5,3) = 5!/(5-3)! = 60

    def test_combinations(self):
        """Test combinations."""
        result = self.manager.execute_operation('combinations', 5, 3)
        assert result == 10  # C(5,3) = 10

    def test_factorial(self):
        """Test factorial."""
        result = self.manager.execute_operation('factorial', 5)
        assert result == 120

    def test_fibonacci(self):
        """Test Fibonacci number."""
        result = self.manager.execute_operation('fibonacci', 10)
        assert result == 55

    def test_binomial_coefficient(self):
        """Test binomial coefficient."""
        result = self.manager.execute_operation('binomial', 5, 2)
        assert result == 10

    def test_euler_phi(self):
        """Test Euler's totient function."""
        result = self.manager.execute_operation('euler_phi', 12)
        # φ(12) = 4 (numbers coprime to 12: 1, 5, 7, 11)
        assert result == 4

    def test_next_prime(self):
        """Test next prime."""
        result = self.manager.execute_operation('next_prime', 10)
        assert result == 11

    def test_nth_prime(self):
        """Test nth prime."""
        result = self.manager.execute_operation('nth_prime', 10)
        assert result == 29  # 10th prime is 29

    def test_prime_count(self):
        """Test prime counting."""
        result = self.manager.execute_operation('prime_count', 100)
        assert result == 25  # There are 25 primes <= 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
