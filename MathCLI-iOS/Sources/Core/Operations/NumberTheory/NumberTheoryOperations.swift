//
//  NumberTheoryOperations.swift
//  MathCLI
//
//  Number theory operations (15 operations)
//

import Foundation

// Helper function for GCD (used by multiple operations)
private func gcd(_ a: Int, _ b: Int) -> Int {
    return b == 0 ? abs(a) : gcd(b, a % b)
}

// MARK: - Is Prime (Number Theory version)

struct IsPrimeNTOperation: MathOperation {
    static var name = "is_prime"
    static var arguments = ["n"]
    static var help = "Check if number is prime: is_prime n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        if n < 2 { return .boolean(false) }
        if n == 2 { return .boolean(true) }
        if n % 2 == 0 { return .boolean(false) }

        let limit = Int(sqrt(Double(n)))
        for i in stride(from: 3, through: limit, by: 2) {
            if n % i == 0 { return .boolean(false) }
        }

        return .boolean(true)
    }
}

// MARK: - Prime Factors (Number Theory version)

struct PrimeFactorsNTOperation: MathOperation {
    static var name = "prime_factors"
    static var arguments = ["n"]
    static var help = "Find prime factors: prime_factors n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        var n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("n must be positive")
        }

        var factors: [Double] = []

        while n % 2 == 0 {
            factors.append(2)
            n /= 2
        }

        var i = 3
        while i * i <= n {
            while n % i == 0 {
                factors.append(Double(i))
                n /= i
            }
            i += 2
        }

        if n > 1 {
            factors.append(Double(n))
        }

        return .array(factors)
    }
}

// MARK: - Next Prime

struct NextPrimeOperation: MathOperation {
    static var name = "next_prime"
    static var arguments = ["n"]
    static var help = "Find next prime after n: next_prime n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        var n = try parseInt(args[0], argumentName: "n")

        func isPrime(_ num: Int) -> Bool {
            if num < 2 { return false }
            if num == 2 { return true }
            if num % 2 == 0 { return false }
            let limit = Int(sqrt(Double(num)))
            for i in stride(from: 3, through: limit, by: 2) {
                if num % i == 0 { return false }
            }
            return true
        }

        n += 1
        while !isPrime(n) {
            n += 1
            if n > 1_000_000 { // Safety limit
                throw OperationError.executionError("Search limit exceeded")
            }
        }

        return .integer(n)
    }
}

// MARK: - Prime Count

struct PrimeCountOperation: MathOperation {
    static var name = "prime_count"
    static var arguments = ["n"]
    static var help = "Count primes up to n: prime_count n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("n must be non-negative")
        }

        if n < 2 { return .integer(0) }

        // Sieve of Eratosthenes
        var isPrime = Array(repeating: true, count: n + 1)
        isPrime[0] = false
        isPrime[1] = false

        for i in 2...Int(sqrt(Double(n))) {
            if isPrime[i] {
                for j in stride(from: i * i, through: n, by: i) {
                    isPrime[j] = false
                }
            }
        }

        let count = isPrime.filter { $0 }.count
        return .integer(count)
    }
}

// MARK: - Euler's Totient (Phi)

struct EulerPhiOperation: MathOperation {
    static var name = "euler_phi"
    static var arguments = ["n"]
    static var help = "Calculate Euler's totient function: euler_phi n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        var n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("n must be positive")
        }

        var result = n

        // For each prime factor p, multiply result by (1 - 1/p)
        var p = 2
        while p * p <= n {
            if n % p == 0 {
                while n % p == 0 {
                    n /= p
                }
                result -= result / p
            }
            p += 1
        }

        if n > 1 {
            result -= result / n
        }

        return .integer(result)
    }
}

// MARK: - Divisors

struct DivisorsOperation: MathOperation {
    static var name = "divisors"
    static var arguments = ["n"]
    static var help = "Find all divisors of n: divisors n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("n must be positive")
        }

        var divisors: [Double] = []

        for i in 1...Int(sqrt(Double(n))) {
            if n % i == 0 {
                divisors.append(Double(i))
                if i != n / i {
                    divisors.append(Double(n / i))
                }
            }
        }

        return .array(divisors.sorted())
    }
}

// MARK: - Perfect Number

struct PerfectNumberOperation: MathOperation {
    static var name = "perfect_number"
    static var arguments = ["n"]
    static var help = "Check if n is a perfect number: perfect_number n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            return .boolean(false)
        }

        var sum = 0
        for i in 1..<n {
            if n % i == 0 {
                sum += i
            }
        }

        return .boolean(sum == n)
    }
}

// MARK: - Catalan Number

struct CatalanOperation: MathOperation {
    static var name = "catalan"
    static var arguments = ["n"]
    static var help = "Calculate nth Catalan number: catalan n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("n must be non-negative")
        }
        guard n <= 30 else {
            throw OperationError.invalidValue("n too large (max 30)")
        }

        // Catalan(n) = (2n)! / ((n+1)! * n!)
        // Using formula: Catalan(n) = C(2n, n) / (n + 1)
        func binomial(_ n: Int, _ k: Int) -> Int {
            if k > n { return 0 }
            if k == 0 || k == n { return 1 }

            var result = 1
            for i in 0..<min(k, n - k) {
                result = result * (n - i) / (i + 1)
            }
            return result
        }

        let result = binomial(2 * n, n) / (n + 1)
        return .integer(result)
    }
}

// MARK: - Bell Number

struct BellNumberOperation: MathOperation {
    static var name = "bell_number"
    static var arguments = ["n"]
    static var help = "Calculate nth Bell number: bell_number n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("n must be non-negative")
        }
        guard n <= 15 else {
            throw OperationError.invalidValue("n too large (max 15)")
        }

        // Bell triangle
        var bell = [[Int]](repeating: [Int](repeating: 0, count: n + 1), count: n + 1)
        bell[0][0] = 1

        for i in 1...n {
            bell[i][0] = bell[i - 1][i - 1]
            for j in 1...i {
                bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
            }
        }

        return .integer(bell[n][0])
    }
}

// MARK: - Stirling Number (Second Kind)

struct StirlingOperation: MathOperation {
    static var name = "stirling"
    static var arguments = ["n", "k"]
    static var help = "Calculate Stirling number of second kind: stirling n k"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        let k = try parseInt(args[1], argumentName: "k")

        guard n >= 0 && k >= 0 else {
            throw OperationError.invalidValue("n and k must be non-negative")
        }
        guard n <= 20 && k <= 20 else {
            throw OperationError.invalidValue("n and k too large (max 20)")
        }

        if k > n { return .integer(0) }
        if k == 0 { return n == 0 ? .integer(1) : .integer(0) }
        if k == n { return .integer(1) }

        // Dynamic programming approach
        var dp = [[Int]](repeating: [Int](repeating: 0, count: k + 1), count: n + 1)

        for i in 0...n {
            dp[i][0] = 0
            if i <= k {
                dp[i][i] = 1
            }
        }
        dp[0][0] = 1

        for i in 1...n {
            for j in 1...min(i, k) {
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
            }
        }

        return .integer(dp[n][k])
    }
}

// MARK: - Partition

struct PartitionOperation: MathOperation {
    static var name = "partition"
    static var arguments = ["n"]
    static var help = "Calculate number of partitions of n: partition n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("n must be non-negative")
        }
        guard n <= 100 else {
            throw OperationError.invalidValue("n too large (max 100)")
        }

        var partitions = [Int](repeating: 0, count: n + 1)
        partitions[0] = 1

        for i in 1...n {
            for j in i...n {
                partitions[j] += partitions[j - i]
            }
        }

        return .integer(partitions[n])
    }
}

// MARK: - Möbius Function

struct MobiusOperation: MathOperation {
    static var name = "mobius"
    static var arguments = ["n"]
    static var help = "Calculate Möbius function μ(n): mobius n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        var n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("n must be positive")
        }

        if n == 1 { return .integer(1) }

        var primeCount = 0
        var temp = n

        // Check for square factors and count prime factors
        var p = 2
        while p * p <= temp {
            if temp % p == 0 {
                primeCount += 1
                temp /= p
                if temp % p == 0 {
                    // Has square factor
                    return .integer(0)
                }
            }
            p += 1
        }

        if temp > 1 {
            primeCount += 1
        }

        // μ(n) = (-1)^k where k is number of prime factors
        return .integer(primeCount % 2 == 0 ? 1 : -1)
    }
}

// MARK: - Totient (Alias)

struct TotientOperation: MathOperation {
    static var name = "totient"
    static var arguments = ["n"]
    static var help = "Calculate Euler's totient (alias for euler_phi): totient n"
    static var category = OperationCategory.numberTheory

    static func execute(args: [Any]) throws -> OperationResult {
        return try EulerPhiOperation.execute(args: args)
    }
}
