//
//  CombinatoricsOperations.swift
//  MathCLI
//
//  Combinatorics operations (10 operations)
//

import Foundation

// MARK: - Combinations

struct CombinationsOperation: MathOperation {
    static var name = "combinations"
    static var arguments = ["n", "r"]
    static var help = "Calculate combinations (nCr): combinations n r"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        let r = try parseInt(args[1], argumentName: "r")

        guard n >= 0 && r >= 0 else {
            throw OperationError.invalidValue("n and r must be non-negative")
        }
        guard r <= n else {
            throw OperationError.invalidValue("r cannot be greater than n")
        }

        func factorial(_ num: Int) -> Int {
            return num <= 1 ? 1 : num * factorial(num - 1)
        }

        let result = factorial(n) / (factorial(r) * factorial(n - r))
        return .integer(result)
    }
}

// MARK: - Permutations

struct PermutationsOperation: MathOperation {
    static var name = "permutations"
    static var arguments = ["n", "r"]
    static var help = "Calculate permutations (nPr): permutations n r"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        let r = try parseInt(args[1], argumentName: "r")

        guard n >= 0 && r >= 0 else {
            throw OperationError.invalidValue("n and r must be non-negative")
        }
        guard r <= n else {
            throw OperationError.invalidValue("r cannot be greater than n")
        }

        func factorial(_ num: Int) -> Int {
            return num <= 1 ? 1 : num * factorial(num - 1)
        }

        let result = factorial(n) / factorial(n - r)
        return .integer(result)
    }
}

// MARK: - Fibonacci

struct FibonacciOperation: MathOperation {
    static var name = "fibonacci"
    static var arguments = ["n"]
    static var help = "Calculate nth Fibonacci number: fibonacci n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("n must be non-negative")
        }
        guard n <= 92 else {
            throw OperationError.invalidValue("n too large (max 92 for Int)")
        }

        func fib(_ n: Int) -> Int {
            if n <= 1 { return n }
            var a = 0, b = 1
            for _ in 2...n {
                let temp = a + b
                a = b
                b = temp
            }
            return b
        }

        return .integer(fib(n))
    }
}

// MARK: - Prime Check

struct IsPrimeOperation: MathOperation {
    static var name = "is_prime"
    static var arguments = ["n"]
    static var help = "Check if number is prime: is_prime n"
    static var category = OperationCategory.combinatorics

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

// MARK: - Prime Factorization

struct PrimeFactorsOperation: MathOperation {
    static var name = "prime_factors"
    static var arguments = ["n"]
    static var help = "Find prime factors of number: prime_factors n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        var n = try parseInt(args[0], argumentName: "n")

        guard n > 0 else {
            throw OperationError.invalidValue("n must be positive")
        }

        var factors: [Double] = []

        // Divide by 2
        while n % 2 == 0 {
            factors.append(2)
            n /= 2
        }

        // Divide by odd numbers
        var i = 3
        while i * i <= n {
            while n % i == 0 {
                factors.append(Double(i))
                n /= i
            }
            i += 2
        }

        // If n is still > 1, it's a prime factor
        if n > 1 {
            factors.append(Double(n))
        }

        return .array(factors)
    }
}

// MARK: - Even Check

struct IsEvenOperation: MathOperation {
    static var name = "is_even"
    static var arguments = ["n"]
    static var help = "Check if number is even: is_even n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        return .boolean(n % 2 == 0)
    }
}

// MARK: - Odd Check

struct IsOddOperation: MathOperation {
    static var name = "is_odd"
    static var arguments = ["n"]
    static var help = "Check if number is odd: is_odd n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        return .boolean(n % 2 != 0)
    }
}

// MARK: - Perfect Square Check

struct IsPerfectSquareOperation: MathOperation {
    static var name = "is_perfect_square"
    static var arguments = ["n"]
    static var help = "Check if number is a perfect square: is_perfect_square n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            return .boolean(false)
        }

        let sqrtN = Int(sqrt(Double(n)))
        return .boolean(sqrtN * sqrtN == n)
    }
}

// MARK: - Digit Sum

struct DigitSumOperation: MathOperation {
    static var name = "digit_sum"
    static var arguments = ["n"]
    static var help = "Calculate sum of digits: digit_sum n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        var n = abs(try parseInt(args[0], argumentName: "n"))

        var sum = 0
        while n > 0 {
            sum += n % 10
            n /= 10
        }

        return .integer(sum)
    }
}

// MARK: - Reverse Number

struct ReverseNumberOperation: MathOperation {
    static var name = "reverse_number"
    static var arguments = ["n"]
    static var help = "Reverse digits of number: reverse_number n"
    static var category = OperationCategory.combinatorics

    static func execute(args: [Any]) throws -> OperationResult {
        let n = try parseInt(args[0], argumentName: "n")
        let isNegative = n < 0
        var num = abs(n)

        var reversed = 0
        while num > 0 {
            reversed = reversed * 10 + (num % 10)
            num /= 10
        }

        return .integer(isNegative ? -reversed : reversed)
    }
}
