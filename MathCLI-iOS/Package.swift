// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "MathCLI",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        // The MathCLI library that can be imported into other projects
        .library(
            name: "MathCLICore",
            targets: ["MathCLICore"]
        ),
        // Executable for command-line testing (optional)
        .executable(
            name: "mathcli-tool",
            targets: ["MathCLITool"]
        )
    ],
    dependencies: [
        // Add any external dependencies here
        // Example: .package(url: "https://github.com/apple/swift-algorithms", from: "1.0.0")
    ],
    targets: [
        // Core library target containing all operations and engine
        .target(
            name: "MathCLICore",
            dependencies: [],
            path: "Sources/Core",
            exclude: [],
            sources: [
                "Engine/",
                "Models/",
                "Operations/"
            ]
        ),

        // Command-line tool for testing operations
        .executableTarget(
            name: "MathCLITool",
            dependencies: ["MathCLICore"],
            path: "Sources/Tool",
            sources: [
                "main.swift"
            ]
        ),

        // Test target
        .testTarget(
            name: "MathCLICoreTests",
            dependencies: ["MathCLICore"],
            path: "Tests",
            sources: [
                "OperationTests/",
                "EngineTests/"
            ]
        )
    ]
)
