"""Directory containing unit tests for each module."""

import pandas as pd

from model import Model
from evaluator import Evaluator

#-------------------------------------------
# MODEL TESTS
#-------------------------------------------

def test_least_square_error():
    """Tests least-square error function."""
    model = Model(None, None)
    y_true = pd.Series([1, 2, 3])
    y_pred = pd.Series([1, 2, 4])

    assert model.least_square_error(y_true, y_pred) == 1, 'The least square error should be 1.'

def test_fit_basic_mapping():
    """Tests, if fit function matches the correct ideal function."""
    # Creates training data (y1 matches ideal y1 perfectly)
    train_df = pd.DataFrame({
        'x':[1, 2, 3],
        'y':[1, 2, 3]
    })

    # Creates ideal function.
    ideal_df = pd.DataFrame({
        'x':[1, 2, 3],
        'y1':[1, 2, 3],
        'y2':[2, 3, 4]
    })

    model = Model(train_df, ideal_df)
    result = model.fit()

    assert result['y']['ideal_function'] == 'y1', 'Should match with y1'
    assert result['y']['error'] == 0, 'Error should be 0 with perfect match'

#--------------------------------------------
# EVALUATOR TESTS
#-------------------------------------------

def test_assign_returns_result():
    """Tests assignment function."""
    #Creates ideal function x-y pair.
    ideal_df = pd.DataFrame({
        "x": [1],
        "y1": [2]
    })

    # Pretends model results.
    best_fit = {
        'train1': {
            'ideal_function': 'y1',
            'max_dev': 1
        }
    }

    evaluator = Evaluator(ideal_df, best_fit)
    test_df = pd.DataFrame({'x': [1], 'y': [2]})
    result = evaluator.assign(test_df)

    assert len(result['results']) == 1, 'The assignment should return exactly one result.'
    assert result['results'][0]['ideal_function'] == 'y1', 'Should match with y1'

def test_find_best_match():
    """Tests assignment based on deviation + √2 criterion."""
    ideal_df = pd.DataFrame({
        'x': [1, 2, 3],
        'y1': [1, 2, 3],
        'y2': [10, 10, 10],
    })

    # Pretend model results.
    best = {
        'y_train': {
            'ideal_function': 'y1',
            'max_dev': 0.1
        }
    }

    evaluator = Evaluator(ideal_df, best)
    result = evaluator._find_best_match(1.0, 1.05)# Test point close to y1.
    result2 = evaluator._find_best_match(1.0, 1.5)# Too far away (should not match).

    assert result is not None, 'Should find match'
    assert result['ideal_function'] == 'y1', 'Should match with y1'
    assert result2 is None, 'Point is too far away for a match'

