"""Data visualisation: Matplotlib charts for the healthcare dataset."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend; notebooks still display figures
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from healthcare_analysis.analysis import (  # noqa: E402
    correlation_matrix, prevalence_by_group)

COLOURS = {"main": "#2a6f97", "alt": "#e07a5f", "grey": "#6c757d"}


def plot_age_distribution(df):
    """Histogram of patient ages with the mean marked.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(df["age"], bins=15, color=COLOURS["main"], edgecolor="white")
    ax.axvline(df["age"].mean(), color=COLOURS["alt"], linestyle="--",
               label=f"Mean = {df['age'].mean():.1f}")
    ax.set(title="Age Distribution of Patients", xlabel="Age (years)",
           ylabel="Number of patients")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_prevalence_by_age_group(df):
    """Grouped bar chart of diabetes and hypertension prevalence by age group.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table with ``age_group``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    diabetes = prevalence_by_group(df, "age_group", "diabetes")
    hyper = prevalence_by_group(df, "age_group", "hypertension")
    x = np.arange(len(diabetes))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(x - 0.2, diabetes.values, 0.4, label="Diabetes",
           color=COLOURS["main"])
    ax.bar(x + 0.2, hyper.values, 0.4, label="Hypertension",
           color=COLOURS["alt"])
    ax.set_xticks(x)
    ax.set_xticklabels(diabetes.index.astype(str))
    ax.set(title="Condition Prevalence by Age Group",
           xlabel="Age group (years)", ylabel="Prevalence (%)")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_glucose_by_diabetes(df):
    """Box plot of blood glucose for patients with and without diabetes.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.

    Returns
    -------
    matplotlib.figure.Figure
    """
    groups = [df.loc[df["diabetes"] == 0, "glucose"],
              df.loc[df["diabetes"] == 1, "glucose"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    box = ax.boxplot(groups, patch_artist=True,
                     tick_labels=["No diabetes", "Diabetes"])
    for patch, colour in zip(box["boxes"], [COLOURS["main"], COLOURS["alt"]]):
        patch.set_facecolor(colour)
    ax.set(title="Blood Glucose by Diabetes Status",
           ylabel="Glucose (mg/dL)")
    fig.tight_layout()
    return fig


def plot_bmi_vs_bp(df):
    """Scatter plot of BMI against systolic BP with a linear trend line.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.

    Returns
    -------
    matplotlib.figure.Figure
    """
    x = df["bmi"].to_numpy(dtype=float)
    y = df["systolic_bp"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(x, y, alpha=0.6, color=COLOURS["main"], s=22)
    ax.plot(xs, slope * xs + intercept, color=COLOURS["alt"],
            label=f"Trend: +{slope:.2f} mmHg per BMI unit")
    ax.set(title="BMI vs Systolic Blood Pressure", xlabel="BMI (kg/m²)",
           ylabel="Systolic BP (mmHg)")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(df):
    """Heatmap of correlations between clinical variables.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.

    Returns
    -------
    matplotlib.figure.Figure
    """
    corr = correlation_matrix(df)
    fig, ax = plt.subplots(figsize=(7.5, 6))
    image = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center",
                    va="center", fontsize=7)
    fig.colorbar(image, ax=ax, shrink=0.8)
    ax.set_title("Correlation Matrix of Clinical Variables")
    fig.tight_layout()
    return fig


CHARTS = {
    "age_distribution": plot_age_distribution,
    "prevalence_by_age_group": plot_prevalence_by_age_group,
    "glucose_by_diabetes": plot_glucose_by_diabetes,
    "bmi_vs_systolic_bp": plot_bmi_vs_bp,
    "correlation_heatmap": plot_correlation_heatmap,
}


def save_figure(fig, output_dir, name):
    """Save a figure as PNG and close it.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save.
    output_dir : str or pathlib.Path
        Destination folder (created if needed).
    name : str
        File name without extension.

    Returns
    -------
    pathlib.Path
        Path of the saved image.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def generate_all_charts(df, output_dir):
    """Create and save every chart in :data:`CHARTS`.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    output_dir : str or pathlib.Path
        Destination folder.

    Returns
    -------
    list of pathlib.Path
        Paths of the saved images.
    """
    return [save_figure(func(df), output_dir, name)
            for name, func in CHARTS.items()]
