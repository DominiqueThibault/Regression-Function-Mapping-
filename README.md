# Regression Function Mapping

## Description
The program maps four training regression functions to the best-fitting functions from a set of 50 ideal functions using the least-squares criterion. Subsequently, unseen test data points are assigned to the selected ideal functions if they satisfy the required deviation constraint \[
|y_{test}-y_{ideal}| \le \sqrt{2}\cdot\max|y_{training}-y_{ideal}|.

Results are stored in an SQLIte database and visualized via Bokeh.

## Features
- Least-Squares fitting
- Selection of the four best-fitting funcitons
- Test point assignment using √2 deviation constraint
- Residual analysis
- SQLite database integration (SQLALchemy ORM)
- Interactive visualization with Bokeh
- Styled HTML result tables

## Project Structure
```text
.
├── main.py                      # Process orchestration
├── model.py                     # Model fitting calculations using least-squares (matching training functions with ideal functions).
├── evaluator.py                 # Test point validation by deviation constraint.
├── visualizer.py                # Plotting outputs in visually appealing graphs.
├── database_orm.py              # Saving outputs to SQLite database.
├── data_loader.py               # Loading CSV datasets into program. 
├── requirements.txt              
├── datasets/
└── outputs/
```

## Installation

### 1. Clone the repository
```bash
git clone [https://github.com/DominiqueThibault/Regression-Function-Mapping-]
cd RegressionFunctionMapping
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

## Run the program

```bash
python main.py
```

## Output

- SQLite database ('functions.db')
- training-to-ideal functions mapping
- test point assignments (matched/ unmatched)
- interactive Bokeh visualizations
- Styled HTML tables

### Examples <br>

50 ideal functions plotted against all test data points: <br>
<img width="1200" height="900" alt="50_ideals_vs_test" src="https://github.com/user-attachments/assets/b2c79988-00aa-47dd-8e75-cc55c914a49e" /> <br><br>

Plotting 4 training functions against their matched best-fitting ideal function: <br>
<img width="2400" height="1245" alt="Overlay_training_ideal" src="https://github.com/user-attachments/assets/2a9a01b6-d014-41fd-bf7b-40dcdd129e26" />

## Technologies

- Python 3.14.0

### Libraries:
- NumPy
- Pandas
- SQLAlchemy
- Bokeh
- PyTest

## Author
Dominique Thibault <br>
IU International University of Applied Sciences <br>
Course: Programming with Python

