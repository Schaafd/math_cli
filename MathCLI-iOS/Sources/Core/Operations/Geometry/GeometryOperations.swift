//
//  GeometryOperations.swift
//  MathCLI
//
//  Geometry operations (15 operations)
//

import Foundation

// MARK: - Distance Operations

struct DistanceOperation: MathOperation {
    static var name = "distance"
    static var arguments = ["x1", "y1", "x2", "y2"]
    static var help = "Calculate 2D distance between two points: distance x1 y1 x2 y2"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x1 = try parseDouble(args[0], argumentName: "x1")
        let y1 = try parseDouble(args[1], argumentName: "y1")
        let x2 = try parseDouble(args[2], argumentName: "x2")
        let y2 = try parseDouble(args[3], argumentName: "y2")

        let dx = x2 - x1
        let dy = y2 - y1
        return .number(sqrt(dx * dx + dy * dy))
    }
}

struct Distance3dOperation: MathOperation {
    static var name = "distance3d"
    static var arguments = ["x1", "y1", "z1", "x2", "y2", "z2"]
    static var help = "Calculate 3D distance between two points: distance3d x1 y1 z1 x2 y2 z2"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x1 = try parseDouble(args[0], argumentName: "x1")
        let y1 = try parseDouble(args[1], argumentName: "y1")
        let z1 = try parseDouble(args[2], argumentName: "z1")
        let x2 = try parseDouble(args[3], argumentName: "x2")
        let y2 = try parseDouble(args[4], argumentName: "y2")
        let z2 = try parseDouble(args[5], argumentName: "z2")

        let dx = x2 - x1
        let dy = y2 - y1
        let dz = z2 - z1
        return .number(sqrt(dx * dx + dy * dy + dz * dz))
    }
}

// MARK: - Circle Operations

struct AreaCircleOperation: MathOperation {
    static var name = "area_circle"
    static var arguments = ["radius"]
    static var help = "Calculate area of circle: area_circle radius"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let radius = try parseDouble(args[0], argumentName: "radius")
        guard radius >= 0 else {
            throw OperationError.invalidValue("Radius must be non-negative")
        }
        return .number(Double.pi * radius * radius)
    }
}

struct CircumferenceOperation: MathOperation {
    static var name = "circumference"
    static var arguments = ["radius"]
    static var help = "Calculate circumference of circle: circumference radius"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let radius = try parseDouble(args[0], argumentName: "radius")
        guard radius >= 0 else {
            throw OperationError.invalidValue("Radius must be non-negative")
        }
        return .number(2 * Double.pi * radius)
    }
}

// MARK: - Triangle Operations

struct AreaTriangleOperation: MathOperation {
    static var name = "area_triangle"
    static var arguments = ["base", "height"]
    static var help = "Calculate area of triangle: area_triangle base height"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let base = try parseDouble(args[0], argumentName: "base")
        let height = try parseDouble(args[1], argumentName: "height")
        guard base >= 0 && height >= 0 else {
            throw OperationError.invalidValue("Base and height must be non-negative")
        }
        return .number(0.5 * base * height)
    }
}

struct AreaTriangleHeronOperation: MathOperation {
    static var name = "area_triangle_heron"
    static var arguments = ["a", "b", "c"]
    static var help = "Calculate area of triangle using Heron's formula: area_triangle_heron a b c"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        let c = try parseDouble(args[2], argumentName: "c")

        guard a > 0 && b > 0 && c > 0 else {
            throw OperationError.invalidValue("All sides must be positive")
        }

        // Triangle inequality check
        guard a + b > c && a + c > b && b + c > a else {
            throw OperationError.invalidValue("Invalid triangle: sides don't satisfy triangle inequality")
        }

        let s = (a + b + c) / 2 // semi-perimeter
        return .number(sqrt(s * (s - a) * (s - b) * (s - c)))
    }
}

struct PythagoreanOperation: MathOperation {
    static var name = "pythagorean"
    static var arguments = ["a", "b"]
    static var help = "Calculate hypotenuse using Pythagorean theorem: pythagorean a b"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .number(sqrt(a * a + b * b))
    }
}

struct PythagoreanSideOperation: MathOperation {
    static var name = "pythagorean_side"
    static var arguments = ["hypotenuse", "side"]
    static var help = "Calculate other side using Pythagorean theorem: pythagorean_side hypotenuse side"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let hypotenuse = try parseDouble(args[0], argumentName: "hypotenuse")
        let side = try parseDouble(args[1], argumentName: "side")

        guard hypotenuse >= side else {
            throw OperationError.invalidValue("Hypotenuse must be greater than or equal to the side")
        }

        return .number(sqrt(hypotenuse * hypotenuse - side * side))
    }
}

// MARK: - Rectangle Operations

struct AreaRectangleOperation: MathOperation {
    static var name = "area_rectangle"
    static var arguments = ["length", "width"]
    static var help = "Calculate area of rectangle: area_rectangle length width"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let length = try parseDouble(args[0], argumentName: "length")
        let width = try parseDouble(args[1], argumentName: "width")
        guard length >= 0 && width >= 0 else {
            throw OperationError.invalidValue("Dimensions must be non-negative")
        }
        return .number(length * width)
    }
}

struct PerimeterRectangleOperation: MathOperation {
    static var name = "perimeter_rectangle"
    static var arguments = ["length", "width"]
    static var help = "Calculate perimeter of rectangle: perimeter_rectangle length width"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let length = try parseDouble(args[0], argumentName: "length")
        let width = try parseDouble(args[1], argumentName: "width")
        guard length >= 0 && width >= 0 else {
            throw OperationError.invalidValue("Dimensions must be non-negative")
        }
        return .number(2 * (length + width))
    }
}

struct AreaSquareOperation: MathOperation {
    static var name = "area_square"
    static var arguments = ["side"]
    static var help = "Calculate area of square: area_square side"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let side = try parseDouble(args[0], argumentName: "side")
        guard side >= 0 else {
            throw OperationError.invalidValue("Side must be non-negative")
        }
        return .number(side * side)
    }
}

// MARK: - Sphere Operations

struct VolumeSphereOperation: MathOperation {
    static var name = "volume_sphere"
    static var arguments = ["radius"]
    static var help = "Calculate volume of sphere: volume_sphere radius"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let radius = try parseDouble(args[0], argumentName: "radius")
        guard radius >= 0 else {
            throw OperationError.invalidValue("Radius must be non-negative")
        }
        return .number((4.0/3.0) * Double.pi * pow(radius, 3))
    }
}

struct SurfaceAreaSphereOperation: MathOperation {
    static var name = "surface_area_sphere"
    static var arguments = ["radius"]
    static var help = "Calculate surface area of sphere: surface_area_sphere radius"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let radius = try parseDouble(args[0], argumentName: "radius")
        guard radius >= 0 else {
            throw OperationError.invalidValue("Radius must be non-negative")
        }
        return .number(4 * Double.pi * radius * radius)
    }
}

// MARK: - Cylinder Operations

struct VolumeCylinderOperation: MathOperation {
    static var name = "volume_cylinder"
    static var arguments = ["radius", "height"]
    static var help = "Calculate volume of cylinder: volume_cylinder radius height"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let radius = try parseDouble(args[0], argumentName: "radius")
        let height = try parseDouble(args[1], argumentName: "height")
        guard radius >= 0 && height >= 0 else {
            throw OperationError.invalidValue("Radius and height must be non-negative")
        }
        return .number(Double.pi * radius * radius * height)
    }
}

// MARK: - Polygon Operations

struct AreaRegularPolygonOperation: MathOperation {
    static var name = "area_regular_polygon"
    static var arguments = ["sides", "side_length"]
    static var help = "Calculate area of regular polygon: area_regular_polygon sides side_length"
    static var category = OperationCategory.geometry

    static func execute(args: [Any]) throws -> OperationResult {
        let sides = try parseInt(args[0], argumentName: "sides")
        let sideLength = try parseDouble(args[1], argumentName: "side_length")

        guard sides >= 3 else {
            throw OperationError.invalidValue("Polygon must have at least 3 sides")
        }
        guard sideLength > 0 else {
            throw OperationError.invalidValue("Side length must be positive")
        }

        let n = Double(sides)
        let area = (n * sideLength * sideLength) / (4 * tan(Double.pi / n))
        return .number(area)
    }
}
