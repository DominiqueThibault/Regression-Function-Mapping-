"""Contains core classes for function representation and matching."""

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Model:
    """
    A core model class for finding the best matching ideal function to the training data.
    using the least-square error.
    """
    def __init__(self, train_df, ideal_df):
        """Initializes the model with training data and ideal functions as parameters."""
        self.train = train_df
        self.ideal = ideal_df
        self.best = {}
        self.logger = logger

    def least_square_error(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Computes sum of squared errors."""
        return np.sum((y_true - y_pred) ** 2)

    def fit(self):
        """Finds the best matching ideal function to each training function."""
        try:
            for train_col in self.train.columns[1:]:
                best_error = float('inf')
                best_ideal = None
                max_dev = 0
                dev = 0

                for ideal_col in self.ideal.columns[1:]:

                    # Aligns on x-values.
                    train_df = self.train[['x', train_col]].rename(columns={train_col: 'y_train'})
                    ideal_df = self.ideal[['x', ideal_col]].rename(columns={ideal_col: 'y_ideal'})

                    merged = pd.merge(
                        train_df,
                        ideal_df,
                        on='x',
                    )

                    merged = merged.dropna()
                    if merged.empty:
                        continue

                    y_train = merged['y_train']
                    y_ideal = merged['y_ideal']

                    error = self.least_square_error(y_train, y_ideal)

                    if error < best_error:
                        best_error = error
                        best_ideal = ideal_col
                        max_dev = np.max(np.abs(y_train - y_ideal))
                        avg_dev = np.mean(y_train - y_ideal)

                    self.logger.debug(f"{train_col} vs {ideal_col}: error={error}")

                # Stores the best match for each column.
                self.best[train_col] = {
                    'ideal_function': best_ideal,
                    'error': best_error,
                    'max_dev': max_dev,
                    'avg_dev': avg_dev
                }

            self.logger.info(f"Found best matches for {len(self.best)}.")

            # Converts dictionary into pandas DataFrame and exports it as CSV file.
            best_df = pd.DataFrame(self.best)
            best_df.to_csv('best.csv', index=False)

            return self.best

        except Exception as e:
            self.logger.error(f"Error in model fitting: {str(e)}.")
            raise


