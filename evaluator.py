"""Implementation of evaluation metrics and validation logic."""

import numpy as np
import logging

# Set up logger
logger = logging.getLogger(__name__)

class Evaluator:
    """
    A class for assigning test data points to the best matching ideal functions
    based on previously determined mappings and on the application of deviation constraints.
    """

    def __init__(self, ideal_df, best):
        """Initializes evaluator class with ideal functions data frame and best matches dictionary."""
        self.ideal_df = ideal_df
        self.best = best
        self.logger = logger

        if not best:
            raise ValueError("best dictionary cannot be empty")

        # Validates structure.
        for train_col, info in best.items():
            if 'ideal_function' not in info:
                raise ValueError(f"Missing 'ideal_function' key in {train_col}.")
            if info["ideal_function"] not in self.ideal_df.columns:
                raise ValueError(f"{info['ideal_function']} not found in ideal_df.")

    def assign(self, test_df):
        """
        Processes entire test data set and assigns each test data point to its best matching
        ideal function based on previous mappings.
        Returns:
            List of dictionaries with assigned values and their deviation.
        """
        results = []
        unmatched = []

        for _, row in test_df.iterrows():
            try:
                x = row['x']
                y = row['y']

                # Skips NaN values.
                if np.isnan(row['y']):
                    continue

                # Finds best matching ideals and stores result.
                assignments = self._find_best_match(row['x'], row['y'])
                if assignments:
                    results.append(assignments)
                else:
                    unmatched.append(self.collect_unmatched(x,y))
            except Exception as e:
                self.logger.error(f"Error processing row: {e}")

        self.logger.info(
            f"Assignment complete: {len(results)} matched, {len(unmatched)} unmatched."
        )

        return {
            'results': results,
            'unmatched': unmatched
        }

    def _find_best_match(self, x, y):
        """
        Finds the best matching ideal function for a single test data point by
        applying deviation criterion.

        Returns:
             Dictionary with assigned functions and their deviation.
        """

        best_fit = None
        smallest_dev = float('inf')
        deviation_dict = {}

        for train_col, info in self.best.items():
            ideal_col = info['ideal_function']

            # Compares matching x values (for ideal and test data) and gets matching ideal y-value.
            y_ideal_vals = self.ideal_df.loc[
                np.isclose(self.ideal_df['x'], x), ideal_col
            ].values
            # -- Continues, if no matches found.
            if len(y_ideal_vals) == 0:
                continue

            y_ideal = y_ideal_vals[0]
            # -- Excludes NaN values.
            if np.isnan(y_ideal):
                continue

            # Computes y-deviation (test vs ideal).
            dev = abs(y - y_ideal)

            # Applies √2 criterion and picks the smallest deviation.
            if dev <= info['max_dev'] * np.sqrt(2):
                if dev < smallest_dev:
                    smallest_dev = dev
                    best_fit = ideal_col
                    best_y_ideal = y_ideal

        if best_fit is None:
            return None

        if best_fit:
            return {
                'x': x,
                'y_test': y,
                'ideal_function': best_fit,
                'y_ideal': best_y_ideal,
                'deviation': smallest_dev,
            }

        self.logger.debug(f"x={x}, y={y}, best={best_fit}, dev={smallest_dev}")

    def collect_unmatched(self, x,y):
        """
        This function collects all unmatched test data points and finds their nearest ideal function
        out of the pool of 50 ideal functions.
        Returns:
            Dictionary containing the ideal function closest to the test data point,
            including the deviation and y-value.
        """
        deviation_dict = {}

        for ideal_col in self.ideal_df.columns[1:]:
            y_ideal_vals = self.ideal_df.loc[
                np.isclose(self.ideal_df['x'], x), ideal_col
            ].values

            if len(y_ideal_vals) == 0:
                continue

            y_ideal = y_ideal_vals[0]

            deviation_dict[f"dev_{ideal_col}"] = abs(y - y_ideal)

        # Finds closest ideal function.
        nearest_ideal = min(deviation_dict, key=deviation_dict.get)
        nearest_func = nearest_ideal.replace('dev_', '')

        nearest_y_ideal = self.ideal_df.loc[
            np.isclose(self.ideal_df['x'], x), nearest_func
        ].values[0]

        return {
            'x': x,
            'y_test': y,
            'ideal_function': None,
            'deviation': None,
            'nearest_ideal': nearest_func, # Stores name of the nearest ideal function.
            'nearest_dev': deviation_dict[nearest_ideal], # Stores value of deviation to that function.
            'nearest_y_ideal': nearest_y_ideal, # Stores y-value of that function.
            **deviation_dict
        }

