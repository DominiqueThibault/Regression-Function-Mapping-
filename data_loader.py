"""
This module handles loading datasets from csv files and preparing them for processing.
"""

import pandas as pd

class DataLoader:
    """Class for loading and preparing function data from files."""
    def __init__(self, train_path, test_path, ideal_path):
        """Initialize the data loader."""
        self.train_path = train_path
        self.test_path = test_path
        self.ideal_path = ideal_path

    def load_data(self):
        """
        Load the data from csv files.

        Returns:
            DataFrame containing training, test and ideal
            function data.

        Raises:
            FileNotFoundError, if file does not exist.
            ValueError, if file does not contain data.
        """
        try:
            train = pd.read_csv(self.train_path, index_col=None)
            test = pd.read_csv(self.test_path, index_col=None)
            ideal = pd.read_csv(self.ideal_path, index_col=None)
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist.")
        except ValueError:
            raise ValueError("File does not contain data.")
        else:
            return train, ideal, test

