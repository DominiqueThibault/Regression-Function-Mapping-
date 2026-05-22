"""This module coordinates the calculations of regression parameters."""
import numpy as np
import pandas as pd

class RegressionParams():
    """A class representing a regression parameters calculator."""
    def __init__(self, train_df, ideal_df):
        """Initialize the calculator class."""
        self.train_df = train_df
        self.ideal_df = ideal_df


    def get_regression_params(self):
        """Calculates the regression parameters."""
        datasets = {
            'train': self.train_df,
            'ideal': self.ideal_df
        }

        # Creates dictionary collecting the results.
        results = {}

        for name, df in datasets.items():
            # Filters columns.
            y_columns = [col for col in df.columns if col != 'x']

            #Vectorizes calculations for all columns simultaneously.
            fit_results = np.polyfit(df['x'], df[y_columns], 1)
            slopes = fit_results[0]
            intercepts = fit_results[1]

            # Stores results in a pd DataFrame.
            params_df = pd.DataFrame({
                "Function": y_columns,
                "Slope":slopes,
                "Intercept": intercepts
            })

            results[name] = params_df

        return results

