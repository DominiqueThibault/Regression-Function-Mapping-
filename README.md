# Regression Function Mapping

## Description
Assignment project for mapping training regression functions to ideal functions using least-squares 
optimization and deviation-based validation. 

## Features
- Least-Squares fitting
- Selection of the four best-fitting funcitons
- Test point assignment using √2 deviation constraint
- Residual analysis
- SQLite database integration (SQLALchemy ORM)
- Interactive visualization with Bokeh
- Styled HTML result tables

## Project Structure
.
├── main.py
├── model.py
├── evaluator.py
├── visualizer.py
├── database_orm.py
├── data_loader.py
├── requirements.txt
├── datasets/
└── outputs/

## Installation

Clone the repository
```bash
git clone <repository-url>
cd RegressionFunctionMapping
```

Install required packages

```bash
pip install -r requirements.txt
```

## Run the programme

```bash
python main.py
```

## Output

- SQLite database ('functions.db')
- training-to-ideal functions mapping
- test point assignments (matched/ unmatched)
- interactive Bokeh visualizations
- Styled HTML tables

## Technologies

- Python 3.14.0
- NumPy
- Pandas
- SQLAlchemy
- Bokeh
- PyTest

## Author
Dominique Thibault
