//
//  OperationRegistry.swift
//  MathCLI
//
//  Central registry for all mathematical operations
//

import Foundation

/// Registry that manages all available operations
class OperationRegistry {
    static let shared = OperationRegistry()

    private var operations: [String: any MathOperation.Type] = [:]

    private init() {
        registerAllOperations()
    }

    /// Register a single operation
    func register<T: MathOperation>(_ operationType: T.Type) {
        operations[operationType.name] = operationType
    }

    /// Get operation by name
    func getOperation(name: String) -> (any MathOperation.Type)? {
        return operations[name]
    }

    /// Get all operation names
    func getAllOperationNames() -> [String] {
        return Array(operations.keys).sorted()
    }

    /// Get operations by category
    func getOperations(in category: OperationCategory) -> [(String, any MathOperation.Type)] {
        return operations.filter { $0.value.category == category }
            .map { ($0.key, $0.value) }
            .sorted { $0.0 < $1.0 }
    }

    /// Get all categories that have operations
    func getAvailableCategories() -> [OperationCategory] {
        let categories = Set(operations.values.map { $0.category })
        return categories.sorted { $0.rawValue < $1.rawValue }
    }

    /// Search operations by name (fuzzy matching)
    func searchOperations(query: String) -> [(String, any MathOperation.Type)] {
        let lowercaseQuery = query.lowercased()
        return operations.filter { name, _ in
            name.lowercased().contains(lowercaseQuery)
        }
        .map { ($0.key, $0.value) }
        .sorted { $0.0 < $1.0 }
    }

    /// Get operation count
    var count: Int {
        return operations.count
    }

    /// Register all built-in operations (266 total!)
    private func registerAllOperations() {
        // ========================================
        // PHASE 1: Original 47 Operations
        // ========================================

        // Basic Arithmetic (14 operations)
        register(AddOperation.self)
        register(SubtractOperation.self)
        register(MultiplyOperation.self)
        register(DivideOperation.self)
        register(PowerOperation.self)
        register(SqrtOperation.self)
        register(FactorialOperation.self)
        register(LogOperation.self)
        register(SinOperation.self)
        register(CosOperation.self)
        register(TanOperation.self)
        register(ToRadiansOperation.self)
        register(ToDegreesOperation.self)
        register(AbsOperation.self)

        // Extended Trigonometry (10 operations)
        register(AsinOperation.self)
        register(AcosOperation.self)
        register(AtanOperation.self)
        register(Atan2Operation.self)
        register(SinhOperation.self)
        register(CoshOperation.self)
        register(TanhOperation.self)
        register(AsinhOperation.self)
        register(AcoshOperation.self)
        register(AtanhOperation.self)

        // Advanced Math (8 operations)
        register(CeilOperation.self)
        register(FloorOperation.self)
        register(RoundOperation.self)
        register(TruncOperation.self)
        register(GcdOperation.self)
        register(LcmOperation.self)
        register(ModOperation.self)
        register(ExpOperation.self)

        // Statistics (15 operations)
        register(MeanOperation.self)
        register(MedianOperation.self)
        register(ModeOperation.self)
        register(GeometricMeanOperation.self)
        register(HarmonicMeanOperation.self)
        register(VarianceOperation.self)
        register(PopVarianceOperation.self)
        register(StdDevOperation.self)
        register(PopStdDevOperation.self)
        register(RangeOperation.self)
        register(MinOperation.self)
        register(MaxOperation.self)
        register(SumOperation.self)
        register(ProductOperation.self)
        register(CountOperation.self)

        // ========================================
        // PHASE 2: NEW 219 Operations
        // ========================================

        // Constants (7 operations)
        register(PiOperation.self)
        register(EOperation.self)
        register(GoldenRatioOperation.self)
        register(SpeedOfLightOperation.self)
        register(PlanckOperation.self)
        register(AvogadroOperation.self)
        register(BoltzmannOperation.self)

        // Unit Conversions (38 operations)
        // Temperature
        register(CelsiusToFahrenheitOperation.self)
        register(FahrenheitToCelsiusOperation.self)
        register(CelsiusToKelvinOperation.self)
        register(KelvinToCelsiusOperation.self)
        // Distance
        register(MilesToKilometersOperation.self)
        register(KilometersToMilesOperation.self)
        register(FeetToMetersOperation.self)
        register(MetersToFeetOperation.self)
        register(InchesToCentimetersOperation.self)
        register(CentimetersToInchesOperation.self)
        // Weight
        register(PoundsToKilogramsOperation.self)
        register(KilogramsToPoundsOperation.self)
        // Volume
        register(GallonsToLitersOperation.self)
        register(LitersToGallonsOperation.self)
        // Speed
        register(MphToKphOperation.self)
        register(KphToMphOperation.self)
        // Time
        register(HoursToSecondsOperation.self)
        register(MinutesToSecondsOperation.self)
        register(DaysToHoursOperation.self)
        register(WeeksToDaysOperation.self)
        register(YearsToDaysOperation.self)
        register(SecondsToMillisecondsOperation.self)
        // Data Size
        register(KbToBytesOperation.self)
        register(MbToBytesOperation.self)
        register(GbToBytesOperation.self)
        register(TbToBytesOperation.self)
        register(BytesToKbOperation.self)
        register(BytesToMbOperation.self)
        register(BytesToGbOperation.self)
        register(BytesToTbOperation.self)
        // Energy
        register(JoulesToCaloriesOperation.self)
        register(CaloriesToJoulesOperation.self)
        register(KwhToJoulesOperation.self)
        register(JoulesToKwhOperation.self)
        // Pressure
        register(PsiToPascalOperation.self)
        register(PascalToPsiOperation.self)
        register(BarToPascalOperation.self)
        register(PascalToBarOperation.self)

        // Geometry (15 operations)
        register(DistanceOperation.self)
        register(Distance3dOperation.self)
        register(AreaCircleOperation.self)
        register(CircumferenceOperation.self)
        register(AreaTriangleOperation.self)
        register(AreaTriangleHeronOperation.self)
        register(PythagoreanOperation.self)
        register(PythagoreanSideOperation.self)
        register(AreaRectangleOperation.self)
        register(PerimeterRectangleOperation.self)
        register(AreaSquareOperation.self)
        register(VolumeSphereOperation.self)
        register(SurfaceAreaSphereOperation.self)
        register(VolumeCylinderOperation.self)
        register(AreaRegularPolygonOperation.self)

        // Combinatorics (10 operations)
        register(CombinationsOperation.self)
        register(PermutationsOperation.self)
        register(FibonacciOperation.self)
        register(IsPrimeOperation.self)
        register(PrimeFactorsOperation.self)
        register(IsEvenOperation.self)
        register(IsOddOperation.self)
        register(IsPerfectSquareOperation.self)
        register(DigitSumOperation.self)
        register(ReverseNumberOperation.self)

        // Number Theory (15 operations)
        register(IsPrimeNTOperation.self)
        register(PrimeFactorsNTOperation.self)
        register(NextPrimeOperation.self)
        register(PrimeCountOperation.self)
        register(EulerPhiOperation.self)
        register(DivisorsOperation.self)
        register(PerfectNumberOperation.self)
        register(CatalanOperation.self)
        register(BellNumberOperation.self)
        register(StirlingOperation.self)
        register(PartitionOperation.self)
        register(MobiusOperation.self)
        register(TotientOperation.self)

        // Complex Numbers (18 operations)
        register(CaddOperation.self)
        register(CsubOperation.self)
        register(CmulOperation.self)
        register(CdivOperation.self)
        register(MagnitudeOperation.self)
        register(PhaseOperation.self)
        register(ConjugateOperation.self)
        register(PolarOperation.self)
        register(RectangularOperation.self)
        register(CsqrtOperation.self)
        register(CexpOperation.self)
        register(ClogOperation.self)
        register(CsinOperation.self)
        register(CcosOperation.self)
        register(CtanOperation.self)
        register(CpowerOperation.self)
        register(CisOperation.self)
        register(RealPartOperation.self)
        register(ImagPartOperation.self)

        // Variables (6 operations)
        register(SetOperation.self)
        register(PersistOperation.self)
        register(GetOperation.self)
        register(VarsOperation.self)
        register(UnsetOperation.self)
        register(ClearVarsOperation.self)

        // Control Flow (13 operations)
        register(EqOperation.self)
        register(NeqOperation.self)
        register(GtOperation.self)
        register(GteOperation.self)
        register(LtOperation.self)
        register(LteOperation.self)
        register(AndOperation.self)
        register(OrOperation.self)
        register(NotOperation.self)
        register(IfOperation.self)
        register(IsNumberOperation.self)
        register(IsStringOperation.self)
        register(IsBoolOperation.self)

        // User Functions (3 operations)
        register(DefOperation.self)
        register(FuncsOperation.self)
        register(UndefOperation.self)

        // Scripts (2 operations)
        register(RunOperation.self)
        register(EvalOperation.self)

        // Export/Integration (6 operations)
        register(ExportSessionOperation.self)
        register(ImportSessionOperation.self)
        register(ExportVarsOperation.self)
        register(ImportVarsOperation.self)
        register(ExportFuncsOperation.self)
        register(ImportFuncsOperation.self)

        // Matrix Operations (12 operations)
        register(DetOperation.self)
        register(TransposeOperation.self)
        register(EigenvaluesOperation.self)
        register(EigenvectorsOperation.self)
        register(TraceOperation.self)
        register(RankOperation.self)
        register(InverseOperation.self)
        register(MatrixMultiplyOperation.self)
        register(IdentityOperation.self)
        register(ZerosOperation.self)
        register(OnesOperation.self)
        register(DiagonalOperation.self)

        // Calculus (12 operations)
        register(DerivativeOperation.self)
        register(Derivative2Operation.self)
        register(PartialOperation.self)
        register(GradientOperation.self)
        register(DivergenceOperation.self)
        register(LaplacianOperation.self)
        register(IntegrateOperation.self)
        register(IntegrateSymbolicOperation.self)
        register(LimitOperation.self)
        register(TaylorOperation.self)
        register(SeriesOperation.self)
        register(SolveOdeOperation.self)

        // Data Analysis (12 operations)
        register(LoadDataOperation.self)
        register(DescribeDataOperation.self)
        register(CorrelationMatrixOperation.self)
        register(GroupByOperation.self)
        register(DetectOutliersOperation.self)
        register(MissingValuesOperation.self)
        register(PivotTableOperation.self)
        register(RollingMeanOperation.self)
        register(TimeSeriesAnalysisOperation.self)
        register(DataInfoOperation.self)
        register(SaveDataOperation.self)
        register(UniqueValuesOperation.self)

        // Data Transform (11 operations)
        register(FilterDataOperation.self)
        register(NormalizeDataOperation.self)
        register(SortDataOperation.self)
        register(AggregateDataOperation.self)
        register(FillNullsOperation.self)
        register(DropNullsOperation.self)
        register(MergeDataOperation.self)
        register(SampleDataOperation.self)
        register(AddColumnOperation.self)
        register(DropColumnOperation.self)
        register(RenameColumnOperation.self)

        // Plotting (8 operations)
        register(PlotHistOperation.self)
        register(PlotBoxOperation.self)
        register(PlotScatterOperation.self)
        register(PlotHeatmapOperation.self)
        register(PlotOperation.self)
        register(PlotLineOperation.self)
        register(PlotBarOperation.self)
        register(PlotDataOperation.self)
    }
}
