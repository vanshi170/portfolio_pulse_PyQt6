# PortfolioPulse

PortfolioPulse is a premium desktop application built with Python and PyQt6 for tracking and analyzing stock market portfolios. It features a modern, responsive, glassmorphic user interface, dynamic SVG icon generation, dual-theme support (Dark/Light), multi-currency localization, and detailed analytical charting tools.

## Core Features

* **Dynamic Portfolio Tracking:** Add, remove, and track holdings with real-time aggregated metrics.
* **Analytical Dashboard:** View aggregated high-level statistics including total value, largest positions, and average investments presented in clean, flashcard-style UI components.
* **Interactive Charting:** Built-in integration with Matplotlib allows for interactive pie charts to visualize portfolio allocations by asset and monetary value.
* **Advanced Theming System:** Features robust QSS-driven stylesheet implementations. It supports a true Dark Mode and a high-contrast Light Mode, completely integrated with a custom dynamic SVG generation engine.
* **Multi-Currency Support:** Dynamically switch base currencies (USD, INR, EUR, GBP). All historical and current tracking recalculates values seamlessly.
* **Robust Storage Layer:** Stores session, configuration, and statistical data locally using a lightweight JSON-based file system.
* **Data Portability:** Complete Export/Import Center supporting JSON, CSV, and TXT outputs.

## Architecture and Concepts

The application is architected utilizing the Model-View-Controller (MVC) paradigm alongside specialized service classes, allowing strict separation between UI rendering and business logic.

### 1. The Service Layer
Handles the core business logic of the application.
* **`PortfolioManager`**: The central controller that manages stock queries, calculates total valuation based on hardcoded asset prices, calculates allocation percentages, and interfaces with the underlying storage layer.
* **`IconGenerator`**: A programmatic SVG rendering engine. Upon startup, it generates purely vector-based GUI assets adapted to the active application theme.

### 2. The Storage Layer
A persistent JSON-backed file storage mechanism located within the `data/` directory.
* **`PortfolioStorage`**: Manages the CRUD (Create, Read, Update, Delete) operations for user stock holdings.
* **`Settings`**: A lightweight local configuration manager holding active parameters (e.g., UI Theme, selected Currency).
* **`Statistics`**: Tracks usage telemetry over the lifetime of the application installation.

### 3. The Presentation Layer (UI)
Constructed heavily using PyQt6 and Qt Designer concepts.
* **`MainWindow`**: The main application shell managing the `QStackedWidget` navigation paradigm.
* **Pages**: Isolated visual components (`DashboardPage`, `PortfolioPage`, `AnalyticsPage`, `SettingsPage`, `ExportCenterPage`, `AboutPage`) that contain localized layout rendering.
* **Components**: Reusable, atomic Qt widgets like custom sidebars, custom sliding toast notifications, and scalable vector labels.

## Folder Structure

The repository maintains a highly decoupled organizational structure:

```text
portfolio_manager/
│
├── main.py                     # Application entry point and bootstrapping script
├── requirements.txt            # Python dependency definitions
├── .gitignore                  # Excluded git tracking definitions
│
├── services/                   # Business logic and external service integrations
│   ├── portfolio_manager.py    # Core portfolio orchestration logic
│   ├── icon_generator.py       # Algorithmic SVG generation code
│   └── export_import_manager.py# CSV/JSON file formatting and parsing logic
│
├── storage/                    # Persistent data storage implementation
│   ├── portfolio_storage.py    # Local JSON operations for portfolio arrays
│   ├── settings.py             # User configuration file operations
│   └── statistics.py           # Application telemetry operations
│
├── ui/                         # User Interface definitions and widgets
│   ├── main_window.py          # Primary application routing shell
│   ├── dashboard_page.py       # High-level statistical views
│   ├── portfolio_page.py       # Interactive QTableWidget for holding management
│   ├── analytics_page.py       # Matplotlib allocation charting
│   ├── export_center_page.py   # Data porting interface
│   ├── settings_page.py        # Application configuration interface
│   ├── about_page.py           # Legal and informational interface
│   │
│   └── components/             # Reusable atomic UI elements
│       ├── sidebar.py          # Navigational routing component
│       └── toast.py            # Animated sliding notification component
│
├── styles/                     # QSS Style Sheets
│   ├── dark.qss                # Black/Grey theme variables and properties
│   └── light.qss               # White/Grey theme variables and properties
│
└── assets/                     # Automatically generated at runtime
    ├── generated/              # Contains the dynamically created App Icon
    └── icons/                  # Contains dark/light adaptive SVG files
```

*Note: The `data/` directory and `assets/` directory are deliberately omitted from source control as they are constructed dynamically upon runtime initialization based on user state.*

## Installation and Execution

### Prerequisites
* Python 3.10 or higher.
* `pip` package manager.

### 1. Environment Setup
It is highly recommended to isolate the application dependencies using a Python virtual environment.

```bash
# Initialize a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate
```

### 2. Dependency Installation
Install all required packages from the included requirements file.

```bash
pip install -r requirements.txt
```

### 3. Application Launch
Execute the main bootstrapping script to start the application. Note that on the very first execution, the `IconGenerator` and `Storage` subsystems will construct their respective runtime assets.

```bash
python main.py
```

## System Workflow and Initialization Sequence

When `main.py` is executed, the following sequence occurs:

1. **Bootstrapping**: The `QApplication` event loop is initialized.
2. **Directory Integrity**: Required directories (`data/`, `assets/`, `styles/`) are validated or created.
3. **Asset Generation**: The `IconGenerator` executes. It calculates required dimensions and path instructions, generating scalable XML `.svg` files dynamically based on expected constants.
4. **Window Instantiation**: `MainWindow` mounts the persistent `Sidebar` and initializes a hidden `QStackedWidget` loaded with pre-instantiated page modules.
5. **Theming Engine**: The stylesheet (`.qss`) associated with the active theme parameter in `data/settings.json` is loaded into the `MainWindow` styling buffer. Icons are triggered to refresh dynamically to map to the loaded style variables.
6. **Execution**: The GUI thread assumes control, awaiting user input.

## Advanced Modifications

* **Adding New Stocks**: To augment the hardcoded price dictionary, simply modify the static dictionary within the `PortfolioManager` initialization logic. The user interface will automatically identify and integrate the new symbols into the comboboxes and validation filters.
* **Modifying Themes**: Visual modifications can be safely made directly inside `styles/dark.qss` and `styles/light.qss` using standard Qt Style Sheet conventions (which heavily mirror standard CSS).
