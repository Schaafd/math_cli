//
//  ConversionOperations.swift
//  MathCLI
//
//  Unit conversion operations (38 operations)
//

import Foundation

// MARK: - Temperature Conversions (4)

struct CelsiusToFahrenheitOperation: MathOperation {
    static var name = "celsius_to_fahrenheit"
    static var arguments = ["celsius"]
    static var help = "Convert Celsius to Fahrenheit: celsius_to_fahrenheit celsius"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let celsius = try parseDouble(args[0], argumentName: "celsius")
        return .number(celsius * 9/5 + 32)
    }
}

struct FahrenheitToCelsiusOperation: MathOperation {
    static var name = "fahrenheit_to_celsius"
    static var arguments = ["fahrenheit"]
    static var help = "Convert Fahrenheit to Celsius: fahrenheit_to_celsius fahrenheit"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let fahrenheit = try parseDouble(args[0], argumentName: "fahrenheit")
        return .number((fahrenheit - 32) * 5/9)
    }
}

struct CelsiusToKelvinOperation: MathOperation {
    static var name = "celsius_to_kelvin"
    static var arguments = ["celsius"]
    static var help = "Convert Celsius to Kelvin: celsius_to_kelvin celsius"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let celsius = try parseDouble(args[0], argumentName: "celsius")
        return .number(celsius + 273.15)
    }
}

struct KelvinToCelsiusOperation: MathOperation {
    static var name = "kelvin_to_celsius"
    static var arguments = ["kelvin"]
    static var help = "Convert Kelvin to Celsius: kelvin_to_celsius kelvin"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kelvin = try parseDouble(args[0], argumentName: "kelvin")
        return .number(kelvin - 273.15)
    }
}

// MARK: - Distance Conversions (6)

struct MilesToKilometersOperation: MathOperation {
    static var name = "miles_to_kilometers"
    static var arguments = ["miles"]
    static var help = "Convert miles to kilometers: miles_to_kilometers miles"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let miles = try parseDouble(args[0], argumentName: "miles")
        return .number(miles * 1.609344)
    }
}

struct KilometersToMilesOperation: MathOperation {
    static var name = "kilometers_to_miles"
    static var arguments = ["kilometers"]
    static var help = "Convert kilometers to miles: kilometers_to_miles kilometers"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kilometers = try parseDouble(args[0], argumentName: "kilometers")
        return .number(kilometers / 1.609344)
    }
}

struct FeetToMetersOperation: MathOperation {
    static var name = "feet_to_meters"
    static var arguments = ["feet"]
    static var help = "Convert feet to meters: feet_to_meters feet"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let feet = try parseDouble(args[0], argumentName: "feet")
        return .number(feet * 0.3048)
    }
}

struct MetersToFeetOperation: MathOperation {
    static var name = "meters_to_feet"
    static var arguments = ["meters"]
    static var help = "Convert meters to feet: meters_to_feet meters"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let meters = try parseDouble(args[0], argumentName: "meters")
        return .number(meters / 0.3048)
    }
}

struct InchesToCentimetersOperation: MathOperation {
    static var name = "inches_to_centimeters"
    static var arguments = ["inches"]
    static var help = "Convert inches to centimeters: inches_to_centimeters inches"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let inches = try parseDouble(args[0], argumentName: "inches")
        return .number(inches * 2.54)
    }
}

struct CentimetersToInchesOperation: MathOperation {
    static var name = "centimeters_to_inches"
    static var arguments = ["centimeters"]
    static var help = "Convert centimeters to inches: centimeters_to_inches centimeters"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let centimeters = try parseDouble(args[0], argumentName: "centimeters")
        return .number(centimeters / 2.54)
    }
}

// MARK: - Weight Conversions (2)

struct PoundsToKilogramsOperation: MathOperation {
    static var name = "pounds_to_kilograms"
    static var arguments = ["pounds"]
    static var help = "Convert pounds to kilograms: pounds_to_kilograms pounds"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let pounds = try parseDouble(args[0], argumentName: "pounds")
        return .number(pounds * 0.45359237)
    }
}

struct KilogramsToPoundsOperation: MathOperation {
    static var name = "kilograms_to_pounds"
    static var arguments = ["kilograms"]
    static var help = "Convert kilograms to pounds: kilograms_to_pounds kilograms"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kilograms = try parseDouble(args[0], argumentName: "kilograms")
        return .number(kilograms / 0.45359237)
    }
}

// MARK: - Volume Conversions (2)

struct GallonsToLitersOperation: MathOperation {
    static var name = "gallons_to_liters"
    static var arguments = ["gallons"]
    static var help = "Convert gallons to liters: gallons_to_liters gallons"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let gallons = try parseDouble(args[0], argumentName: "gallons")
        return .number(gallons * 3.78541)
    }
}

struct LitersToGallonsOperation: MathOperation {
    static var name = "liters_to_gallons"
    static var arguments = ["liters"]
    static var help = "Convert liters to gallons: liters_to_gallons liters"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let liters = try parseDouble(args[0], argumentName: "liters")
        return .number(liters / 3.78541)
    }
}

// MARK: - Speed Conversions (2)

struct MphToKphOperation: MathOperation {
    static var name = "mph_to_kph"
    static var arguments = ["mph"]
    static var help = "Convert miles per hour to kilometers per hour: mph_to_kph mph"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let mph = try parseDouble(args[0], argumentName: "mph")
        return .number(mph * 1.609344)
    }
}

struct KphToMphOperation: MathOperation {
    static var name = "kph_to_mph"
    static var arguments = ["kph"]
    static var help = "Convert kilometers per hour to miles per hour: kph_to_mph kph"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kph = try parseDouble(args[0], argumentName: "kph")
        return .number(kph / 1.609344)
    }
}

// MARK: - Time Conversions (6)

struct HoursToSecondsOperation: MathOperation {
    static var name = "hours_to_seconds"
    static var arguments = ["hours"]
    static var help = "Convert hours to seconds: hours_to_seconds hours"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let hours = try parseDouble(args[0], argumentName: "hours")
        return .number(hours * 3600)
    }
}

struct MinutesToSecondsOperation: MathOperation {
    static var name = "minutes_to_seconds"
    static var arguments = ["minutes"]
    static var help = "Convert minutes to seconds: minutes_to_seconds minutes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let minutes = try parseDouble(args[0], argumentName: "minutes")
        return .number(minutes * 60)
    }
}

struct DaysToHoursOperation: MathOperation {
    static var name = "days_to_hours"
    static var arguments = ["days"]
    static var help = "Convert days to hours: days_to_hours days"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let days = try parseDouble(args[0], argumentName: "days")
        return .number(days * 24)
    }
}

struct WeeksToDaysOperation: MathOperation {
    static var name = "weeks_to_days"
    static var arguments = ["weeks"]
    static var help = "Convert weeks to days: weeks_to_days weeks"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let weeks = try parseDouble(args[0], argumentName: "weeks")
        return .number(weeks * 7)
    }
}

struct YearsToDaysOperation: MathOperation {
    static var name = "years_to_days"
    static var arguments = ["years"]
    static var help = "Convert years to days: years_to_days years"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let years = try parseDouble(args[0], argumentName: "years")
        return .number(years * 365.25)
    }
}

struct SecondsToMillisecondsOperation: MathOperation {
    static var name = "seconds_to_milliseconds"
    static var arguments = ["seconds"]
    static var help = "Convert seconds to milliseconds: seconds_to_milliseconds seconds"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let seconds = try parseDouble(args[0], argumentName: "seconds")
        return .number(seconds * 1000)
    }
}

// MARK: - Data Size Conversions (8)

struct KbToBytesOperation: MathOperation {
    static var name = "kb_to_bytes"
    static var arguments = ["kilobytes"]
    static var help = "Convert kilobytes to bytes: kb_to_bytes kilobytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kb = try parseDouble(args[0], argumentName: "kilobytes")
        return .number(kb * 1024)
    }
}

struct MbToBytesOperation: MathOperation {
    static var name = "mb_to_bytes"
    static var arguments = ["megabytes"]
    static var help = "Convert megabytes to bytes: mb_to_bytes megabytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let mb = try parseDouble(args[0], argumentName: "megabytes")
        return .number(mb * 1024 * 1024)
    }
}

struct GbToBytesOperation: MathOperation {
    static var name = "gb_to_bytes"
    static var arguments = ["gigabytes"]
    static var help = "Convert gigabytes to bytes: gb_to_bytes gigabytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let gb = try parseDouble(args[0], argumentName: "gigabytes")
        return .number(gb * 1024 * 1024 * 1024)
    }
}

struct TbToBytesOperation: MathOperation {
    static var name = "tb_to_bytes"
    static var arguments = ["terabytes"]
    static var help = "Convert terabytes to bytes: tb_to_bytes terabytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let tb = try parseDouble(args[0], argumentName: "terabytes")
        return .number(tb * 1024 * 1024 * 1024 * 1024)
    }
}

struct BytesToKbOperation: MathOperation {
    static var name = "bytes_to_kb"
    static var arguments = ["bytes"]
    static var help = "Convert bytes to kilobytes: bytes_to_kb bytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let bytes = try parseDouble(args[0], argumentName: "bytes")
        return .number(bytes / 1024)
    }
}

struct BytesToMbOperation: MathOperation {
    static var name = "bytes_to_mb"
    static var arguments = ["bytes"]
    static var help = "Convert bytes to megabytes: bytes_to_mb bytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let bytes = try parseDouble(args[0], argumentName: "bytes")
        return .number(bytes / (1024 * 1024))
    }
}

struct BytesToGbOperation: MathOperation {
    static var name = "bytes_to_gb"
    static var arguments = ["bytes"]
    static var help = "Convert bytes to gigabytes: bytes_to_gb bytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let bytes = try parseDouble(args[0], argumentName: "bytes")
        return .number(bytes / (1024 * 1024 * 1024))
    }
}

struct BytesToTbOperation: MathOperation {
    static var name = "bytes_to_tb"
    static var arguments = ["bytes"]
    static var help = "Convert bytes to terabytes: bytes_to_tb bytes"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let bytes = try parseDouble(args[0], argumentName: "bytes")
        return .number(bytes / (1024 * 1024 * 1024 * 1024))
    }
}

// MARK: - Energy Conversions (4)

struct JoulesToCaloriesOperation: MathOperation {
    static var name = "joules_to_calories"
    static var arguments = ["joules"]
    static var help = "Convert joules to calories: joules_to_calories joules"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let joules = try parseDouble(args[0], argumentName: "joules")
        return .number(joules / 4.184)
    }
}

struct CaloriesToJoulesOperation: MathOperation {
    static var name = "calories_to_joules"
    static var arguments = ["calories"]
    static var help = "Convert calories to joules: calories_to_joules calories"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let calories = try parseDouble(args[0], argumentName: "calories")
        return .number(calories * 4.184)
    }
}

struct KwhToJoulesOperation: MathOperation {
    static var name = "kwh_to_joules"
    static var arguments = ["kilowatt_hours"]
    static var help = "Convert kilowatt-hours to joules: kwh_to_joules kilowatt_hours"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let kwh = try parseDouble(args[0], argumentName: "kilowatt_hours")
        return .number(kwh * 3_600_000)
    }
}

struct JoulesToKwhOperation: MathOperation {
    static var name = "joules_to_kwh"
    static var arguments = ["joules"]
    static var help = "Convert joules to kilowatt-hours: joules_to_kwh joules"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let joules = try parseDouble(args[0], argumentName: "joules")
        return .number(joules / 3_600_000)
    }
}

// MARK: - Pressure Conversions (4)

struct PsiToPascalOperation: MathOperation {
    static var name = "psi_to_pascal"
    static var arguments = ["psi"]
    static var help = "Convert PSI to pascals: psi_to_pascal psi"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let psi = try parseDouble(args[0], argumentName: "psi")
        return .number(psi * 6894.76)
    }
}

struct PascalToPsiOperation: MathOperation {
    static var name = "pascal_to_psi"
    static var arguments = ["pascal"]
    static var help = "Convert pascals to PSI: pascal_to_psi pascal"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let pascal = try parseDouble(args[0], argumentName: "pascal")
        return .number(pascal / 6894.76)
    }
}

struct BarToPascalOperation: MathOperation {
    static var name = "bar_to_pascal"
    static var arguments = ["bar"]
    static var help = "Convert bar to pascals: bar_to_pascal bar"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let bar = try parseDouble(args[0], argumentName: "bar")
        return .number(bar * 100_000)
    }
}

struct PascalToBarOperation: MathOperation {
    static var name = "pascal_to_bar"
    static var arguments = ["pascal"]
    static var help = "Convert pascals to bar: pascal_to_bar pascal"
    static var category = OperationCategory.conversions

    static func execute(args: [Any]) throws -> OperationResult {
        let pascal = try parseDouble(args[0], argumentName: "pascal")
        return .number(pascal / 100_000)
    }
}
