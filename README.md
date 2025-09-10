# Vendor Performance Analysis Project

This project analyzes vendor performance data using Python, Jupyter notebooks, and Power BI visualizations.

## Project Structure

```
vendorProject/
├── ExploratoryDataAnalysis.ipynb    # Initial data exploration and analysis
├── VendorPerformanceAnalysis.ipynb  # Main vendor performance analysis
├── notebook.ipynb                   # Additional analysis notebook
├── get_vendor_summary.py            # Python script for vendor data summarization
├── ingestion_db.py                  # Database ingestion utilities
├── vendorSales.pbix                 # Power BI dashboard
├── vendorSales.pdf                  # Generated report
├── data/                            # Data directory (excluded from git)
├── logs/                            # Log files (excluded from git)
└── README.md                        # This file
```

## Features

- **Data Analysis**: Comprehensive vendor performance analysis using Python and pandas
- **Jupyter Notebooks**: Interactive analysis and visualization notebooks
- **Database Integration**: SQLite database for vendor data storage
- **Power BI Dashboard**: Interactive business intelligence dashboard
- **Automated Reporting**: Scripts for generating vendor summaries

## Requirements

- Python 3.x
- Jupyter Notebook
- pandas
- sqlite3
- Power BI Desktop (for .pbix files)

## Getting Started

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd vendorProject
   ```

2. Install required Python packages:
   ```bash
   pip install pandas jupyter sqlite3
   ```

3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. Open the analysis notebooks:
   - Start with `ExploratoryDataAnalysis.ipynb` for initial data exploration
   - Use `VendorPerformanceAnalysis.ipynb` for detailed performance analysis

## Usage

### Running the Analysis

1. **Data Ingestion**: Use `ingestion_db.py` to load data into the SQLite database
2. **Vendor Summary**: Run `get_vendor_summary.py` to generate vendor performance summaries
3. **Interactive Analysis**: Open the Jupyter notebooks for detailed analysis and visualization

### Power BI Dashboard

Open `vendorSales.pbix` in Power BI Desktop to view the interactive dashboard with vendor performance metrics and visualizations.
Since the file is too large, the pdf file `vendorSales.pdf` is included

## Data Files

Note: Large data files (*.db, *.csv) are excluded from version control. Make sure to:
- Place your vendor data in the `data/` directory
- Run the ingestion scripts to populate the database
- Ensure data files are available locally for analysis

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis feature'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## License

This project is for internal vendor analysis purposes.

## Contact

For questions about this analysis, please contact @dishansarkar9@gmail.com
