import os
import uuid

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from django.conf import settings


# =========================================================
# DATASET LOADER
# =========================================================

def load_dataset_for_visualization(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":

        try:
            df = pd.read_csv(file_path)

        except UnicodeDecodeError:
            df = pd.read_csv(
                file_path,
                encoding="latin-1"
            )

    elif extension == ".xlsx":

        df = pd.read_excel(
            file_path,
            engine="openpyxl"
        )

    elif extension == ".xls":

        df = pd.read_excel(
            file_path,
            engine="xlrd"
        )

    else:

        raise ValueError(
            "Unsupported file format."
        )

    df.columns = df.columns.astype(str)

    return df


# =========================================================
# CREATE VISUALIZATION DIRECTORY
# =========================================================

def get_visualization_directory(dataset_id):

    directory = os.path.join(

        settings.MEDIA_ROOT,

        "visualizations",

        str(dataset_id)

    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    return directory


# =========================================================
# GENERATE UNIQUE FILE NAME
# =========================================================

def generate_filename(prefix):

    unique_id = uuid.uuid4().hex[:8]

    return f"{prefix}_{unique_id}.png"


# =========================================================
# HISTOGRAM
# =========================================================

def create_histogram(

    df,
    column,
    directory

):

    filename = generate_filename(
        f"histogram_{column}"
    )

    file_path = os.path.join(
        directory,
        filename
    )

    plt.figure(figsize=(10, 6))

    sns.histplot(

        df[column].dropna(),

        kde=True

    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(column)

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=100
    )

    plt.close()

    return filename


# =========================================================
# BOX PLOT
# =========================================================

def create_boxplot(

    df,
    column,
    directory

):

    filename = generate_filename(
        f"boxplot_{column}"
    )

    file_path = os.path.join(
        directory,
        filename
    )

    plt.figure(figsize=(10, 6))

    sns.boxplot(

        x=df[column].dropna()

    )

    plt.title(
        f"Box Plot of {column}"
    )

    plt.xlabel(column)

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=100
    )

    plt.close()

    return filename


# =========================================================
# BAR CHART
# =========================================================

def create_bar_chart(

    df,
    column,
    directory

):

    value_counts = (

        df[column]

        .astype(str)

        .value_counts()

        .head(15)

    )

    if len(value_counts) == 0:

        return None

    filename = generate_filename(
        f"bar_chart_{column}"
    )

    file_path = os.path.join(
        directory,
        filename
    )

    plt.figure(figsize=(12, 6))

    value_counts.plot(
        kind="bar"
    )

    plt.title(
        f"Top Values in {column}"
    )

    plt.xlabel(column)

    plt.ylabel("Count")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=100
    )

    plt.close()

    return filename


# =========================================================
# PIE CHART
# =========================================================

def create_pie_chart(

    df,
    column,
    directory

):

    value_counts = (

        df[column]

        .astype(str)

        .value_counts()

        .head(10)

    )

    if len(value_counts) < 2:

        return None

    filename = generate_filename(
        f"pie_chart_{column}"
    )

    file_path = os.path.join(
        directory,
        filename
    )

    plt.figure(figsize=(9, 9))

    plt.pie(

        value_counts.values,

        labels=value_counts.index,

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=100
    )

    plt.close()

    return filename


# =========================================================
# CORRELATION HEATMAP
# =========================================================

def create_correlation_heatmap(

    df,
    directory

):

    numerical_df = df.select_dtypes(
        include=["number"]
    )

    if numerical_df.shape[1] < 2:

        return None

    correlation = numerical_df.corr()

    filename = generate_filename(
        "correlation_heatmap"
    )

    file_path = os.path.join(
        directory,
        filename
    )

    plt.figure(

        figsize=(12, 8)

    )

    sns.heatmap(

        correlation,

        annot=True,

        fmt=".2f",

        linewidths=0.5

    )

    plt.title(
        "Correlation Heatmap"
    )

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=100
    )

    plt.close()

    return filename


# =========================================================
# SCATTER PLOTS
# =========================================================

def create_scatter_plot(

    df,
    column_x,
    column_y,
    directory

):

    plot_df = df[
        [column_x, column_y]
    ].dropna()

    if len(plot_df) == 0:

        return None

    filename = generate_filename(

        f"scatter_{column_x}_{column_y}"

    )

    file_path = os.path.join(

        directory,

        filename

    )

    plt.figure(
        figsize=(10, 6)
    )

    sns.scatterplot(

        data=plot_df,

        x=column_x,

        y=column_y

    )

    plt.title(

        f"{column_x} vs {column_y}"

    )

    plt.tight_layout()

    plt.savefig(

        file_path,

        dpi=100

    )

    plt.close()

    return filename


# =========================================================
# COMPLETE VISUALIZATION GENERATOR
# =========================================================

def generate_visualizations(

    file_path,
    dataset_id,
    request

):

    df = load_dataset_for_visualization(
        file_path
    )

    directory = get_visualization_directory(
        dataset_id
    )

    visualizations = {

        "histograms": [],

        "boxplots": [],

        "bar_charts": [],

        "pie_charts": [],

        "scatter_plots": [],

        "correlation_heatmap": None,

    }


    # =====================================================
    # NUMERICAL COLUMNS
    # =====================================================

    numerical_columns = (

        df.select_dtypes(

            include=["number"]

        ).columns.tolist()

    )


    # Limit columns to prevent generating too many images

    numerical_columns = numerical_columns[:10]


    for column in numerical_columns:

        try:

            filename = create_histogram(

                df,

                column,

                directory

            )

            visualizations["histograms"].append({

                "column": column,

                "url": request.build_absolute_uri(

                    settings.MEDIA_URL

                    + "visualizations/"

                    + str(dataset_id)

                    + "/"

                    + filename

                ),

            })

        except Exception:

            pass


        try:

            filename = create_boxplot(

                df,

                column,

                directory

            )

            visualizations["boxplots"].append({

                "column": column,

                "url": request.build_absolute_uri(

                    settings.MEDIA_URL

                    + "visualizations/"

                    + str(dataset_id)

                    + "/"

                    + filename

                ),

            })

        except Exception:

            pass


    # =====================================================
    # CATEGORICAL COLUMNS
    # =====================================================

    categorical_columns = (

        df.select_dtypes(

            include=[

                "object",

                "category",

                "bool"

            ]

        ).columns.tolist()

    )


    categorical_columns = categorical_columns[:10]


    for column in categorical_columns:

        unique_count = df[column].nunique()


        # Avoid charts with too many categories

        if unique_count > 30:

            continue


        try:

            filename = create_bar_chart(

                df,

                column,

                directory

            )


            if filename:

                visualizations["bar_charts"].append({

                    "column": column,

                    "url": request.build_absolute_uri(

                        settings.MEDIA_URL

                        + "visualizations/"

                        + str(dataset_id)

                        + "/"

                        + filename

                    ),

                })

        except Exception:

            pass


        # Pie charts only for smaller category counts

        if unique_count <= 10:

            try:

                filename = create_pie_chart(

                    df,

                    column,

                    directory

                )


                if filename:

                    visualizations["pie_charts"].append({

                        "column": column,

                        "url": request.build_absolute_uri(

                            settings.MEDIA_URL

                            + "visualizations/"

                            + str(dataset_id)

                            + "/"

                            + filename

                        ),

                    })

            except Exception:

                pass


    # =====================================================
    # CORRELATION HEATMAP
    # =====================================================

    try:

        filename = create_correlation_heatmap(

            df,

            directory

        )


        if filename:

            visualizations["correlation_heatmap"] = (

                request.build_absolute_uri(

                    settings.MEDIA_URL

                    + "visualizations/"

                    + str(dataset_id)

                    + "/"

                    + filename

                )

            )

    except Exception:

        pass


    # =====================================================
    # SCATTER PLOTS
    # =====================================================

    if len(numerical_columns) >= 2:

        max_scatter_plots = 5

        scatter_count = 0


        for i in range(

            len(numerical_columns)

        ):

            for j in range(

                i + 1,

                len(numerical_columns)

            ):

                if scatter_count >= max_scatter_plots:

                    break


                column_x = numerical_columns[i]

                column_y = numerical_columns[j]


                try:

                    filename = create_scatter_plot(

                        df,

                        column_x,

                        column_y,

                        directory

                    )


                    if filename:

                        visualizations[

                            "scatter_plots"

                        ].append({

                            "x_column": column_x,

                            "y_column": column_y,

                            "url": request.build_absolute_uri(

                                settings.MEDIA_URL

                                + "visualizations/"

                                + str(dataset_id)

                                + "/"

                                + filename

                            ),

                        })


                        scatter_count += 1


                except Exception:

                    pass


            if scatter_count >= max_scatter_plots:

                break


    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {

        "dataset_rows": int(len(df)),

        "dataset_columns": int(len(df.columns)),

        "visualizations": visualizations,

    }