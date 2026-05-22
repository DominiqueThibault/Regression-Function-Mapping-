"""Orchestration of the entire process."""

import pandas as pd

from data_loader import DataLoader
from model import Model
from evaluator import Evaluator
from database_orm import DatabaseORM
from regression_params import RegressionParams
from visualizer import Visualizer
import logging


def main():
    """This function runs the main program."""

    # Sets logging levels.
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(message)s'
    )

    # 1. Loads data.
    loader = DataLoader(
        'datasets/train.csv',
        'datasets/test.csv',
        'datasets/ideal.csv'
    )
    train_df, ideal_df, test_df = loader.load_data()

    # 2. Trains model (finds the best ideal function).
    model = Model(train_df, ideal_df)
    best_fit = model.fit()

    # 3. Evaluates test data, converts them to pandas DataFrame and saves them in a csv format.
    evaluator = Evaluator(ideal_df, best_fit)
    output = evaluator.assign(test_df)
    res = output['results']
    unmatched = output['unmatched']
    results_df = pd.DataFrame(output['results'])
    unmatched_df = pd.DataFrame(unmatched)
    results_df.to_csv('results.csv', index=False)
    unmatched_df.to_csv('unmatched.csv', index=False)

    # 4. Saves to database.
    db = DatabaseORM()
    db.load_csv_to_db(train_df, test_df, ideal_df)
    db.save_training_mapping(best_fit)
    db.save_test_assignments(res)

    # Gets the DataFrames from the database for visualization.
    conn = db.engine.connect()
    training_mapping_df = pd.read_sql('SELECT * FROM training_mapping', conn)
    test_assignment_df = pd.read_sql('SELECT * FROM test_assignment', conn)
    conn.close()

    db.close()

    # 5. Plotting and visualizing.
    viz = Visualizer()
    viz.plot_training_functions(train_df, test_df)
    viz.plot_overlay_fit(train_df, ideal_df, best_fit)
    viz.plot_all_ideals_vs_test(ideal_df,test_df)
    viz.plot_test_vs_ideal_functions(ideal_df, results_df, unmatched_df, best_fit)
    viz.plot_assignments(results_df)
    viz.make_pretty(training_mapping_df, test_assignment_df, results_df, unmatched_df)

    # 6. Additional function: Parameter calculation
    calculator = RegressionParams(train_df, ideal_df)
    all_params = calculator.get_regression_params()
    train_params = all_params['train']
    ideal_params = all_params['ideal']

    train_params_df = pd.DataFrame(train_params)
    ideal_params_df = pd.DataFrame(ideal_params)

    train_params_df.to_excel('train_params.xlsx', index=False)
    ideal_params_df.to_excel('ideal_params.xlsx', index=False)

if __name__ == '__main__':
    main()