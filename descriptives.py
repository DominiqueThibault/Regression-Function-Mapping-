"""
This modules serves exclusively for data set exploration before further data processing.
It is not part of the project's operating architecture.
"""

import pandas as pd

import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save, show

# Load CSV-files
train = pd.read_csv('raw_datasets/train.csv', encoding='utf-8')
test = pd.read_csv('raw_datasets/test.csv',encoding='utf-8')
ideal = pd.read_csv('raw_datasets/ideal.csv', encoding='utf-8')
#unmatched = pd.read_csv('unmatched.csv', encoding='utf-8')
#test_assignment = pd.read_csv('datasets/test_assignment.csv', encoding='utf-8')

# Pass name and pd dataframe to a dictionary.
datasets = {
    'train': train,
    'test': test,
    'ideal': ideal,
    #'unmatched': unmatched
}
# Create empty dictionary for saved Excel-files later on.
saved_filenames = []

# Iterate over dataset dictionary to retrieve stats, nan and view pd.
# Raise exception, if files are not found.
for name, df in datasets.items():
    try:
        print(f"Dataset loaded: {name}")
        print(df.head())
        print(df.tail())

        print("number of rows and columns:")
        print(df.shape)

        print("Summary of descriptive stats:")
        print(df.describe())

        print("Missing values (NaN) by column:")
        print(df.isnull().sum())

        output_path = f"raw_datasets/{name}.xlsx"
        df.to_excel(
            output_path,
            sheet_name='data set',
            index=False
        )
        try:
            y_cols = df.columns[1:]

            min_col = df[y_cols].min().idxmin()
            max_col = df[y_cols].max().idxmax()

            min_value = df[y_cols].min().min()
            max_value = df[y_cols].max().max()

            print(f"Minimum value {min_value} found in column {min_col}")
            print(f"Maximum value {max_value} found in column {max_col}")
        except Exception as e:
            print(f"error in processing files {df}: {e}")
            raise
    except FileNotFoundError:
        print(f"File {name} not found in directory.")
    else:
        saved_filenames.append(output_path)
        print(f"{len(saved_filenames)} files saved successfully.")


# Create matplotlib line plot for all ideal values.
# Save and open as PNG-file.
for col in ideal.columns[1:]:
    plt.plot(ideal['x'], ideal[col], alpha=0.5)

plt.xlabel('x')
plt.ylabel('y')
plt.title('50 Ideal Functions vs. Test Data Points')
plt.show()

# Create Bokeh figure for all ideal functions and test data points.
p = figure(
    title='Ideal Functions',
    x_axis_label='x',
    y_axis_label='y',
    toolbar_location='right',
    width=800,
    height=600
)

# Plot all 50 ideal functions.
for col in ideal.columns[1:]:
    p.line(
        ideal['x'],
        ideal[col],
        alpha=0.5,
        line_width=2,
        legend_label='Ideal Functions',
    )

# Plot all test data points.
p.scatter(
    test['x'],
    test['y'],
    alpha=0.5,
    line_width=2,
    line_color='black',
    fill_color='blue',
    fill_alpha=0.2,
    legend_label='Test Data Points'
)

# Save and open as HTML-file.
output_file('raw_datasets/50_ideal_vs_test.html')
save(p)
show(p)

# Create Bokeh figure for all training functions and test data points.
p = figure(
    title='Training Functions vs. Test Data Points',
    x_axis_label='x',
    y_axis_label='y',
    width=800,
    height=600,
    toolbar_location='right'
)

# Create a plot for all training functions.
for col in train.columns[1:]:
    p.line(
        train['x'],
        train[col],
        alpha=0.5,
        line_width=2,
        line_color='red',
        legend_label='Training Functions'
    )

# Create a plot for all test data points.
    p.scatter(
        test['x'],
        test['y'],
        alpha=0.5,
        line_width=2,
        line_color='black',
        fill_color='blue',
        fill_alpha=0.2,
        legend_label='Test Data Points'
    )

# Save and open as HTML-file.
output_file('raw_datasets/training_functions_vs_test.html')
save(p)
show(p)