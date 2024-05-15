import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

def plot_visits_month_on_month(df):
    df["percentage_visits_change_oct_nov"] = (
        (df["visits_october"] - df["visits_november"]) / df["visits_october"]
    ) * 100
    df["percentage_visits_change_nov_dec"] = (
        (df["visits_november"] - df["visits_december"]) / df["visits_november"]
    ) * 100

    # FIXME(akshat): avoid recreation of dataframe here
    df_plot = pd.DataFrame(
        {
            "Website": df["website"].tolist() * 2,
            "Percentage Change": df["percentage_visits_change_oct_nov"].tolist()
            + df["percentage_visits_change_nov_dec"].tolist(),
            "Period": ["Oct-Nov"] * len(df) + ["Nov-Dec"] * len(df),
        }
    )

    plt.figure(figsize=(12, 8))
    plot = sns.barplot(
        x="Website",
        y="Percentage Change",
        hue="Period",
        data=df_plot,
        palette=["lightcoral", "skyblue"],
    )
    plt.title("Month-on-Month Visits Change in Percentage for Each Website")
    plt.xlabel("Website")
    plt.ylabel("Percentage Visits Change (%)")
    plt.grid(True, linestyle="--", alpha=0.5)

    for bar in plot.patches:
        height = bar.get_height()
        if height != 0:
            annot_text = f"{height:.1f}%"
            plot.annotate(
                annot_text,
                (bar.get_x() + bar.get_width() / 2, height),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
                color="black",
            )

    plt.legend(title="Period")

    filename = "plots/visits_month_on_month.png"
    plt.savefig(filename)
    logger.info(f"plotted month on month growth in visits in {filename}")


def plot_rank_month_on_month(df):
    df["percentage_rank_change_oct_nov"] = (
        (df["rank_october"] - df["rank_november"]) / df["rank_october"]
    ) * 100
    df["percentage_rank_change_nov_dec"] = (
        (df["rank_november"] - df["rank_december"]) / df["rank_november"]
    ) * 100

    # FIXME(akshat): avoid recreation of dataframe here
    df_plot = pd.DataFrame(
        {
            "Website": df["website"].tolist() * 2,
            "Percentage Change": df["percentage_rank_change_oct_nov"].tolist()
            + df["percentage_rank_change_nov_dec"].tolist(),
            "Period": ["Oct-Nov"] * len(df) + ["Nov-Dec"] * len(df),
        }
    )

    plt.figure(figsize=(12, 8))
    plot = sns.barplot(
        x="Website",
        y="Percentage Change",
        hue="Period",
        data=df_plot,
        palette=["lightcoral", "skyblue"],
    )
    plt.title("Month-on-Month Rank Change in Percentage for Each Website")
    plt.xlabel("Website")
    plt.ylabel("Percentage Rank Change (%)")
    plt.grid(True, linestyle="--", alpha=0.5)

    for bar in plot.patches:
        height = bar.get_height()
        if height != 0:
            annot_text = f"{height:.1f}%"
            plot.annotate(
                annot_text,
                (bar.get_x() + bar.get_width() / 2, height),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
                color="black",
            )

    plt.legend(title="Period")

    filename = "plots/rank_month_on_month.png"
    plt.savefig(filename)
    logger.info(f"plotted month on month growth in rank in {filename}")


def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())


def plot_growth_score(df):
    weight_visits = 0.5
    weight_rank = 0.5

    df["visits_growth"] = (df["visits_december"] - df["visits_october"]) / df[
        "visits_october"
    ]
    df["normalized_visits_growth"] = min_max_normalize(df["visits_growth"])

    df["rank_growth"] = -(df["rank_december"] - df["rank_october"]) / df["rank_october"]
    df["normalized_rank_growth"] = min_max_normalize(df["rank_growth"])

    df["normalized_growth_score"] = (
        weight_visits * df["normalized_visits_growth"]
        + weight_rank * df["normalized_rank_growth"]
    )

    df = df.sort_values("normalized_growth_score", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(df["website"], df["normalized_growth_score"], color="skyblue")
    plt.xlabel("Normalized Growth Score")
    plt.ylabel("Website")
    plt.title("Website Growth Score")

    filename = "plots/growth_score.png"
    plt.savefig(filename)
    logger.info(f"plotted growth score in {filename}")
