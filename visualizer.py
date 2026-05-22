"""
A module for plotting and visualizing the training data and their corresponding ideal function
as well as their assigned test data points.
"""
from bokeh.plotting import figure, output_file, save
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    PanTool,
    WheelZoomTool,
    BoxZoomTool,
    ResetTool,
    SaveTool
)
from bokeh.layouts import gridplot
import pandas as pd
import numpy as np

class Visualizer:
    """A class for visualizing input data and output results."""
    def plot_training_functions(self, train, test):
        """
        Plots the training functions in figure 1 and the training functions
        against the test data points in figure 2.
        """
        # Creates plot with title and axis labels
        p1 = figure(
            title='Training Functions',
            x_axis_label='X',
            y_axis_label='Y',
            toolbar_location='right',
            width=800,
            height=400,
            background_fill_color='#fafafa'
        )

        # Adds training functions as renderers.
        colors = ['red', 'blue', 'black', 'green']
        y_cols = train.columns[1:].tolist()

        for i, col in enumerate(y_cols):
            p1.line(
                train['x'],
                train[col],
                line_width=2,
                line_color=colors[i%len(colors)],
                line_alpha=0.5,
                legend_label=str(col)
            )

        # Customizes output and saves plot as HTML file.
        output_file('datasets/training_functions.html')
        save(p1)

        # Creates Bokeh figure for all training functions and test data points.
        p2 = figure(
            title='Training Functions vs. Test Data Points',
            x_axis_label='x',
            y_axis_label='y',
            width=800,
            height=600,
            toolbar_location='right'
        )

        # Creates a plot for all training functions.
        for col in train.columns[1:]:
            p2.line(
                train['x'],
                train[col],
                alpha=0.5,
                line_width=2,
                line_color='red',
                legend_label='Training Functions'
            )

            # Creates a plot for all test data points.
            p2.scatter(
                test['x'],
                test['y'],
                alpha=0.5,
                line_width=2,
                line_color='black',
                fill_color='blue',
                fill_alpha=0.2,
                legend_label='Test Data Points'
            )

        # Saves as HTML-file.
        output_file('datasets/training_functions_vs_test.html')
        save(p2)

    def plot_all_ideals_vs_test(self, ideal, test):
        """The function for plotting all 50 ideal functions against all test data points in one figure."""
        # Creates Bokeh figure for all ideal functions.
        p = figure(
            title='50 Ideal Functions vs. Test Data Points',
            x_axis_label='x',
            y_axis_label='y',
            toolbar_location='right',
            width=800,
            height=600
        )

        # Plots all 50 ideal functions.
        for col in ideal.columns[1:]:
            p.line(
                ideal['x'],
                ideal[col],
                alpha=0.5,
                line_width=2,
                legend_label='Ideal Functions',
            )

        # Plots all test data points.
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

        # Saves as HTML-file.
        output_file('datasets/50_ideal_vs_test.html')
        save(p)

    def plot_overlay_fit(self, train, ideal, best):
        """
        A function visualizes the training functions and their corresponding ideal functions
        using overlaid line plots for better visual comparison and assessment of the quality of matches.
        """

        # Creates empty list for saving the plots later on.
        plots = []

        for train_col, info in best.items():
            ideal_col = info['ideal_function']

        # Creates figure.
            p = figure(
                title= f'{train_col} vs {ideal_col}',
                width=800,
                height=400,
                toolbar_location='right',
                tools=[
                    PanTool(),
                    WheelZoomTool(),
                    BoxZoomTool(),
                    ResetTool(),
                    SaveTool()
                ]
            )

            source_train = ColumnDataSource(train)
            source_ideal = ColumnDataSource(ideal)

            # Creates plots for each training function.
            p.line(
                'x',
                train_col,
                source=source_train,
                legend_label=f'Train {train_col}',
                line_color='blue',
                line_width=2
            )

            # Creates plots for ideal functions.
            p.line(
                'x',
                ideal_col,
                source=source_ideal,
                legend_label=f'Ideal {ideal_col}',
                line_color='red',
                line_width=2,
                line_dash='dashed'
            )

            # Customizes legend.
            p.legend.location = 'top_right'

            # Appends plots to empty list.
            plots.append(p)

        # Adds linked axes.
        if len(plots) > 1:
            for fig in plots[1:]:
                fig.x_range = plots[0].x_range
                fig.y_range = plots[0].y_range

        # Arranges plots in 2x2 grid.
        grid = gridplot([plots[i:i+2] for i in range(0, len(plots), 2)])

        # Customizes output file to HTML.
        # Shows HTML.
        output_file('datasets/training_vs_ideal_overlay.html')
        save(grid)

    def plot_test_vs_ideal_functions(self, ideal_df, results_df, unmatched_df, best_fit):
        """
        This function plots test data points together with the 4 selected ideal functions.
        Showing the overall fit of each ideal function.
        """

        # Creates figure
        p = figure(
            title='Test Data Points vs. Ideal Functions',
            x_axis_label='X',
            y_axis_label='Y',
            width=800,
            height=400,
            tools=[ResetTool(), SaveTool(), BoxZoomTool(), WheelZoomTool(), PanTool()],
            toolbar_location='right'
        )

       # 1. IDEAL FUNCTION PLOTTING
        colors = ['red', 'lightgreen', 'blue', 'magenta']

        for i, (train_col, info) in enumerate(best_fit.items()):
            ideal_col = info['ideal_function']
            threshold = info['max_dev'] * np.sqrt(2)

            # --Adds tolerance band to each ideal curve for visualizing deviation--
            p.varea(
                x=ideal_df['x'],
                y1=ideal_df[ideal_col] - threshold,
                y2=ideal_df[ideal_col] + threshold,
                fill_alpha=0.6,
                color='gray',
                legend_label='Tolerance Band'
        )
            # --Plots the 4 ideal functions--
            p.line(
                ideal_df['x'],
                ideal_df[ideal_col],
                line_width=2,
                color=colors[i % len(colors)],
                legend_label=f'Ideal: {ideal_col} --> {train_col}'
            )

        # 2. TEST DATA POINT PLOTTING.
        # --Creates ColumnDataSource--
        source = ColumnDataSource(results_df)

        # --Plots matched test points in a scatter plot--
        scatter_renderer = p.scatter(
            x= 'x',
            y ='y_test',
            size=6,
            source=source,
            fill_color = 'orange',
            line_color='black',
            legend_label='Assigned Test data points',
        )

        # --Plots unmatched test points in a scatter plot--
        source_unmatched = ColumnDataSource(unmatched_df)
        scatter_renderer = p.scatter(
            x='x',
            y='y_test',
            size=6,
            source=source_unmatched,
            fill_color='lightblue',
            line_color='black',
            legend_label='Unmatched Test data points',
            fill_alpha=0.6
        )

        # --Adds hover tool with tooltips--
        #dev_cols = [col for col in results_df.columns if col.startswith('dev_')]

        p.add_tools(HoverTool(
            renderers=[scatter_renderer],
            tooltips=(
                    [('X', '@x{0.00 a}'),
                     ('Y', '@y_test{0.00 a}'),
                     ('Nearest ideal func', '@nearest_ideal'),
                     ('Smallest deviation', '@nearest_dev{0.00 a}'),]
                    #+ [(col, f'@{col}{{0.00 a}}') for col in dev_cols]
            )
        ))

        # --Configures legend--
        p.legend.location = 'top_right'
        p.legend.click_policy = 'hide'
        legend = p.legend[0]

        # --Reorders legend items--
        desired_order = [
            'Test data points',
            'Ideal: y13 --> y1',
            'Ideal: y24 --> y2',
            'Ideal: y36 --> y3',
            'Ideal: y40 --> y4',
            'Residuals',
            'Tolerance Band'
        ]

        legend.items = sorted(
            legend.items,
            # Computes a number for each legend item and sorts by that number.
            # Looks up where that text appears in custom list.
            # Retrieves the actual legend text.
            key=lambda item: desired_order.index(item.label['value'])
            if item.label['value'] in desired_order else 999
        )

        p.add_layout(p.legend[0], 'right')

        # --Customizes output file and saves it to HTML--
        # --Shows HTML--
        output_file('datasets/test_vs_ideal_functions.html')
        save(p)

    def plot_assignments(self, result_df):
        """
        Plots the assigned data points by ideal function.
        Showing which point belongs to which function.
        """
        # Creates figure.
        p = figure(
            title = 'Assigned Test Data Points',
            x_axis_label = 'X',
            y_axis_label = 'Y',
            width=800,
            height=400,
            toolbar_location='right',
            tools=[ResetTool(), SaveTool(), BoxZoomTool(), WheelZoomTool(), PanTool()]
        )

        # Colors test data points according to the assigned ideal function.
        result_df['ideal_function'] = result_df['ideal_function'].fillna('unmatched')
        # -- Retrieves list of all four ideal functions matched --
        ideal_functions = list(set(result_df['ideal_function'].unique()))
        # -- List of colors defined for the color mapping --
        colors = ['black', 'red', 'green', 'blue', 'orange']
        # Maps the colors from colors list to each item in ideal functions list.
        color_map={
            ideal:colors[i % len(colors)]
            for i, ideal in enumerate(ideal_functions)
        }

        # Creates scatter plot for each group separately.
        for ideal_func in ideal_functions:
            subset = result_df[result_df['ideal_function'] == ideal_func]

            p.scatter(
                subset['x'],
                subset['y_test'],
                size=6,
                legend_label=f'Ideal: {ideal_func}',
                color=color_map[ideal_func], # Takes color value from color mapping.
                fill_alpha=0.6
            )

        # Configures legend.
        p.legend[0].items.sort(key=lambda item: item.label['value'])
        p.legend.location='top_right'
        p.legend.click_policy='hide'

        # Saves output in HTML file.
        # Shows HTML.
        output_file('datasets/color_mapped_assignments.html')
        save(p)

    def make_pretty(self, training_mapping_df, test_assignment_df, results_df, unmatched_df):
        """This function formats and styles the output tables for a more aesthetic presentation."""
        # Uses pandas Styler class to format tables appropriately.
        # Deletes "id" column in both data frames.
        from html2image import Html2Image
        self.training_mapping_df = training_mapping_df

        # Clears data before formatting.
        #--Drops ID-column--
        training_mapping_df = training_mapping_df.drop(columns=['id'])
        test_assignment_df = test_assignment_df.drop(columns=['id']).sort_values(by=['deviation'], ascending=False)

        # --Resets index and drops uncessary 'deviation_dict' 'ideal_function', 'deviation' columns--
        unmatched_df = unmatched_df.reset_index(drop=True)
        unmatched_df = unmatched_df.drop(unmatched_df.columns[2:4], axis=1)
        unmatched_df = unmatched_df.drop(unmatched_df.columns[5:], axis=1)

        # 1. Training Mapping Table
        self.current_df = training_mapping_df

        training_styler = (
            training_mapping_df.style
            .set_caption('Training Functions mapped to Ideal Functions')
            .format(precision=4, thousands=",", decimal=".")
            .apply(self.highlight_alternate, axis=0)
            .map_index(self.hightlight_alternate_index, axis=0)
            .set_table_styles([
                {'selector': 'th, td',
                 'props': [('border', '1px solid #dddddd'),
                           ('padding', '8px')]},
                {'selector': 'table',
                 'props': [('border-collapse', 'collapse')]},
                {'selector': 'caption',
                 'props': [('font-weight', 'bold'),
                           ('font-size', '1.3em')]}
             ])
            .relabel_index(['Training', 'Ideal', 'Least-Square Error',
                            'Max Dev', 'Avg Dev'],axis='columns')
        )

        #  2. Test Assignment Table
        self.current_df = test_assignment_df

        test_styler = (
            test_assignment_df.style
            .set_caption('Test Data Points assigned to Ideal Functions')
            .format(precision=4, thousands=",", decimal=".")
            .apply(self.highlight_alternate, axis=0)
            .map_index(self.hightlight_alternate_index, axis=0)
            .set_table_styles([
                {'selector': 'th, td',
                 'props': [('border', '1px solid #dddddd'),
                           ('padding', '8px')]},
                {'selector': 'table',
                 'props': [('border-collapse', 'collapse')]},
                {'selector': 'caption',
                 'props': [('font-weight', 'bold'),
                           ('font-size', '1.3em')]}
            ])
            .relabel_index(['X', 'Y', 'Dev', 'Ideal'],axis='columns')
        )

        # 3. Results Table
        self.current_df = results_df

        results_styler = (
            results_df.style
            .set_caption('Test Data Points assigned to Ideal Functions')
            .format(precision=2, thousands=",", decimal=".")
            .apply(self.highlight_alternate, axis=0)
            .map_index(self.hightlight_alternate_index, axis=0)
            .set_table_styles([
                {'selector': 'th, td',
                 'props': [('border', '1px solid #dddddd'),
                           ('padding', '8px')]},
                {'selector': 'table',
                 'props': [('border-collapse', 'collapse')]},
                {'selector': 'caption',
                 'props': [('font-weight', 'bold'),
                           ('font-size', '1.3em')]}
            ])
        )

        # 4. Unmatched Table
        self.current_df = unmatched_df
        #print(unmatched_df.describe())

        unmatched_styler = (
            unmatched_df.style
            .set_caption('Unmatched Test Data Points vs. 50 Ideal Functions')
            .format(precision=2, thousands=",", decimal=".")
            .apply(self.highlight_alternate, axis=0)
            .map(self.highlight_dev_constraint, subset=['nearest_dev'])
            .map_index(self.hightlight_alternate_index, axis=0)
            .set_table_styles([
                {'selector': 'th, td',
                 'props': [('border', '1px solid #dddddd'),
                           ('padding', '8px')]},
                {'selector': 'table',
                 'props': [('border-collapse', 'collapse')]},
                {'selector': 'caption',
                 'props': [('font-weight', 'bold'),
                           ('font-size', '1.3em')]}
            ])
            .relabel_index(['X', 'Y', 'Nearest Ideal', 'Nearest Dev', 'Nearest Y-Ideal'],axis='columns')
        )

        # Saves and opens tables in an HTML file and PNG.
        hti = Html2Image()

        with open('training_mapping_styler.html', 'w', encoding='utf-8') as f:
            f.write(training_styler.to_html())

        with open('test_assignment_styler.html', 'w', encoding='utf-8') as f:
            f.write(test_styler.to_html())
        hti.screenshot(html_file='test_assignment_styler.html', save_as='datasets/test_assignment_styler.png')

        with open('results_styler.html', 'w', encoding='utf-8') as f:
            f.write(results_styler.to_html())

        with open('unmatched_styler.html', 'w', encoding='utf-8') as f:
            f.write(unmatched_styler.to_html())
        hti.screenshot(html_file='unmatched_styler.html', save_as='datasets/unmatched_styler.png')

    def highlight_alternate(self, s):
        """Highlights every other row in the data frame lightgray."""
        return ['background-color: #f2f2f2' if i % 2 != 0 else '' for i in range(len(s))]

    def hightlight_alternate_index(self, label):
        """Highlights every other row index column in the data frame lightgray."""
        idx_pos = self.current_df.index.get_loc(label)
        if idx_pos % 2 != 0:
            return 'background-color: #f2f2f2;'
        return ''

    def highlight_dev_constraint(self, val):
        """Highlights values below the deviation constraint."""
        # Defines thresholds.
        threshold = self.training_mapping_df['max_deviation'].max() * np.sqrt(2)
        threshold_5 = threshold * 1.05
        threshold_20 = threshold * 1.20
        threshold_25 = threshold * 1.25

        # Maps color to threshold level.
        if val <= threshold:
            color = 'lightblue'
        elif threshold <= val <= threshold_5:
            color = 'lightgreen'
        elif threshold_5 < val <= threshold_20:
            color ='orange'
        elif threshold_20 < val <= threshold_25:
            color = 'red'
        else:
            return ''
        return f'background-color:{color}'
