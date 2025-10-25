# Math CLI - Remaining Work & Future Development Plan

**Last Updated:** 2025-01-25
**Status:** Planning Phase
**Current Version:** Phase 5.4 (Export features complete)

---

## Overview

This document outlines the remaining planned features for Math CLI, organized into three major tracks:

1. **Phase 5.4 (Remaining)** - Complete Integration & Connectivity features
2. **Phase 5.5** - AI/ML Intelligence Features
3. **Phase 5.6 (NEW)** - Web UI & Full Web Application

---

# Phase 5.4 (Remaining): Integration & Connectivity

**Priority:** MEDIUM | **Duration:** 2-3 weeks | **Complexity:** Medium-High

## Status

**Completed:**
- ✅ Export formats (JSON, Markdown, LaTeX)
- ✅ Session export/import
- ✅ Variable/function export/import

**Remaining Work:**
- ⏸️ API integrations
- ⏸️ Cloud sync
- ⏸️ Jupyter kernel integration

---

## Track 1: API Integrations

### Goals
Connect Math CLI to external mathematical services and APIs for advanced computations beyond local capabilities.

### Features

#### 1.1 Wolfram Alpha Integration
**Module:** `integrations/wolfram_client.py`

**Capabilities:**
```bash
# Query Wolfram Alpha for complex calculations
python math_cli.py wolfram "integrate x^2 from 0 to 10"
python math_cli.py wolfram "solve x^2 + 5x + 6 = 0"
python math_cli.py wolfram "derivative of sin(x)*cos(x)"

# Short-form queries
python math_cli.py wolfram "population of Tokyo"
python math_cli.py wolfram "speed of light in meters per second"
```

**Implementation Steps:**
1. Create Wolfram Alpha API client wrapper
2. Implement API key management (environment variables, config file)
3. Add request/response parsing
4. Implement result formatting for CLI display
5. Add caching to reduce API calls (SQLite cache)
6. Implement rate limiting (max queries per minute)
7. Add error handling for API failures
8. Create fallback to local operations when possible

**Configuration:**
```json
{
  "wolfram_alpha": {
    "api_key": "${WOLFRAM_API_KEY}",
    "cache_ttl": 86400,
    "rate_limit": 60,
    "timeout": 10
  }
}
```

#### 1.2 Other API Integrations
**Module:** `integrations/api_registry.py`

**Potential APIs:**
- **Numbers API** - Interesting math facts: `fact_about 42`
- **Exchange Rate API** - Currency conversions: `convert_currency 100 USD EUR`
- **Unit Conversion API** - Advanced unit conversions
- **Mathematical Constants DB** - Extended constants library

**Implementation Steps:**
1. Create generic API client framework
2. Implement plugin system for API providers
3. Add unified error handling
4. Create response normalizers
5. Implement multi-provider fallback

### Dependencies
```
requests>=2.31.0          # HTTP client
python-dotenv>=1.0.0      # Environment variable management
requests-cache>=1.1.0     # API response caching
ratelimit>=2.2.1          # Rate limiting
```

### Testing Strategy
- Mock API responses for unit tests
- Integration tests with real API (CI only)
- Cache hit/miss testing
- Rate limiting verification
- Error handling scenarios

### Success Metrics
- [x] Wolfram Alpha integration working
- [x] API key management secure
- [x] Caching reduces duplicate calls by 80%+
- [x] Rate limiting prevents API abuse
- [x] Error handling graceful for all failure modes

---

## Track 2: Cloud Sync

### Goals
Enable synchronization of user data (history, functions, preferences) across devices.

### Features

#### 2.1 Local File-Based Sync
**Module:** `cloud/file_sync.py`

**Capabilities:**
```bash
# Configure sync location
python math_cli.py sync_config --provider=dropbox --path=~/Dropbox/MathCLI

# Manual sync
python math_cli.py sync_push    # Upload local state
python math_cli.py sync_pull    # Download remote state
python math_cli.py sync_auto    # Enable automatic sync

# Sync status
python math_cli.py sync_status
```

**Sync Data:**
- Command history (`.mathcli/history.json`)
- User-defined functions (`.mathcli/functions.json`)
- Persistent variables (`.mathcli/variables.json`)
- Custom themes/preferences (`.mathcli/config.json`)
- Script files (`.mathcli/scripts/`)

**Supported Providers:**
1. **Dropbox** - Sync via local Dropbox folder
2. **Google Drive** - Sync via local Drive folder
3. **OneDrive** - Sync via local OneDrive folder
4. **Git** - Version control for scripts/functions
5. **Custom** - Any folder path

#### 2.2 Conflict Resolution
**Module:** `cloud/conflict_resolver.py`

**Strategies:**
- **Last Write Wins** - Most recent timestamp wins
- **Manual Merge** - User chooses which version
- **Auto Merge** - Merge non-conflicting changes
- **Keep Both** - Preserve both versions with timestamps

**Example Conflict:**
```
Sync conflict detected:
  Local:  function square(x) = multiply $x $x (modified 2 mins ago)
  Remote: function square(x) = power $x 2 (modified 5 mins ago)

Choose resolution:
  1) Keep local
  2) Keep remote
  3) Keep both (rename remote to square_remote)
  4) Manual merge
```

#### 2.3 Encryption
**Module:** `cloud/encryption.py`

**Security:**
- Encrypt sensitive data before sync (variables, API keys)
- AES-256 encryption
- User-provided passphrase or keyfile
- Encrypted metadata to prevent data leakage

**Implementation Steps:**
1. Create sync framework with provider abstraction
2. Implement file watching for auto-sync
3. Add conflict detection and resolution
4. Implement encryption layer
5. Create sync status dashboard
6. Add bandwidth optimization (delta sync)
7. Implement version history (keep last N versions)

### Dependencies
```
watchdog>=3.0.0           # File system monitoring
cryptography>=41.0.0      # Encryption
gitpython>=3.1.0          # Git integration (optional)
```

### Testing Strategy
- Multi-device simulation
- Conflict generation and resolution
- Encryption/decryption verification
- Network failure recovery
- Data integrity checks

### Success Metrics
- [x] Sync working across 3+ providers
- [x] Conflict resolution handles 95%+ cases automatically
- [x] Encryption verified secure
- [x] Auto-sync detects changes within 5 seconds
- [x] Data integrity maintained across sync cycles

---

## Track 3: Jupyter Integration

### Goals
Make Math CLI available as a Jupyter kernel and magic command provider.

### Features

#### 3.1 Jupyter Kernel
**Module:** `integrations/jupyter_kernel.py`

**Installation:**
```bash
# Install Math CLI kernel
python math_cli.py install_kernel

# Use in Jupyter
jupyter notebook
# Select "Math CLI" kernel in new notebook
```

**Notebook Usage:**
```python
# In a Jupyter notebook with Math CLI kernel
add 5 3
# Output: 8

set x 10
multiply $x 5
# Output: 50

plot_function 'x**2' -10 10
# Displays inline plot
```

#### 3.2 IPython Magic Commands
**Module:** `integrations/ipython_magics.py`

**Installation:**
```python
# In IPython/Jupyter with Python kernel
%load_ext mathcli
```

**Magic Commands:**
```python
# Line magic
%mathcli add 5 3
# Output: 8

# Cell magic
%%mathcli
set radius 5
set pi 3.14159
multiply $pi (multiply $radius $radius)
# Output: Area = 78.53975

# Share variables with Python
x = 42
%mathcli set py_x {x}
%mathcli multiply $py_x 2
# Output: 84

# Get results back to Python
result = %mathcli sqrt 144
print(result)  # 12
```

#### 3.3 Rich Output Integration
**Features:**
- Display plots inline with Jupyter's display system
- Render LaTeX output in notebook cells
- Format tables as HTML for better display
- Syntax highlighting for Math CLI code
- Interactive widgets for complex inputs

**Implementation Steps:**
1. Create Jupyter kernel wrapper
2. Implement kernel protocol (IPython kernel base)
3. Add IPython magic command extensions
4. Integrate with Jupyter display system
5. Support bidirectional variable sharing
6. Add rich output formatting
7. Create kernel installation/uninstallation
8. Add kernel configuration options

### Dependencies
```
ipykernel>=6.25.0         # Jupyter kernel framework
IPython>=8.12.0           # IPython integration
ipywidgets>=8.1.0         # Interactive widgets
```

### Testing Strategy
- Kernel protocol compliance
- Variable sharing bidirectionally
- Plot rendering verification
- Magic command registration
- Multi-cell execution

### Success Metrics
- [x] Kernel installable and selectable in Jupyter
- [x] All Math CLI operations work in kernel
- [x] Magic commands registered and functional
- [x] Variables shared between Python and Math CLI
- [x] Plots display inline correctly
- [x] Rich output renders properly

---

# Phase 5.5: AI/ML Intelligence Features

**Priority:** MEDIUM | **Duration:** 3-4 weeks | **Complexity:** High

## Overview
Add artificial intelligence and machine learning capabilities to make Math CLI more intuitive, intelligent, and helpful.

---

## Track 1: Natural Language Processing

### Goals
Enable users to interact with Math CLI using natural language instead of command syntax.

### Features

#### 1.1 Natural Language Query Parser
**Module:** `ai/nlp_processor.py`

**Capabilities:**
```bash
# Natural language queries (interactive mode)
> "What is the square root of 144?"
# Interprets as: sqrt 144
# Output: 12

> "Calculate 25 percent of 80"
# Interprets as: multiply 80 0.25
# Output: 20

> "What's 15 plus 27 times 3?"
# Interprets as: add 15 (multiply 27 3)
# Output: 96

> "Convert 100 fahrenheit to celsius"
# Interprets as: fahrenheit_to_celsius 100
# Output: 37.78
```

#### 1.2 Command Interpretation
**Features:**
- **Intent Classification** - Determine what operation user wants
- **Entity Extraction** - Extract numbers, units, variables
- **Operator Mapping** - Map words to operations ("plus" → add, "times" → multiply)
- **Context Awareness** - Remember previous queries
- **Spell Correction** - Handle typos ("sqare root" → "square root")

**Synonym Understanding:**
```
"add" → add, plus, sum, total, combine
"multiply" → multiply, times, product
"divide" → divide, over, divided by, per
"power" → power, exponent, to the power of, raised to
```

#### 1.3 Conversational Interface
**Module:** `ai/conversation_manager.py`

**Capabilities:**
```bash
> "Calculate the area of a circle with radius 5"
# Sets context: working with circles, radius = 5

> "Now use radius 10"
# Updates context, recalculates

> "What if the radius was 15?"
# Further context update

> "Show me all the radii I tried"
# Output: 5, 10, 15
```

**Implementation Steps:**
1. Create NLP pipeline using lightweight models
2. Implement intent classifier (rule-based + ML)
3. Build entity extractor for math expressions
4. Create command translator (NL → Math CLI syntax)
5. Add context manager for conversational state
6. Implement spell correction using edit distance
7. Build synonym dictionary for mathematical terms
8. Add confidence scoring for interpretations
9. Create fallback to command mode for ambiguity

### Dependencies
```
transformers>=4.30.0      # Pre-trained NLP models (optional)
nltk>=3.8.1               # Natural language toolkit
spacy>=3.7.0              # Advanced NLP (optional)
fuzzywuzzy>=0.18.0        # Fuzzy string matching
python-Levenshtein>=0.21  # Fast edit distance
```

### Model Strategy
**Lightweight Approach (Recommended):**
- Rule-based intent classification
- Regex-based entity extraction
- Dictionary-based synonym mapping
- No large ML models (fast startup)

**Advanced Approach (Optional):**
- BERT/RoBERTa for intent classification
- NER models for entity extraction
- Embedding-based semantic search
- Requires model download (~500MB)

### Success Metrics
- [x] Query interpretation accuracy ≥ 80%
- [x] Handles 50+ common phrasings per operation
- [x] Spell correction catches 90%+ typos
- [x] Context maintained across 5+ turns
- [x] Response time < 100ms for rule-based, < 500ms for ML

---

## Track 2: Pattern Recognition & Smart Suggestions

### Goals
Detect patterns in user behavior and data, provide intelligent suggestions.

### Features

#### 2.1 Sequence Pattern Detection
**Module:** `ai/pattern_recognizer.py`

**Capabilities:**
```bash
> "Analyze this sequence: 2, 4, 8, 16, 32"
Pattern detected: Powers of 2
Formula: 2^n where n = 1, 2, 3, 4, 5
Next values: 64, 128, 256

> "What's the pattern? 1, 1, 2, 3, 5, 8, 13"
Pattern detected: Fibonacci sequence
Formula: F(n) = F(n-1) + F(n-2)
Next values: 21, 34, 55
```

**Pattern Types:**
- Arithmetic sequences (linear)
- Geometric sequences (exponential)
- Fibonacci-like sequences
- Polynomial patterns
- Factorial patterns
- Prime number sequences

#### 2.2 Formula Inference
**Module:** `ai/formula_inference.py`

**Capabilities:**
```bash
> load_data sales.csv
> "Infer relationship between price and sales"

Analysis Results:
  Pattern: Negative correlation
  Suggested formula: sales = 1000 - 25 * price
  R² = 0.89
  Recommendation: Use linear_regression for precise model
```

#### 2.3 Smart Autocomplete
**Module:** `ai/suggestion_engine.py`

**Features:**
- **Context-aware suggestions** - Based on current workflow
- **Next operation prediction** - "You usually do X after Y"
- **Parameter suggestions** - Common values for operations
- **Error prevention** - Warn about likely mistakes

**Example:**
```bash
> set x 10
> set y 20
> add [TAB]
Suggestions:
  add $x $y          (Variables in scope)
  add 5 3            (Recent similar)
  add $x 5           (Common pattern)
```

#### 2.4 Anomaly Detection
**Module:** `ai/anomaly_detector.py`

**Capabilities:**
```bash
> load_data sensor_readings.csv
> "Check for anomalies in temperature column"

Anomalies detected (3):
  Row 47:  temperature = 150.2 (expected: 20-30)
  Row 103: temperature = -50.7 (expected: 20-30)
  Row 244: temperature = 999.9 (likely sensor error)

Recommendation: Filter or investigate these values
```

**Implementation Steps:**
1. Create pattern recognition engine
2. Implement sequence analyzers (arithmetic, geometric, etc.)
3. Build formula inference using regression
4. Create smart autocomplete with context
5. Implement prediction models for next operations
6. Add anomaly detection using statistical methods
7. Build suggestion ranking system
8. Create user feedback loop for learning

### Dependencies
```
scikit-learn>=1.3.0       # ML algorithms
statsmodels>=0.14.0       # Statistical models
```

### Success Metrics
- [x] Sequence pattern detection ≥ 90% accuracy
- [x] Formula inference R² ≥ 0.7 for linear relationships
- [x] Autocomplete suggestions relevant 80%+ of time
- [x] Anomaly detection with <5% false positives

---

## Track 3: Mathematical Assistant

### Goals
Provide educational support, step-by-step solutions, and concept explanations.

### Features

#### 3.1 Step-by-Step Solver
**Module:** `ai/step_solver.py`

**Capabilities:**
```bash
> "Solve x^2 - 5x + 6 = 0 step by step"

Solution:
Step 1: Identify equation type
  This is a quadratic equation: ax² + bx + c = 0
  Where a=1, b=-5, c=6

Step 2: Try factoring
  Find two numbers that multiply to 6 and add to -5
  Numbers: -2 and -3
  Factored form: (x - 2)(x - 3) = 0

Step 3: Solve for x
  x - 2 = 0  →  x = 2
  x - 3 = 0  →  x = 3

Answer: x = 2 or x = 3

Verification:
  (2)² - 5(2) + 6 = 4 - 10 + 6 = 0 ✓
  (3)² - 5(3) + 6 = 9 - 15 + 6 = 0 ✓
```

#### 3.2 Concept Explainer
**Module:** `ai/concept_explainer.py`

**Capabilities:**
```bash
> "What is an eigenvalue?"

Eigenvalue (noun):
  A scalar λ that, when multiplied by an eigenvector v,
  produces the same result as the matrix A multiplied by v.

Mathematical Definition:
  A·v = λ·v

In simple terms:
  When you transform a vector with a matrix, some vectors
  only get scaled (not rotated). The scaling factor is
  the eigenvalue.

Example:
  Matrix: [[2, 0], [0, 3]]
  Eigenvalues: 2 and 3
  This matrix stretches vectors by 2x in one direction
  and 3x in another.

Related concepts:
  - Eigenvector
  - Diagonalization
  - Principal Component Analysis (PCA)

Try it:
  eigenvalues [[2, 0], [0, 3]]
```

#### 3.3 Method Recommender
**Module:** `ai/method_recommender.py`

**Capabilities:**
```bash
> "I need to solve a system of 5 linear equations"

Recommendations:
  1. matrix_solve (BEST for your case)
     - Fast and accurate for linear systems
     - Handles up to 1000x1000 systems
     Example: matrix_solve [[...]] [...]

  2. gaussian_elimination
     - Shows step-by-step process
     - Educational, but slower
     Example: gaussian_elimination [[...]] [...]

  3. iterative_methods
     - Good for very large sparse systems
     - Use if matrix_solve fails
     Example: jacobi_method [[...]] [...]

Why matrix_solve is best:
  - Your system is small (5 equations)
  - You want accurate results
  - No special structure to exploit
```

#### 3.4 Interactive Tutorials
**Module:** `ai/tutorial_system.py`

**Capabilities:**
```bash
> "Teach me about derivatives"

Tutorial: Introduction to Derivatives
======================================

Lesson 1: What is a derivative?
  A derivative measures how a function changes as its
  input changes. It's the slope of the function.

  Try it yourself:
  > derivative x^2 x

  Great! The derivative of x² is 2x.
  This means the slope at x=3 is 2(3) = 6.

Lesson 2: Derivative rules
  1. Power rule: d/dx(x^n) = n*x^(n-1)
  2. Sum rule: d/dx(f + g) = f' + g'
  3. Product rule: d/dx(f*g) = f'g + fg'

  Exercise: Find the derivative of x³
  > derivative x^3 x

  Correct! ✓

Continue to Lesson 3? (y/n)
```

**Implementation Steps:**
1. Create step-by-step solver framework
2. Implement solution strategies for common problem types
3. Build concept knowledge base (JSON/YAML)
4. Create explanation generator
5. Implement method recommendation system
6. Build interactive tutorial engine
7. Add progress tracking for tutorials
8. Create visualization for solutions

### Dependencies
```
sympy>=1.12              # Symbolic mathematics
networkx>=3.1            # Concept graph
```

### Knowledge Base
- Mathematical concepts (500+ entries)
- Solution strategies (100+ problem types)
- Step-by-step templates
- Visualization recipes

### Success Metrics
- [x] Step-by-step solver handles 20+ problem types
- [x] Concept explanations for 100+ terms
- [x] Method recommender suggests correct approach 85%+ of time
- [x] Tutorials maintain user engagement (completion rate ≥ 60%)

---

## Track 4: Predictive Analytics (Basic ML)

### Goals
Provide basic machine learning capabilities for prediction and analysis.

### Features

#### 4.1 Time Series Forecasting
**Module:** `ai/forecasting.py`

**Capabilities:**
```bash
> load_data sales_history.csv
> forecast data sales 12
# Forecast next 12 periods

Forecast Results:
  Method: ARIMA(1,1,1)
  Periods: 12

  Period  Forecast  Lower_CI  Upper_CI
  ------  --------  --------  --------
    13      1250      1180      1320
    14      1280      1200      1360
    15      1310      1220      1400
    ...

  Confidence: 95%
  Mean Absolute Error: 45.2
```

**Methods:**
- ARIMA models
- Exponential smoothing
- Linear trend
- Seasonal decomposition

#### 4.2 Classification & Regression
**Module:** `ai/ml_models.py`

**Capabilities:**
```bash
> load_data customers.csv
> train_classifier data target=purchased features=[age,income]

Model Training Results:
  Model: Random Forest Classifier
  Accuracy: 87.3%
  Precision: 0.85
  Recall: 0.82
  F1 Score: 0.83

  Feature Importance:
    income: 0.68
    age:    0.32

> predict_class model new_customer.csv
Predictions: [1, 0, 1, 1, 0]
```

**Supported Algorithms:**
- Logistic Regression
- Random Forest
- Decision Trees
- k-Nearest Neighbors
- Support Vector Machines

#### 4.3 Clustering Analysis
**Module:** `ai/clustering.py`

**Capabilities:**
```bash
> load_data customer_data.csv
> cluster data n_clusters=3 features=[spending,frequency]

Clustering Results:
  Algorithm: K-Means
  Clusters: 3

  Cluster 0: 234 customers (High-value)
    Avg spending: $1,245
    Avg frequency: 15 purchases/year

  Cluster 1: 456 customers (Medium-value)
    Avg spending: $420
    Avg frequency: 6 purchases/year

  Cluster 2: 310 customers (Low-value)
    Avg spending: $85
    Avg frequency: 2 purchases/year

  Silhouette Score: 0.67 (good separation)
```

**Implementation Steps:**
1. Create ML model framework
2. Implement scikit-learn wrappers for common models
3. Add model training and evaluation operations
4. Create prediction operations
5. Implement model persistence (save/load)
6. Add hyperparameter tuning (basic grid search)
7. Create model visualization (feature importance, etc.)
8. Add model comparison utilities

### Dependencies
```
scikit-learn>=1.3.0       # ML algorithms
xgboost>=2.0.0            # Gradient boosting (optional)
statsmodels>=0.14.0       # Time series
```

### Success Metrics
- [x] Time series forecasting with MAPE < 15%
- [x] Classification models achieve 80%+ accuracy on test sets
- [x] Clustering produces meaningful segments
- [x] Model training completes in < 30 seconds for datasets < 10k rows

---

# Phase 5.6 (NEW): Web UI & Full Web Application

**Priority:** MEDIUM-HIGH | **Duration:** 4-6 weeks | **Complexity:** Medium-High

## Overview
Create a local web UI that can evolve into a full-featured web application, enabling browser-based access to Math CLI with potential for cloud deployment.

## Progressive Development Strategy

### Phase 5.6.1: Local Web UI (Week 1-2)
**Goal:** Basic browser interface running locally

### Phase 5.6.2: Enhanced Web UI (Week 3-4)
**Goal:** Rich interactive features and visualizations

### Phase 5.6.3: Full Web App (Week 5-6)
**Goal:** Multi-user, cloud-ready application

---

## Phase 5.6.1: Local Web UI

### Goals
Create a lightweight web interface that runs locally on the user's machine, providing a browser-based alternative to the CLI.

### Architecture

```
┌─────────────────┐
│   Browser UI    │ (React/Vue/Svelte)
└────────┬────────┘
         │ HTTP/WebSocket
┌────────┴────────┐
│  FastAPI Server │ (Python)
└────────┬────────┘
         │
┌────────┴────────┐
│  Math CLI Core  │ (Existing)
└─────────────────┘
```

### Features

#### 1.1 Basic Calculator Interface
**Component:** `web/ui/Calculator.jsx`

**Features:**
- Clean, minimal UI with operation buttons
- Input field for direct command entry
- History panel showing recent calculations
- Result display with formatting
- Support for keyboard shortcuts

**UI Layout:**
```
┌──────────────────────────────────────┐
│  Math CLI Web                     ⚙️ │
├──────────────────────────────────────┤
│                                      │
│  Input: add 5 3              [Run]  │
│                                      │
│  Result: 8                           │
│                                      │
├──────────────────────────────────────┤
│  History                             │
│  ─────────────────────────────────   │
│  > add 5 3            → 8            │
│  > sqrt 144           → 12           │
│  > power 2 8          → 256          │
│                                      │
└──────────────────────────────────────┘
```

#### 1.2 Backend API Server
**Module:** `web/server.py`

**Framework:** FastAPI (lightweight, async, auto-docs)

**Endpoints:**
```python
# Execute operation
POST /api/execute
{
  "operation": "add",
  "args": [5, 3]
}
Response: {"result": 8, "execution_time": 0.002}

# Get operation list
GET /api/operations
Response: {"operations": [...], "categories": [...]}

# Get history
GET /api/history
Response: {"history": [...]}

# WebSocket for real-time
WS /api/ws
```

#### 1.3 Session Management
**Module:** `web/session_manager.py`

**Features:**
- Browser-based sessions (localStorage)
- Persist variables across page reloads
- Save/load session state
- Multiple session support (tabs)

#### 1.4 Launch Command
**New CLI Command:**
```bash
# Start web server
python math_cli.py web --port 8080
# Opens browser to http://localhost:8080

# Options
python math_cli.py web --port 8080 --no-browser  # Don't auto-open
python math_cli.py web --host 0.0.0.0            # Allow network access
```

**Implementation Steps:**
1. Create FastAPI backend server
2. Implement API endpoints for operations
3. Add WebSocket support for real-time updates
4. Build basic React/Vue frontend
5. Implement session management
6. Add operation browser/search
7. Create responsive mobile layout
8. Add keyboard shortcuts
9. Implement auto-save/restore
10. Add error display and handling

### Tech Stack

**Backend:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- WebSockets (real-time communication)
- CORS middleware (security)

**Frontend:**
- React with Vite (fast, modern) OR
- Vue 3 (simpler learning curve) OR
- Svelte (smallest bundle)
- TailwindCSS (styling)
- Chart.js (basic plots)

**Choice Recommendation:** **React + Vite** (most ecosystem support)

### Dependencies
```python
# Backend
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
websockets>=12.0
python-multipart>=0.0.6

# Frontend (npm)
react>=18.2.0
vite>=5.0.0
tailwindcss>=3.3.0
axios>=1.6.0
```

### File Structure
```
web/
├── server.py              # FastAPI application
├── api/
│   ├── routes.py          # API endpoints
│   ├── websocket.py       # WebSocket handler
│   └── models.py          # Request/response models
├── session_manager.py     # Session handling
├── static/                # Built frontend files
└── ui/                    # React source
    ├── src/
    │   ├── components/
    │   │   ├── Calculator.jsx
    │   │   ├── History.jsx
    │   │   ├── OperationBrowser.jsx
    │   │   └── ResultDisplay.jsx
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

### Success Metrics
- [x] Web UI launches in < 3 seconds
- [x] All CLI operations accessible via UI
- [x] Response time < 100ms for operations
- [x] UI works on desktop and mobile
- [x] Session persists across reloads

---

## Phase 5.6.2: Enhanced Web UI

### Goals
Add advanced features: plotting, scripting, data visualization, rich output.

### Features

#### 2.1 Interactive Plotting
**Component:** `web/ui/PlotViewer.jsx`

**Features:**
- Inline plot rendering with Plotly.js
- Interactive zoom, pan, hover tooltips
- Multiple plot types (line, bar, scatter, heatmap)
- Export plots as PNG/SVG
- Plot customization (colors, labels, legends)

**UI:**
```
┌──────────────────────────────────────┐
│  plot_function 'x**2' -10 10         │
├──────────────────────────────────────┤
│  ┌────────────────────────────────┐  │
│  │        y = x²                  │  │
│  │   100┤            ╱╲           │  │
│  │      │           ╱  ╲          │  │
│  │    50┤          ╱    ╲         │  │
│  │      │         ╱      ╲        │  │
│  │     0┼────────┴────────┴────   │  │
│  │     -10      0        10       │  │
│  └────────────────────────────────┘  │
│  [Download PNG] [Download SVG]       │
└──────────────────────────────────────┘
```

#### 2.2 Script Editor
**Component:** `web/ui/ScriptEditor.jsx`

**Features:**
- Monaco Editor (VS Code editor component)
- Syntax highlighting for .mathcli files
- Autocomplete for operations
- Run scripts from editor
- Save/load scripts
- Line-by-line execution
- Breakpoint support

**UI:**
```
┌──────────────────────────────────────┐
│  Script Editor              [Run] [Save] │
├──────────────────────────────────────┤
│  1  # Calculate compound interest    │
│  2  set principal 1000                │
│  3  set rate 0.05                     │
│  4  set years 10                      │
│  5  set amount = multiply $principal  │
│  6      (power (add 1 $rate) $years)  │
│  7                                     │
├──────────────────────────────────────┤
│  Output:                              │
│  > Line 5: amount = 1628.89           │
└──────────────────────────────────────┘
```

#### 2.3 Data Table Viewer
**Component:** `web/ui/DataTable.jsx`

**Features:**
- Display DataFrames as interactive tables
- Sorting, filtering, searching
- Pagination for large datasets
- Export to CSV/Excel
- Inline editing (for data manipulation)
- Column statistics on hover

#### 2.4 Variable Explorer
**Component:** `web/ui/VariableExplorer.jsx`

**Features:**
- Tree view of all variables
- Type indicators (number, string, array, DataFrame)
- Quick actions (delete, edit, export)
- Search and filter
- Memory usage display

**UI:**
```
┌──────────────────────────────────────┐
│  Variables                    [Clear] │
├──────────────────────────────────────┤
│  📊 Data                              │
│  ├─ sales_data      DataFrame (100x5)│
│  └─ results         DataFrame (50x3) │
│                                       │
│  🔢 Numbers                           │
│  ├─ x               10                │
│  ├─ y               20                │
│  └─ pi              3.14159           │
│                                       │
│  🔤 Strings                           │
│  └─ name            "test"            │
└──────────────────────────────────────┘
```

#### 2.5 Operation Browser
**Component:** `web/ui/OperationBrowser.jsx`

**Features:**
- Categorized operation list
- Search and filter
- Operation help/documentation inline
- Quick insert to input
- Examples for each operation
- Favorites/recent operations

**Implementation Steps:**
1. Integrate Plotly.js for interactive plots
2. Add Monaco Editor for script editing
3. Create data table component with ag-Grid
4. Build variable explorer with tree view
5. Implement operation browser with search
6. Add export functionality (plots, data, scripts)
7. Create keyboard shortcut system
8. Add dark/light theme toggle
9. Implement responsive layout for mobile

### Dependencies
```javascript
// Frontend (npm)
plotly.js>=2.27.0          // Interactive plotting
monaco-editor>=0.44.0      // Code editor
ag-grid-react>=30.2.0      // Data tables
react-icons>=4.12.0        // Icons
zustand>=4.4.0             // State management
```

### Success Metrics
- [x] Plots render in < 500ms
- [x] Script editor supports 1000+ line files
- [x] Data tables handle 10k+ rows smoothly
- [x] Variable explorer updates in real-time
- [x] Operation browser searchable and fast

---

## Phase 5.6.3: Full Web Application

### Goals
Transform the local web UI into a full-featured web application with multi-user support, cloud deployment, and collaboration features.

### Architecture

```
                    ┌─────────────┐
                    │   Browser   │
                    └──────┬──────┘
                           │ HTTPS
                    ┌──────┴──────┐
                    │  CDN/NGINX  │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────┴────┐      ┌──────┴──────┐    ┌─────┴─────┐
   │  React  │      │   FastAPI   │    │   Redis   │
   │  SPA    │      │   Backend   │    │  (Cache)  │
   └─────────┘      └──────┬──────┘    └───────────┘
                           │
                    ┌──────┴──────┐
                    │  PostgreSQL │
                    │  (Database) │
                    └─────────────┘
```

### Features

#### 3.1 User Authentication & Authorization
**Module:** `web/auth.py`

**Features:**
```bash
# User registration
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}

# User login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}
Response: {"access_token": "...", "refresh_token": "..."}

# OAuth integration
GET /api/auth/oauth/google
GET /api/auth/oauth/github
```

**Security:**
- JWT tokens (access + refresh)
- Password hashing (bcrypt)
- OAuth 2.0 (Google, GitHub)
- Rate limiting per user
- Session management
- CSRF protection

#### 3.2 Multi-User Database
**Module:** `web/database.py`

**Schema:**
```sql
-- Users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  name VARCHAR,
  created_at TIMESTAMP,
  settings JSONB
);

-- User sessions
CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  name VARCHAR,
  data JSONB,  -- variables, functions, history
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Saved scripts
CREATE TABLE scripts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  name VARCHAR NOT NULL,
  content TEXT,
  is_public BOOLEAN DEFAULT false,
  created_at TIMESTAMP
);

-- Shared calculations
CREATE TABLE shared_calculations (
  id UUID PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR,
  operations JSONB,
  results JSONB,
  created_at TIMESTAMP,
  expires_at TIMESTAMP
);
```

#### 3.3 Cloud Persistence
**Module:** `web/cloud_storage.py`

**Features:**
- Auto-save sessions to cloud
- Sync across devices automatically
- Version history (last 10 versions)
- Conflict resolution
- Backup and restore
- Export entire user data

**API:**
```bash
# Save session
POST /api/sessions/save
{
  "name": "My Analysis",
  "data": {...}
}

# Load session
GET /api/sessions/{session_id}

# List user sessions
GET /api/sessions
Response: [
  {"id": 1, "name": "My Analysis", "updated_at": "..."},
  {"id": 2, "name": "Budget Calc", "updated_at": "..."}
]

# Auto-save (WebSocket)
WS /api/ws/autosave
```

#### 3.4 Sharing & Collaboration
**Module:** `web/sharing.py`

**Features:**

**Share Calculations:**
```bash
# Create shareable link
POST /api/share/create
{
  "title": "Budget Analysis",
  "operations": [...],
  "results": [...],
  "expires_in": 604800  # 7 days
}
Response: {
  "share_url": "https://mathcli.app/s/abc123xyz",
  "qr_code": "data:image/png;base64,..."
}

# View shared calculation
GET /api/share/{share_id}
# Returns calculation with results, embeddable
```

**Collaborative Sessions (Future):**
- Real-time multi-user editing
- Shared workspaces
- Comments on calculations
- Activity feed

#### 3.5 Public Script Library
**Component:** `web/ui/ScriptLibrary.jsx`

**Features:**
- Browse public scripts by category
- Search scripts by keywords
- One-click import to your account
- Rate and comment on scripts
- Publish your own scripts
- Fork and modify public scripts

**Categories:**
- Finance & Economics
- Physics & Engineering
- Statistics & Data Science
- Education & Tutorials
- Games & Puzzles

#### 3.6 API for External Integration
**Module:** `web/public_api.py`

**REST API:**
```bash
# Execute operation (authenticated)
POST /api/v1/execute
Headers: Authorization: Bearer {api_key}
{
  "operation": "add",
  "args": [5, 3]
}

# Batch execution
POST /api/v1/batch
{
  "operations": [
    {"op": "add", "args": [5, 3]},
    {"op": "multiply", "args": [10, 2]}
  ]
}

# Webhooks (trigger on events)
POST /api/v1/webhooks/create
{
  "url": "https://your-app.com/webhook",
  "events": ["calculation_complete", "script_finish"]
}
```

**Rate Limiting:**
- Free tier: 100 requests/hour
- Pro tier: 10,000 requests/hour
- Enterprise: Unlimited

#### 3.7 Admin Dashboard
**Component:** `web/ui/Admin.jsx`

**Features:**
- User management
- Usage analytics
- System health monitoring
- Script moderation (review public scripts)
- Database maintenance
- Feature flags

**Implementation Steps:**
1. Set up PostgreSQL database
2. Implement user authentication (JWT)
3. Add OAuth providers (Google, GitHub)
4. Create user session management
5. Implement cloud persistence
6. Build sharing functionality
7. Create public API with rate limiting
8. Add admin dashboard
9. Implement billing/subscriptions (optional)
10. Add monitoring and logging
11. Set up CI/CD pipeline
12. Deploy to cloud (AWS/GCP/Azure)

### Deployment Architecture

**Options:**

**Option A: Simple (Recommended for MVP)**
```
Heroku/Railway/Render
├── Web dyno (FastAPI + React static)
├── PostgreSQL addon
└── Redis addon
```

**Option B: Scalable (Production)**
```
AWS/GCP/Azure
├── EC2/Compute Engine (FastAPI)
├── RDS/Cloud SQL (PostgreSQL)
├── ElastiCache/Memorystore (Redis)
├── S3/Cloud Storage (file uploads)
├── CloudFront/CDN (static assets)
└── Load Balancer
```

**Option C: Kubernetes (Enterprise)**
```
Kubernetes Cluster
├── FastAPI pods (auto-scaling)
├── PostgreSQL StatefulSet
├── Redis StatefulSet
├── NGINX Ingress
└── Monitoring (Prometheus + Grafana)
```

### Dependencies

**Backend:**
```python
# Database
sqlalchemy>=2.0.0          # ORM
alembic>=1.12.0            # Migrations
psycopg2-binary>=2.9.0     # PostgreSQL driver
redis>=5.0.0               # Caching

# Authentication
python-jose[cryptography]  # JWT
passlib[bcrypt]            # Password hashing
python-multipart           # Form data
authlib>=1.2.0             # OAuth

# Cloud deployment
gunicorn>=21.2.0           # WSGI server
sentry-sdk>=1.38.0         # Error tracking
prometheus-client>=0.19.0  # Metrics
```

**Frontend:**
```javascript
react-router-dom>=6.20.0   // Routing
react-query>=5.12.0        // Data fetching
react-hook-form>=7.48.0    // Forms
zod>=3.22.0                // Validation
```

### Success Metrics
- [x] User registration and login working
- [x] Sessions persisted to database
- [x] Multi-device sync functional
- [x] Sharing works with expiring links
- [x] Public API handles 1000+ req/min
- [x] Deployment stable with 99.9% uptime
- [x] Page load time < 2 seconds

---

# Implementation Timeline

## Phase 5.4 Remaining (2-3 weeks)
```
Week 1: API Integrations
├── Day 1-2: Wolfram Alpha client
├── Day 3-4: Caching and rate limiting
└── Day 5: Testing and documentation

Week 2: Cloud Sync
├── Day 1-2: File-based sync framework
├── Day 3-4: Conflict resolution
└── Day 5: Encryption and testing

Week 3: Jupyter Integration
├── Day 1-2: Jupyter kernel
├── Day 3-4: IPython magic commands
└── Day 5: Rich output and testing
```

## Phase 5.5 (3-4 weeks)
```
Week 1: NLP & Pattern Recognition
├── Day 1-3: Natural language parser
├── Day 4-5: Pattern recognition

Week 2: Smart Suggestions
├── Day 1-2: Autocomplete engine
├── Day 3-4: Anomaly detection
└── Day 5: Testing

Week 3: Mathematical Assistant
├── Day 1-2: Step-by-step solver
├── Day 3-4: Concept explainer
└── Day 5: Method recommender

Week 4: Predictive Analytics
├── Day 1-2: Forecasting models
├── Day 3-4: Classification/regression
└── Day 5: Clustering and testing
```

## Phase 5.6 (4-6 weeks)
```
Week 1-2: Local Web UI (Phase 5.6.1)
├── Day 1-3: FastAPI backend + React setup
├── Day 4-6: Basic calculator interface
├── Day 7-8: WebSocket real-time updates
└── Day 9-10: Session management and testing

Week 3-4: Enhanced Web UI (Phase 5.6.2)
├── Day 1-3: Interactive plotting
├── Day 4-6: Script editor with Monaco
├── Day 7-8: Data table viewer
└── Day 9-10: Variable explorer and polish

Week 5-6: Full Web App (Phase 5.6.3)
├── Day 1-3: Authentication and database
├── Day 4-6: Cloud persistence and sync
├── Day 7-8: Sharing and public API
└── Day 9-12: Deployment and production setup
```

---

# Resource Requirements

## Development Tools
- Code editor with TypeScript/React support
- PostgreSQL (local for development)
- Redis (local for development)
- Docker (for containerization)
- Postman/Insomnia (API testing)

## Cloud Resources (Phase 5.6.3)
- Domain name ($10-15/year)
- SSL certificate (free with Let's Encrypt)
- Cloud hosting:
  - Heroku/Railway: $7-25/month (start)
  - AWS/GCP: $50-200/month (production)
- Database: Included or $10-50/month
- CDN: Free tier or $5-20/month

## API Keys (Phase 5.4)
- Wolfram Alpha API: Free tier available
- OAuth apps: Free (Google, GitHub)

## Monitoring (Production)
- Sentry: Free tier or $26/month
- LogRocket: $99/month (optional)
- Uptime monitoring: Free tier available

---

# Success Criteria

## Phase 5.4 (Remaining)
- [x] Wolfram Alpha queries work with caching
- [x] Cloud sync operational across 3+ providers
- [x] Jupyter kernel installable and functional
- [x] All integrations tested and documented

## Phase 5.5
- [x] NLP interprets 80%+ of natural queries correctly
- [x] Pattern recognition identifies common sequences
- [x] Smart suggestions are contextually relevant
- [x] Math assistant provides helpful explanations
- [x] ML models train and predict successfully

## Phase 5.6
- [x] Local web UI accessible at localhost
- [x] Enhanced UI supports all CLI features
- [x] Full web app deployed and publicly accessible
- [x] Multi-user support with authentication
- [x] Sharing and collaboration working
- [x] Public API documented and functional

---

# Risk Mitigation

## Technical Risks
1. **API Dependencies** - Wolfram Alpha outages
   - Mitigation: Cache responses, fallback to local operations

2. **Scalability** - Web app performance under load
   - Mitigation: Load testing, horizontal scaling, caching

3. **Security** - User data protection
   - Mitigation: Encryption, security audits, HTTPS only

4. **Browser Compatibility** - UI issues across browsers
   - Mitigation: Cross-browser testing, progressive enhancement

## Business Risks
1. **Hosting Costs** - Cloud bills exceed budget
   - Mitigation: Usage monitoring, cost alerts, tier limits

2. **API Costs** - Wolfram Alpha quota exceeded
   - Mitigation: Aggressive caching, rate limiting

3. **Maintenance** - Time commitment for multi-user app
   - Mitigation: Automated deployment, monitoring, community support

---

# Future Enhancements (Post-5.6)

## Mobile Apps
- React Native mobile app (iOS/Android)
- Offline calculation support
- Camera input for equation recognition

## Desktop Apps
- Electron app for Windows/Mac/Linux
- System tray integration
- Offline mode with local database

## Enterprise Features
- Team workspaces
- Role-based access control
- Audit logs
- SSO integration (SAML, LDAP)
- Self-hosted option

## Advanced Features
- GPU acceleration for ML
- Custom plugin marketplace
- Visual programming interface (node-based)
- AI code generation for operations

---

**End of Plan**

*This plan will be updated as features are implemented and requirements evolve.*
