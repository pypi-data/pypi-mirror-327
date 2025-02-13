import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import numpy as np
import datetime
import matplotlib.dates as mdates

class Page:
    def __init__(self, response):
        
        self.response = response
        self.grid_data = self.transform_input_to_structure_v4(response)

    
    def plot_from_figure_dict(self, figure_dict, ax, dpi: int = 150):
        
        def get_valid_color(color, default="steelblue"):
            if not color or not mcolors.is_color_like(color):
                return default
            return color

        def format_number(value):
            if value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
            return str(int(value))

    
        category = figure_dict.get("category", "")
        data = figure_dict.get("data", [])
        chart_type = category or (data[0].get("type") if data else "")

        title = figure_dict.get("title", "")
        x_label = figure_dict.get("xAxisLabel", "")
        y_label = figure_dict.get("yAxisLabel", "")

        if not data:
            print("No data available for plotting.")
            return

        # Determine subplot dimensions for dynamic sizing
        bbox = ax.get_position()
        subplot_width = bbox.width * ax.figure.get_size_inches()[0]
        subplot_height = bbox.height * ax.figure.get_size_inches()[1]
        dynamic_title_fontsize = max(8, min(16, int(subplot_height * 2)))
        dynamic_label_fontsize = max(8, min(12, int(subplot_width * 1.5)))

        # Adjust title if it is long
        words = title.split()
        if len(words) > 3:
            mid = len(words) // 2
            title = "\n".join([" ".join(words[:mid]), " ".join(words[mid:])])

        ax.set_title(title, fontsize=dynamic_title_fontsize, fontweight="bold", color="#333", pad=0)
        ax.set_xlabel(x_label, fontsize=dynamic_label_fontsize, fontweight="bold", color="#333", labelpad=subplot_height * 0.1)
        ax.set_ylabel(y_label, fontsize=dynamic_label_fontsize, fontweight="bold", color="#333", labelpad=subplot_height * 0.1)

        x_labels = []
        # ------------------------ CARTESIAN CHARTS ------------------------ #
        if category == "cartesian":
            # -------------------- BAR / COLUMN / STACKED BAR CHART HANDLING -------------------- #
            if any(d.get("type") in ["bar", "column", "stackedBar"] for d in data):
                # Ensure x_labels are strings so we can test for date patterns
                x_labels = [str(lbl) for lbl in data[0].get("xData", [])]
                x_indices = np.arange(len(x_labels))  # positions for the bars

                # Calculate dynamic dimensions for the subplot (in inches)
                bbox = ax.get_position()
                subplot_width = bbox.width * ax.figure.get_size_inches()[0]
                subplot_height = bbox.height * ax.figure.get_size_inches()[1]
                max_labels = 15
                label_step = max(1, len(x_labels) // max_labels)

                # Detect if labels appear to be time-based (e.g. "2025-02-06")
                is_time_data = all("-" in lbl for lbl in x_labels)

                # Determine chart type for grouping logic
                is_stacked = all(d.get("type") == "stackedBar" for d in data)
                is_grouped = all(d.get("type") == "column" for d in data) and len(data) > 1
                is_normal_bar = all(d.get("type") == "bar" for d in data) and len(data) == 1

                if is_stacked:
                    bottom_values = np.zeros(len(x_labels))
                    for dataset in data:
                        y_data = np.array(dataset.get("yData", []))
                        color = get_valid_color(dataset.get("color", "blue"))
                        label = dataset.get("name", "")
                        bars = ax.bar(x_indices, y_data, width=0.6, bottom=bottom_values,
                                      color=color, label=label)
                        for i, (bar, value) in enumerate(zip(bars, y_data)):
                            total_height = bottom_values[i] + value
                            ax.text(bar.get_x() + bar.get_width() / 2, total_height,
                                    format_number(value), ha="center", va="bottom", fontsize=8)
                        bottom_values += y_data

                elif is_grouped:
                    num_series = len(data)
                    bar_width = 0.35
                    offsets = np.linspace(-bar_width / 2, bar_width / 2, num_series)
                    for idx, dataset in enumerate(data):
                        y_data = np.array(dataset.get("yData", []))
                        color = get_valid_color(dataset.get("color", "blue"))
                        label = dataset.get("name", "")
                        bars = ax.bar(x_indices + offsets[idx], y_data, width=bar_width,
                                      color=color, label=label)
                        for bar, value in zip(bars, y_data):
                            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                                    format_number(value), ha="center", va="bottom", fontsize=8)

                else:
                    dataset = data[0]
                    y_data = np.array(dataset.get("yData", []))
                    color = get_valid_color(dataset.get("color", "blue"))
                    label = dataset.get("name", "")
                    bars = ax.bar(x_indices, y_data, width=0.6, color=color, label=label)
                    for bar, value in zip(bars, y_data):
                        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                                format_number(value), ha="center", va="bottom", fontsize=8)

                # -------------------- DYNAMIC X LABEL PLACEMENT -------------------- #
                ax.set_xticks(x_indices)  # set the tick positions

                if is_time_data:
                    # For time-based data, use the built-in tick labels
                    dynamic_label_fontsize = max(8, min(12, int(subplot_width * 1.5)))
                    visible_labels = [label if i % label_step == 0 else ""
                                      for i, label in enumerate(x_labels)]
                    ax.set_xticklabels(visible_labels, ha="center", fontsize=dynamic_label_fontsize)
                    # Rotate slightly for readability and add some bottom padding
                    ax.tick_params(axis='x', rotation=45, pad=10)
                else:
                    # For non-time-based data, manually add text labels (and hide the default ticks)
                    dynamic_fontsize = max(6, min(8, int(subplot_width * 1.5)))
                    for i, label in enumerate(x_labels):
                        if len(x_labels) > 15:
                            if i % label_step == 0:
                                ax.text(x_indices[i], -subplot_height * 0.1, label,
                                        ha="center", va="top", fontsize=dynamic_fontsize, fontweight="bold")
                        else:
                            ax.text(x_indices[i], -subplot_height * 0.1, label,
                                    ha="center", va="top", fontsize=8, fontweight="bold")
                    ax.set_xticklabels([])  # Hide the default tick labels

                ax.set_xlabel(figure_dict.get("xAxisLabel", "Category"), labelpad=subplot_height * 5)
                plt.tight_layout()

                if len(data) > 1:
                    ax.legend(loc="upper right", fontsize=8, frameon=True,
                              bbox_to_anchor=(0.95, 0.95), bbox_transform=ax.transAxes)

            # -------------------- CANDLESTICK CHART HANDLING -------------------- #
            if any(d.get("type") == "candle" for d in data):
                import datetime
                import matplotlib.dates as mdates

                dataset = next((d for d in data if d.get("type") == "candle"), None)
                if dataset:
                    x_data = dataset.get("xData", [])
                    low = dataset.get("low", [])
                    high = dataset.get("high", [])
                    open_ = dataset.get("open", [])
                    close = dataset.get("close", [])

                    min_length = min(len(x_data), len(low), len(high), len(open_), len(close))
                    if min_length == 0:
                        print("Error: No valid candlestick data available.")
                        return

                    # Convert timestamp from nanoseconds to datetime
                    x_data = [datetime.datetime.utcfromtimestamp(ts / 1e9) for ts in x_data[:min_length]]
                    low = low[:min_length]
                    high = high[:min_length]
                    open_ = open_[:min_length]
                    close = close[:min_length]

                    # Plot Candlesticks with Labels
                    for i in range(min_length):
                        color = "green" if close[i] > open_[i] else "red"
                        ax.plot([x_data[i], x_data[i]], [low[i], high[i]], color=color, linewidth=1, label="_nolegend_")
                        ax.plot([x_data[i], x_data[i]], [open_[i], close[i]], color=color, linewidth=4,
                                label="Up" if color == "green" else "Down")

                        # Add High & Low Value Labels
                        ax.text(x_data[i], high[i], f"{high[i]:.2f}", ha="center", va="bottom", fontsize=8, color=color)
                        ax.text(x_data[i], low[i], f"{low[i]:.2f}", ha="center", va="top", fontsize=8, color=color)

                    # Format x-axis
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    ax.xaxis.set_major_locator(mdates.DayLocator())

                    # Remove duplicate legend labels
                    handles, labels = ax.get_legend_handles_labels()
                    unique_legend = {lbl: hdl for hdl, lbl in zip(handles, labels) if lbl != "_nolegend_"}
                    ax.legend(unique_legend.values(), unique_legend.keys(), loc="upper left", fontsize=8, frameon=True)

                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)

            # -------------------- LINE CHART HANDLING -------------------- #
            elif any(d.get("type") == "line" for d in data):
                x_labels = [str(lbl) for lbl in data[0].get("xData", [])]  # Convert to strings
                x_indices = np.arange(len(x_labels))  # Numeric indices for plotting

                for dataset in data:
                    y_data = np.array(dataset.get("yData", []))
                    color = get_valid_color(dataset.get("color", "blue"))
                    line_label = dataset.get("name", "")
                    ax.plot(x_indices, y_data, marker='o', color=color, label=line_label)

                    # Annotate points with values
                    for xi, yi in zip(x_indices, y_data):
                        ax.text(xi, yi, format_number(yi), ha="center", va="bottom", fontsize=8)

                # **Ensure x-axis ticks are not hidden**
                ax.set_xticks(x_indices)  # Ensure ticks are set
                ax.set_xticklabels(x_labels, ha="right", rotation=45, fontsize=8)  # Display labels

                # **Ensure ticks are visible**
                ax.tick_params(axis='x', length=5, labelbottom=True)  # Do not hide x-ticks
                ax.tick_params(axis='y', length=5, labelleft=True)  # Ensure y-ticks are also visible

                # Adjust limits to prevent cropping
                ax.set_xlim(-0.5, len(x_labels) - 0.5)

                ax.set_xlabel(figure_dict.get("xAxisLabel", "Category"), fontsize=10, labelpad=10)
                ax.set_ylabel(figure_dict.get("yAxisLabel", "Value"), fontsize=10, labelpad=10)

                if len(data) > 1:
                    ax.legend(loc="upper right", fontsize=8, frameon=True)

                plt.draw()

            # -------------------- SCATTER CHART HANDLING -------------------- #
            elif any(d.get("type") == "scatter" for d in data):
                x_labels = [str(lbl) for lbl in data[0].get("xData", [])]  # Convert xData to strings
                x_indices = np.arange(len(x_labels))  # Numeric indices for plotting

                for dataset in data:
                    y_data = np.array(dataset.get("yData", []))
                    color = get_valid_color(dataset.get("color", "blue"))
                    scatter_label = dataset.get("name", "")

                    # Scatter plot with x_indices (numeric) and y_data
                    ax.scatter(x_indices, y_data, color=color, label=scatter_label, alpha=0.7, edgecolors="k")

                    # Annotate points with values
                    for xi, yi in zip(x_indices, y_data):
                        ax.text(xi, yi, format_number(yi), ha="center", va="bottom", fontsize=8)

                # **Ensure x-axis ticks are not hidden**
                ax.set_xticks(x_indices)  # Ensure ticks are set
                ax.set_xticklabels(x_labels, ha="right", rotation=45, fontsize=8)  # Display labels

                # **Ensure ticks are visible**
                ax.tick_params(axis='x', length=5, labelbottom=True)  # Do not hide x-ticks
                ax.tick_params(axis='y', length=5, labelleft=True)  # Ensure y-ticks are also visible

                # Adjust limits to prevent cropping
                ax.set_xlim(-0.5, len(x_labels) - 0.5)

                ax.set_xlabel(figure_dict.get("xAxisLabel", "Category"), fontsize=10, labelpad=10)
                ax.set_ylabel(figure_dict.get("yAxisLabel", "Value"), fontsize=10, labelpad=10)

                if len(data) > 1:
                    ax.legend(loc="upper right", fontsize=8, frameon=True)

                plt.draw()

        # ------------------------ PIE CHART HANDLING ------------------------ #
        elif chart_type in ["circular", "pie"]:
            dataset = data[0]
            pie_data = dataset.get("data", [])

            if not pie_data:
                print("No pie chart data found.")
                return

            sizes = [item["wedgeSize"] for item in pie_data]
            labels = [item["label"] for item in pie_data]

            if not any(sizes):
                print("No valid pie chart data to display.")
                return

            def autopct_format(pct, allvals):
                total = sum(allvals)
                absolute = int(round(pct * total / 100.0))
                return f'{absolute} ({pct:.1f}%)' if pct >= 2 else ''  # Hide small values

            # Get subplot size for dynamic label font adjustments
            bbox = ax.get_position()
            subplot_width = bbox.width * ax.figure.get_size_inches()[0]
            subplot_height = bbox.height * ax.figure.get_size_inches()[1]

            # Dynamic font sizing based on pie chart size
            base_fontsize = min(subplot_width * 8, subplot_height * 8)
            dynamic_label_fontsize = max(6, min(14, int(base_fontsize)))

            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=None,  # Hide default labels
                autopct=lambda pct: autopct_format(pct, sizes),
                startangle=270,
                wedgeprops={'edgecolor': 'white'},
                pctdistance=0.5,  # Position percentage inside the pie
                labeldistance=1.1  # Move labels slightly outward
            )

            # Adjust the font size of autopct texts dynamically
            for text in autotexts:
                text.set_fontsize(dynamic_label_fontsize)

            # Calculate total size to find slice percentages
            total_size = sum(sizes)
            percentages = [(size / total_size) * 100 for size in sizes]

            # Place labels inside slices dynamically based on size
            for i, (size, wedge) in enumerate(zip(sizes, wedges)):
                angle = (wedge.theta2 + wedge.theta1) / 2
                x = 0.4 * np.cos(np.radians(angle))  # Position inside the pie
                y = 0.4 * np.sin(np.radians(angle))

                # Adjust position for small slices
                if percentages[i] < 2:
                    x = 1.2 * np.cos(np.radians(angle))  # Move label outside for small slices
                    y = 1.2 * np.sin(np.radians(angle))
                    ha, va = ('center', 'center')
                else:
                    ha, va = ('center', 'center')

                ax.text(
                    x, y, labels[i] if percentages[i] >= 2 else '',
                    ha=ha, va=va, fontsize=dynamic_label_fontsize,
                    fontweight='bold', color="white" if percentages[i] > 5 else "black"
                )

            ax.set_xlabel("")
            ax.set_ylabel("")

            # Adjust legend placement dynamically based on available space
            if subplot_height < 2 or subplot_width < 2:
                ax.legend(labels, loc="center left", fontsize=8, frameon=True,
                          bbox_to_anchor=(1.2, 0.5), bbox_transform=ax.transAxes)
            else:
                ax.legend(labels, loc="best", fontsize=8, frameon=True)

        elif chart_type == "html":
            html_text = data[0].get("htmlText", "").strip()

            if not html_text:
                print("No HTML text to display.")
                return

            # Display the HTML text in the middle of the figure
            ax.text(0.5, 0.5, html_text, fontsize=12, ha='center', va='center', wrap=True)

            # Remove axes for a clean text display
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)

        # ----- RADIAL BAR CHART HANDLING ----- #
        elif chart_type == "radial_bar":
            if not data:
                print("No data available for radial bar chart.")
                return

            dataset = data[0]
            bars_data = dataset.get("data", [])

            if not bars_data:
                print("No valid radial bar chart data found.")
                return

            labels = [item["label"] for item in bars_data]
            values = [item["wedgeSize"] for item in bars_data]

            num_bars = len(values)
            angles = np.linspace(0, 2 * np.pi, num_bars, endpoint=False)

            max_value = max(values) if max(values) > 0 else 1  # Avoid division by zero
            normalized_values = [val / max_value for val in values]

            # Dynamically adjust font size based on subplot size
            bbox = ax.get_position()
            subplot_width = bbox.width * ax.figure.get_size_inches()[0]
            subplot_height = bbox.height * ax.figure.get_size_inches()[1]
            base_fontsize = min(subplot_width * 8, subplot_height * 8)
            dynamic_label_fontsize = max(6, min(14, int(base_fontsize)))

            # Plot bars
            bars = ax.bar(angles, normalized_values, width=2 * np.pi / num_bars,
                          color=['red', 'blue', 'green', 'yellow', 'purple'], alpha=0.7)

            # Set labels at corresponding angles with adjusted font size
            ax.set_xticks(angles)
            ax.set_xticklabels(labels, fontsize=dynamic_label_fontsize, fontweight='bold')

            # Remove radial ticks and grid
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.grid(False)

            # Set title dynamically
            ax.set_title(title, fontsize=dynamic_title_fontsize, fontweight="bold", pad=15)

            plt.tight_layout()

        else:
            print("Chart type not recognized:", chart_type)

        if x_labels and chart_type in ["bar", "column"]:
            ax.set_xlim(-0.5, len(x_labels) - 0.5)
            if any(dataset.get("yData") for dataset in data):
                ax.set_ylim(0, max(max(dataset.get("yData", [])) for dataset in data) * 1.1)

        if chart_type in ["bar", "column"]:
            ax.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        


        

    # ----------------------------------------------
    # Transformation Functions
    # ----------------------------------------------
    def read_row_data(self, row_dict, idx, id):
        temp_dict = {}
        temp_dict['id'] = str(id) + "_row" + str(idx)
        temp_dict['parent_index'] = idx

        if row_dict['type'] == 'chart':
            temp_dict['type'] = 'chart'
            if ('chartData' in row_dict and row_dict['chartData'] and
                'data' in row_dict['chartData'] and row_dict['chartData']['data'] and
                'data' in row_dict['chartData']['data'] and
                len(row_dict['chartData']['data']['data']) > 0 and
                'charts' in row_dict['chartData']['data']['data'][0] and
                row_dict['chartData']['data']['data'][0]['charts'] and
                len(row_dict['chartData']['data']['data'][0]['charts']) > 0):
                temp_dict['charts'] = row_dict['chartData']['data']['data'][0]['charts'][0]['type']
                temp_dict['chartData'] = row_dict['chartData']['data']['data'][0]['charts'][0]
            else:
                print("No valid chart data found in row index", idx)
                temp_dict['charts'] = None
                temp_dict['chartData'] = {}
            return temp_dict

        if 'resizedColumnSizes' in row_dict:
            temp_dict['type'] = 'col'
            if len(row_dict['resizedColumnSizes']) == 1:
                temp_dict['ratio'] = [row_dict['resizedColumnSizes'][0]['ratio']]
                temp_dict0 = self.read_column_data(row_dict['columns'][0], 0, temp_dict['id'])
                if temp_dict0['type'] == 'chart':
                    temp_dict['charts'] = [temp_dict0]
                else:
                    temp_dict['children'] = [temp_dict0]
            else:
                temp_dict['ratio'] = [row_dict['resizedColumnSizes'][0]['ratio'],
                                        row_dict['resizedColumnSizes'][1]['ratio']]
                temp_dict0 = self.read_column_data(row_dict['columns'][0], 0, temp_dict['id'])
                temp_dict1 = self.read_column_data(row_dict['columns'][1], 1, temp_dict['id'])
                if (temp_dict0['type'] == 'chart') and (temp_dict1['type'] != 'chart'):
                    temp_dict['charts'] = [temp_dict0]
                    temp_dict['children'] = [temp_dict1]
                elif (temp_dict0['type'] != 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict1]
                    temp_dict['children'] = [temp_dict0]
                elif (temp_dict0['type'] == 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict0, temp_dict1]
                    temp_dict['children'] = []
                else:
                    temp_dict['children'] = [temp_dict0, temp_dict1]
            return temp_dict

        if 'resizedRowSizes' in row_dict:
            temp_dict['type'] = 'row'
            if len(row_dict['resizedRowSizes']) == 1:
                temp_dict0 = self.read_row_data(row_dict['rows'][0], 0, temp_dict['id'])
                temp_dict['ratio'] = [row_dict['resizedRowSizes'][0]['ratio']]
                if temp_dict0['type'] == 'chart':
                    temp_dict['charts'] = [temp_dict0]
                else:
                    temp_dict['children'] = [temp_dict0]
            else:
                temp_dict0 = self.read_row_data(row_dict['rows'][0], 0, temp_dict['id'])
                temp_dict1 = self.read_row_data(row_dict['rows'][1], 1, temp_dict['id'])
                temp_dict['ratio'] = [row_dict['resizedRowSizes'][0]['ratio'],
                                        row_dict['resizedRowSizes'][1]['ratio']]
                if (temp_dict0['type'] == 'chart') and (temp_dict1['type'] != 'chart'):
                    temp_dict['charts'] = [temp_dict0]
                    temp_dict['children'] = [temp_dict1]
                elif (temp_dict0['type'] != 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict1]
                    temp_dict['children'] = [temp_dict0]
                elif (temp_dict0['type'] == 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict0, temp_dict1]
                    temp_dict['children'] = []
                else:
                    temp_dict['children'] = [temp_dict0, temp_dict1]
            return temp_dict

    def read_column_data(self, column_dict, idx, id):
        temp_dict = {}
        temp_dict['id'] = str(id) + "_col" + str(idx)
        temp_dict['parent_index'] = idx

        if column_dict['type'] == 'chart':
            temp_dict['type'] = 'chart'
            if ('chartData' in column_dict and column_dict['chartData'] and
                'data' in column_dict['chartData'] and column_dict['chartData']['data'] and
                'data' in column_dict['chartData']['data'] and
                len(column_dict['chartData']['data']['data']) > 0 and
                'charts' in column_dict['chartData']['data']['data'][0] and
                column_dict['chartData']['data']['data'][0]['charts'] and
                len(column_dict['chartData']['data']['data'][0]['charts']) > 0):
                temp_dict['charts'] = column_dict['chartData']['data']['data'][0]['charts'][0]['type']
                temp_dict['chartData'] = column_dict['chartData']['data']['data'][0]['charts'][0]
            else:
                print("No valid chart data found in column index", idx)
                temp_dict['charts'] = None
                temp_dict['chartData'] = {}
            return temp_dict

        if 'resizedColumnSizes' in column_dict:
            temp_dict['type'] = 'col'
            if len(column_dict['resizedColumnSizes']) == 1:
                temp_dict['ratio'] = [column_dict['resizedColumnSizes'][0]['ratio']]
                temp_dict0 = self.read_column_data(column_dict['columns'][0], 0, temp_dict['id'])
                if temp_dict0['type'] == 'chart':
                    temp_dict['charts'] = [temp_dict0]
                else:
                    temp_dict['children'] = [temp_dict0]
            else:
                temp_dict['ratio'] = [column_dict['resizedColumnSizes'][0]['ratio'],
                                        column_dict['resizedColumnSizes'][1]['ratio']]
                temp_dict0 = self.read_column_data(column_dict['columns'][0], 0, temp_dict['id'])
                temp_dict1 = self.read_column_data(column_dict['columns'][1], 1, temp_dict['id'])
                if (temp_dict0['type'] == 'chart') and (temp_dict1['type'] != 'chart'):
                    temp_dict['charts'] = [temp_dict0]
                    temp_dict['children'] = [temp_dict1]
                elif (temp_dict0['type'] != 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict1]
                    temp_dict['children'] = [temp_dict0]
                elif (temp_dict0['type'] == 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict0, temp_dict1]
                    temp_dict['children'] = []
                else:
                    temp_dict['children'] = [temp_dict0, temp_dict1]
            return temp_dict

        if 'resizedRowSizes' in column_dict:
            temp_dict['type'] = 'row'
            if len(column_dict['resizedRowSizes']) == 1:
                temp_dict0 = self.read_row_data(column_dict['rows'][0], 0, temp_dict['id'])
                temp_dict['ratio'] = [column_dict['resizedRowSizes'][0]['ratio']]
                if temp_dict0['type'] == 'chart':
                    temp_dict['charts'] = [temp_dict0]
                else:
                    temp_dict['children'] = [temp_dict0]
            else:
                temp_dict0 = self.read_row_data(column_dict['rows'][0], 0, temp_dict['id'])
                temp_dict1 = self.read_row_data(column_dict['rows'][1], 1, temp_dict['id'])
                temp_dict['ratio'] = [column_dict['resizedRowSizes'][0]['ratio'],
                                        column_dict['resizedRowSizes'][1]['ratio']]
                if (temp_dict0['type'] == 'chart') and (temp_dict1['type'] != 'chart'):
                    temp_dict['charts'] = [temp_dict0]
                    temp_dict['children'] = [temp_dict1]
                elif (temp_dict0['type'] != 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict1]
                    temp_dict['children'] = [temp_dict0]
                elif (temp_dict0['type'] == 'chart') and (temp_dict1['type'] == 'chart'):
                    temp_dict['charts'] = [temp_dict0, temp_dict1]
                    temp_dict['children'] = []
                else:
                    temp_dict['children'] = [temp_dict0, temp_dict1]
            return temp_dict

    # ----------------------------------------------
    # Transformation Function to Build Grid Data
    # ----------------------------------------------
    def transform_input_to_structure_v4(self, response_dict):
        temp_dict = {}
        main_ratios = [item['ratio'] for item in response_dict['dimensions']['main']]
        temp_dict['main'] = {'ratio': main_ratios}

        if 'row' in response_dict['dimensions']:
            if response_dict['dimensions']['row'] is not None:
                if isinstance(response_dict['dimensions']['row'], list):
                    row_ratios = [item['ratio'] for item in response_dict['dimensions']['row']]
                    row_charts = []
                    row_children = []
                    split_type = 'row'

                    if isinstance(response_dict.get('rows'), list) and response_dict['rows']:
                        for idx, row in enumerate(response_dict['rows']):
                            if row['type'] == 'chart':
                                if ('chartData' in row and row['chartData'] and
                                    'data' in row['chartData'] and row['chartData']['data'] and
                                    'data' in row['chartData']['data'] and
                                    len(row['chartData']['data']['data']) > 0 and
                                    'charts' in row['chartData']['data']['data'][0] and
                                    row['chartData']['data']['data'][0]['charts'] and
                                    len(row['chartData']['data']['data'][0]['charts']) > 0):
                                    charts = row['chartData']['data']['data'][0]['charts'][0]['type']
                                    chartData = row['chartData']['data']['data'][0]['charts'][0]
                                else:
                                    print("No valid chart data found in row index", idx)
                                    charts = None
                                    chartData = {}
                                row_charts.append({'parent_index': idx, 'charts': charts, 'chartData': chartData})
                            elif row['type'] != 'chart':
                                if 'resizedColumnSizes' in row:
                                    split_type = 'col'
                                    row_children.append(self.read_column_data(row, idx, 'row'))
                                elif 'resizedRowSizes' in row:
                                    split_type = 'row'
                                    row_children.append(self.read_row_data(row, idx, 'row'))

                    temp_dict['row_ratios_1'] = {
                        'id': 'row',
                        'type': split_type,
                        'ratio': row_ratios,
                        'children': row_children,
                        'charts': row_charts
                    }

        if 'column' in response_dict['dimensions']:
            if response_dict['dimensions']['column'] is not None:
                if isinstance(response_dict['dimensions']['column'], list):
                    col_ratios = [item['ratio'] for item in response_dict['dimensions']['column']]
                    col_charts = []
                    col_children = []
                    split_type = ''
                    if isinstance(response_dict.get('columns'), list) and response_dict['columns']:
                        for idx, col in enumerate(response_dict['columns']):
                            if col['type'] == 'chart':
                                if ('chartData' in col and col['chartData'] and
                                    'data' in col['chartData'] and col['chartData']['data'] and
                                    'data' in col['chartData']['data'] and
                                    len(col['chartData']['data']['data']) > 0 and
                                    'charts' in col['chartData']['data']['data'][0] and
                                    col['chartData']['data']['data'][0]['charts'] and
                                    len(col['chartData']['data']['data'][0]['charts']) > 0):
                                    charts = col['chartData']['data']['data'][0]['charts'][0]['type']
                                    chartData = col['chartData']['data']['data'][0]['charts'][0]
                                else:
                                    print("No valid chart data found in column index", idx)
                                    charts = None
                                    chartData = {}
                                col_charts.append({'parent_index': idx, 'charts': charts, 'chartData': chartData})
                            elif col['type'] != 'chart':
                                if 'resizedColumnSizes' in col:
                                    split_type = 'col'
                                    col_children.append(self.read_column_data(col, idx, 'row'))
                                elif 'resizedRowSizes' in col:
                                    split_type = 'row'
                                    col_children.append(self.read_row_data(col, idx, 'row'))
                    temp_dict['column_ratios_1'] = {
                        'id': 'column',
                        'type': split_type,
                        'ratio': col_ratios,
                        'children': col_children,
                        'charts': col_charts
                    }

        return temp_dict

    # ----------------------------------------------
    # Grid Processing and Figure Creation
    # ----------------------------------------------
    def process_grid_v2(self, fig, parent_spec, grid_data, orientation="col"):
        id_ = grid_data["id"]
        ratios = grid_data["ratio"]
        num_splits = len(ratios)

        if orientation == "row":
            grid_spec = gridspec.GridSpecFromSubplotSpec(
                1, num_splits, subplot_spec=parent_spec, width_ratios=ratios
            )
        else:
            grid_spec = gridspec.GridSpecFromSubplotSpec(
                num_splits, 1, subplot_spec=parent_spec, height_ratios=ratios
            )

        for idx in range(num_splits):
            ax = fig.add_subplot(grid_spec[idx] if orientation == "col" else grid_spec[:, idx])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)
            for spine in ['top', 'right', 'left', 'bottom']:
                ax.spines[spine].set_visible(False)

            if "charts" in grid_data:
                for chart in grid_data["charts"]:
                    if chart["parent_index"] == idx:
                        self.plot_from_figure_dict(chart['chartData'], ax)

            if "children" in grid_data:
                for child in grid_data["children"]:
                    if child["parent_index"] == idx:
                        self.process_grid_v2(
                            fig,
                            grid_spec[idx] if orientation == "col" else grid_spec[:, idx],
                            child,
                            orientation=child.get("type", "col")
                        )

    def createGrid_v2(self):
        main_ratios = self.grid_data["main"]["ratio"]
        fig = plt.figure(figsize=(8, 8))

        if len(main_ratios) == 1:
            main_grid = gridspec.GridSpec(1, 1, figure=fig)
            main_cell = main_grid[0]
        else:
            main_grid = gridspec.GridSpec(len(main_ratios), 1, figure=fig, height_ratios=main_ratios)
            main_cell = main_grid[0]

        if 'row_ratios_1' in self.grid_data:
            row_data = self.grid_data['row_ratios_1']
            row_ratios = row_data["ratio"]
            children = row_data.get('children', [])
            parent_spec = main_cell
            sub_grid = gridspec.GridSpecFromSubplotSpec(
                1, len(row_ratios),
                subplot_spec=parent_spec,
                width_ratios=row_ratios
            )

            for j in range(len(row_ratios)):
                ax = fig.add_subplot(sub_grid[0, j])
                ax.set_xticks([])
                ax.set_yticks([])
                ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)
                for spine in ['top', 'right', 'left', 'bottom']:
                    ax.spines[spine].set_visible(False)

                if "charts" in row_data:
                    for chart in row_data["charts"]:
                        if chart["parent_index"] == j:
                            self.plot_from_figure_dict(chart['chartData'], ax)
                for child in children:
                    if child['parent_index'] == j:
                        self.process_grid_v2(fig, sub_grid[0, j], child, orientation=child.get("type", "col"))

        if 'column_ratios_1' in self.grid_data:
            col_data = self.grid_data['column_ratios_1']
            col_ratios = col_data["ratio"]
            children = col_data.get('children', [])
            parent_spec = main_cell if len(main_ratios) == 1 else main_grid[1]
            sub_grid = gridspec.GridSpecFromSubplotSpec(
                len(col_ratios), 1,
                subplot_spec=parent_spec,
                height_ratios=col_ratios, hspace=0.5
            )

            for j in range(len(col_ratios)):
                ax = fig.add_subplot(sub_grid[j, 0])
                ax.set_xticks([])
                ax.set_yticks([])
                ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)
                for spine in ['top', 'right', 'left', 'bottom']:
                    ax.spines[spine].set_visible(False)

                if "charts" in col_data:
                    for chart in col_data["charts"]:
                        if chart["parent_index"] == j:
                            self.plot_from_figure_dict(chart['chartData'], ax)
                for child in children:
                    if child['parent_index'] == j:
                        self.process_grid_v2(fig, sub_grid[j, 0], child, orientation=child.get("type", "col"))

        plt.subplots_adjust(bottom=0.1, top=0.9, hspace=0.5)
        plt.tight_layout()
        #plt.show()
        return fig

    
    def export(self):
        fig = self.createGrid_v2()
        return fig

import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Documents:
    def __init__(self, json_data):
      
        self.json_data = json_data
        self.pages = [Page(page) for page in json_data.get("pages", [])]  

    def export(self, output_pdf="final_output.pdf"):
       
        #start_time_total = time.time()

        with PdfPages(output_pdf) as pdf:
            for i, page in enumerate(self.pages):
                print(f"Processing Page {i+1}...")

                fig = page.export()  
                
                if fig is None:  
                    print(f"Warning: No figure generated for Page {i+1}, skipping...")
                    continue

               
                fig.suptitle(
                    f"Page {i + 1} - Document Title",  
                    fontsize=14, fontweight='bold', color='black', y=1.02  
                )

                fig.text(
                    0.95, 0.01,  
                    "ChartArt",  
                    fontsize=10, fontweight='normal', color='gray', ha='right'
                )

                pdf.savefig(fig, dpi=100, bbox_inches='tight')  
                plt.close(fig)

        #total_time_taken = time.time() - start_time_total

        print(f"\nDocument export completed.")
        #print(f"Total execution time: {total_time_taken:.2f} seconds")

__all__ = ["Documents"]
