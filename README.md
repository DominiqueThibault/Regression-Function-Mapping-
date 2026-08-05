[50_ideal_vs_test.html](https://github.com/user-attachments/files/30743921/50_ideal_vs_test.html)# Regression Function Mapping

## Description
This project was developed as part of the IU Written Assignment for the Programming with Python course.

The program maps four training regression functions to the best-fitting functions from a set of 50 ideal functions using the least-squares criterion. Subsequently, unseen test data points are assigned to the selected ideal functions if they satisfy the required deviation constraint

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

## Example output

<img width="1200" height="900" alt="50_ideals_vs_test" src="https://github.com/user-attachments/assets/b2c79988-00aa-47dd-8e75-cc55c914a49e" />

<img width="2400" height="1245" alt="Overlay_training_ideal" src="https://github.com/user-attachments/assets/2a9a01b6-d014-41fd-bf7b-40dcdd129e26" />

## Technologies

- Python 3.14.0
- NumPy
- Pandas
- SQLAlchemy
- Bokeh
- PyTest

## Author
Dominique Thibault
