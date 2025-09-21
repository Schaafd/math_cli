"""
Unit Conversions Plugin

Provides various unit conversion operations for length, weight, temperature,
area, volume, and other common measurements.
"""

import math
from core.base_operations import MathOperation

# Temperature Conversions
class CelsiusToFahrenheitOperation(MathOperation):
    name = "celsius_to_fahrenheit"
    args = ["celsius"]
    help = "Convert Celsius to Fahrenheit"

    @classmethod
    def execute(cls, celsius):
        return (celsius * 9/5) + 32

class FahrenheitToCelsiusOperation(MathOperation):
    name = "fahrenheit_to_celsius"
    args = ["fahrenheit"]
    help = "Convert Fahrenheit to Celsius"

    @classmethod
    def execute(cls, fahrenheit):
        return (fahrenheit - 32) * 5/9

class CelsiusToKelvinOperation(MathOperation):
    name = "celsius_to_kelvin"
    args = ["celsius"]
    help = "Convert Celsius to Kelvin"

    @classmethod
    def execute(cls, celsius):
        return celsius + 273.15

class KelvinToCelsiusOperation(MathOperation):
    name = "kelvin_to_celsius"
    args = ["kelvin"]
    help = "Convert Kelvin to Celsius"

    @classmethod
    def execute(cls, kelvin):
        if kelvin < 0:
            raise ValueError("Kelvin temperature cannot be negative")
        return kelvin - 273.15

class FahrenheitToKelvinOperation(MathOperation):
    name = "fahrenheit_to_kelvin"
    args = ["fahrenheit"]
    help = "Convert Fahrenheit to Kelvin"

    @classmethod
    def execute(cls, fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        return celsius + 273.15

class KelvinToFahrenheitOperation(MathOperation):
    name = "kelvin_to_fahrenheit"
    args = ["kelvin"]
    help = "Convert Kelvin to Fahrenheit"

    @classmethod
    def execute(cls, kelvin):
        if kelvin < 0:
            raise ValueError("Kelvin temperature cannot be negative")
        celsius = kelvin - 273.15
        return (celsius * 9/5) + 32

# Length Conversions
class MetersToFeetOperation(MathOperation):
    name = "meters_to_feet"
    args = ["meters"]
    help = "Convert meters to feet"

    @classmethod
    def execute(cls, meters):
        return meters * 3.28084

class FeetToMetersOperation(MathOperation):
    name = "feet_to_meters"
    args = ["feet"]
    help = "Convert feet to meters"

    @classmethod
    def execute(cls, feet):
        return feet / 3.28084

class MetersToInchesOperation(MathOperation):
    name = "meters_to_inches"
    args = ["meters"]
    help = "Convert meters to inches"

    @classmethod
    def execute(cls, meters):
        return meters * 39.3701

class InchesToMetersOperation(MathOperation):
    name = "inches_to_meters"
    args = ["inches"]
    help = "Convert inches to meters"

    @classmethod
    def execute(cls, inches):
        return inches / 39.3701

class KilometersToMilesOperation(MathOperation):
    name = "kilometers_to_miles"
    args = ["kilometers"]
    help = "Convert kilometers to miles"

    @classmethod
    def execute(cls, kilometers):
        return kilometers * 0.621371

class MilesToKilometersOperation(MathOperation):
    name = "miles_to_kilometers"
    args = ["miles"]
    help = "Convert miles to kilometers"

    @classmethod
    def execute(cls, miles):
        return miles / 0.621371

class CentimetersToInchesOperation(MathOperation):
    name = "centimeters_to_inches"
    args = ["centimeters"]
    help = "Convert centimeters to inches"

    @classmethod
    def execute(cls, centimeters):
        return centimeters / 2.54

class InchesToCentimetersOperation(MathOperation):
    name = "inches_to_centimeters"
    args = ["inches"]
    help = "Convert inches to centimeters"

    @classmethod
    def execute(cls, inches):
        return inches * 2.54

# Weight/Mass Conversions
class KilogramsToPoundsOperation(MathOperation):
    name = "kilograms_to_pounds"
    args = ["kilograms"]
    help = "Convert kilograms to pounds"

    @classmethod
    def execute(cls, kilograms):
        return kilograms * 2.20462

class PoundsToKilogramsOperation(MathOperation):
    name = "pounds_to_kilograms"
    args = ["pounds"]
    help = "Convert pounds to kilograms"

    @classmethod
    def execute(cls, pounds):
        return pounds / 2.20462

class GramsToPoundsOperation(MathOperation):
    name = "grams_to_pounds"
    args = ["grams"]
    help = "Convert grams to pounds"

    @classmethod
    def execute(cls, grams):
        return grams / 453.592

class PoundsToGramsOperation(MathOperation):
    name = "pounds_to_grams"
    args = ["pounds"]
    help = "Convert pounds to grams"

    @classmethod
    def execute(cls, pounds):
        return pounds * 453.592

class GramsToOuncesOperation(MathOperation):
    name = "grams_to_ounces"
    args = ["grams"]
    help = "Convert grams to ounces"

    @classmethod
    def execute(cls, grams):
        return grams / 28.3495

class OuncesToGramsOperation(MathOperation):
    name = "ounces_to_grams"
    args = ["ounces"]
    help = "Convert ounces to grams"

    @classmethod
    def execute(cls, ounces):
        return ounces * 28.3495

# Volume Conversions
class LitersToGallonsOperation(MathOperation):
    name = "liters_to_gallons"
    args = ["liters"]
    help = "Convert liters to US gallons"

    @classmethod
    def execute(cls, liters):
        return liters / 3.78541

class GallonsToLitersOperation(MathOperation):
    name = "gallons_to_liters"
    args = ["gallons"]
    help = "Convert US gallons to liters"

    @classmethod
    def execute(cls, gallons):
        return gallons * 3.78541

class LitersToQuartsOperation(MathOperation):
    name = "liters_to_quarts"
    args = ["liters"]
    help = "Convert liters to US quarts"

    @classmethod
    def execute(cls, liters):
        return liters * 1.05669

class QuartsToLitersOperation(MathOperation):
    name = "quarts_to_liters"
    args = ["quarts"]
    help = "Convert US quarts to liters"

    @classmethod
    def execute(cls, quarts):
        return quarts / 1.05669

class MillilitersToFluidOuncesOperation(MathOperation):
    name = "milliliters_to_fluid_ounces"
    args = ["milliliters"]
    help = "Convert milliliters to US fluid ounces"

    @classmethod
    def execute(cls, milliliters):
        return milliliters / 29.5735

class FluidOuncesToMillilitersOperation(MathOperation):
    name = "fluid_ounces_to_milliliters"
    args = ["fluid_ounces"]
    help = "Convert US fluid ounces to milliliters"

    @classmethod
    def execute(cls, fluid_ounces):
        return fluid_ounces * 29.5735

# Area Conversions
class SquareMetersToSquareFeetOperation(MathOperation):
    name = "square_meters_to_square_feet"
    args = ["square_meters"]
    help = "Convert square meters to square feet"

    @classmethod
    def execute(cls, square_meters):
        return square_meters * 10.7639

class SquareFeetToSquareMetersOperation(MathOperation):
    name = "square_feet_to_square_meters"
    args = ["square_feet"]
    help = "Convert square feet to square meters"

    @classmethod
    def execute(cls, square_feet):
        return square_feet / 10.7639

class AcresToSquareMetersOperation(MathOperation):
    name = "acres_to_square_meters"
    args = ["acres"]
    help = "Convert acres to square meters"

    @classmethod
    def execute(cls, acres):
        return acres * 4046.86

class SquareMetersToAcresOperation(MathOperation):
    name = "square_meters_to_acres"
    args = ["square_meters"]
    help = "Convert square meters to acres"

    @classmethod
    def execute(cls, square_meters):
        return square_meters / 4046.86

# Speed Conversions
class MetersPerSecondToMilesPerHourOperation(MathOperation):
    name = "mps_to_mph"
    args = ["meters_per_second"]
    help = "Convert meters per second to miles per hour"

    @classmethod
    def execute(cls, meters_per_second):
        return meters_per_second * 2.23694

class MilesPerHourToMetersPerSecondOperation(MathOperation):
    name = "mph_to_mps"
    args = ["miles_per_hour"]
    help = "Convert miles per hour to meters per second"

    @classmethod
    def execute(cls, miles_per_hour):
        return miles_per_hour / 2.23694

class KilometersPerHourToMilesPerHourOperation(MathOperation):
    name = "kph_to_mph"
    args = ["kilometers_per_hour"]
    help = "Convert kilometers per hour to miles per hour"

    @classmethod
    def execute(cls, kilometers_per_hour):
        return kilometers_per_hour / 1.60934

class MilesPerHourToKilometersPerHourOperation(MathOperation):
    name = "mph_to_kph"
    args = ["miles_per_hour"]
    help = "Convert miles per hour to kilometers per hour"

    @classmethod
    def execute(cls, miles_per_hour):
        return miles_per_hour * 1.60934

# Energy Conversions
class JoulesToCaloriesOperation(MathOperation):
    name = "joules_to_calories"
    args = ["joules"]
    help = "Convert joules to calories"

    @classmethod
    def execute(cls, joules):
        return joules / 4.184

class CaloriesToJoulesOperation(MathOperation):
    name = "calories_to_joules"
    args = ["calories"]
    help = "Convert calories to joules"

    @classmethod
    def execute(cls, calories):
        return calories * 4.184

class KilowattHoursToJoulesOperation(MathOperation):
    name = "kwh_to_joules"
    args = ["kilowatt_hours"]
    help = "Convert kilowatt-hours to joules"

    @classmethod
    def execute(cls, kilowatt_hours):
        return kilowatt_hours * 3600000

class JoulesToKilowattHoursOperation(MathOperation):
    name = "joules_to_kwh"
    args = ["joules"]
    help = "Convert joules to kilowatt-hours"

    @classmethod
    def execute(cls, joules):
        return joules / 3600000
