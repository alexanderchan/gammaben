# Run Gamma Enhanced Program Flow

```mermaid
flowchart TD
    A[🚀 Start: run_gamma_enhanced.sh] --> B[📊 Display welcome message]
    B --> C[🔧 Setup environment<br/>- Add uv to PATH<br/>- Activate gamma-env]
    C --> D[❓ User choice prompt<br/>1: Interactive display<br/>2: Save to files]

    D --> E{User Selection}
    E -->|Choice 1 or default| F[🖼️ Interactive Mode<br/>python gammaProfileCommandLine_enhanced.py SPX]
    E -->|Choice 2| G[💾 Save Mode<br/>python gammaProfileCommandLine_enhanced.py SPX --save]

    F --> H[📈 Python Script Execution]
    G --> H

    H --> I[🔄 Fetch SPX options data<br/>from CBOE API]
    I --> J[💰 Get spot price<br/>Calculate strike range<br/>80%-120% of spot]

    J --> K[📊 Parse options data<br/>- Extract calls/puts<br/>- Parse expiration dates<br/>- Extract strike prices]
    K --> L[🔗 Merge call/put data<br/>Validate matching strikes/expirations]

    L --> M[⚡ Calculate Gamma Exposure<br/>GEX = Gamma × OI × 100 × Spot² × 0.01]
    M --> N[📊 Generate 4 Charts]

    N --> O[Chart 1: Total Gamma Exposure<br/>Bar chart by strike price]
    O --> P[Chart 2: Open Interest<br/>Calls vs Puts by strike]
    P --> Q[Chart 3: Gamma by Type<br/>Call Gamma vs Put Gamma]
    Q --> R[Chart 4: Gamma Profile<br/>Exposure across price levels]

    R --> S{Save Mode?}
    S -->|Yes| T[💾 Save charts to<br/>gamma_charts/ directory]
    S -->|No| U[🖼️ Display charts<br/>interactively]

    T --> V[📁 Show file locations<br/>List saved chart files]
    U --> W[ℹ️ Show navigation tips<br/>Zoom, pan, reset instructions]

    V --> X[✅ Analysis Complete]
    W --> X

    subgraph "Key Calculations"
        Y[Black-Scholes Gamma<br/>calcGammaEx function]
        Z[Gamma Flip Point<br/>Zero-crossing analysis]
        AA[Third Friday Detection<br/>Monthly expiry logic]
    end

    subgraph "Data Processing"
        BB[Strike Price Filtering<br/>fromStrike to toStrike]
        CC[Days to Expiration<br/>Business day calculation]
        DD[Implied Volatility<br/>Call/Put IV processing]
    end

    M -.-> Y
    R -.-> Z
    K -.-> AA
    J -.-> BB
    L -.-> CC
    L -.-> DD

    style A fill:#e1f5fe
    style H fill:#f3e5f5
    style N fill:#e8f5e8
    style X fill:#fff3e0
```

## Program Components

### 1. Shell Script (`run_gamma_enhanced.sh`)

- **Purpose**: User interface and environment setup
- **Features**:
  - Interactive vs save mode selection
  - Virtual environment activation
  - User guidance and tips

### 2. Python Script (`gammaProfileCommandLine_enhanced.py`)

- **Purpose**: Core gamma analysis engine
- **Key Functions**:
  - `calcGammaEx()`: Black-Scholes gamma calculation
  - `isThirdFriday()`: Monthly expiry detection
  - `save_or_show_chart()`: Chart output handling

### 3. Data Flow

1. **Data Acquisition**: Fetches live SPX options from CBOE API
2. **Data Processing**: Parses and validates call/put option pairs
3. **Gamma Calculation**: Computes exposure using Black-Scholes model
4. **Visualization**: Generates 4 comprehensive charts
5. **Output**: Interactive display or file saving

### 4. Chart Types Generated

- **Chart 1**: Total gamma exposure by strike price
- **Chart 2**: Open interest distribution (calls vs puts)
- **Chart 3**: Gamma exposure by option type
- **Chart 4**: Gamma profile across price levels with flip point

### 5. Key Metrics Calculated

- **Total Gamma Exposure**: Dollar impact per 1% index move
- **Gamma Flip Point**: Price level where gamma changes sign
- **Strike Range**: 80%-120% of current spot price
- **Expiration Analysis**: Current vs future expiries
