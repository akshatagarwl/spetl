import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def clean(path):
    df = pd.read_csv(path)

    df.replace("- -", np.nan, inplace=True)
    df.replace("--", np.nan, inplace=True)

    df["global_rank"] = (
        df["global_rank"]
        .astype(str)
        .str.removeprefix("#")
        .str.replace(",", "")
        .astype(int)
    )

    df["total_visits"] = (
        df["total_visits"]
        .astype(str)
        .str.removeprefix("< ")
        .replace({"K": "*1e3", "M": "*1e6", "B": "*1e9"}, regex=True)
        .map(pd.eval)
        .astype(int)
    )
    df["visits_october"] = df["visits_october"].fillna(-1)
    df["visits_october"] = (
        df["visits_october"]
        .astype(str)
        .replace({"K": "*1e3", "M": "*1e6", "B": "*1e9"}, regex=True)
        .map(pd.eval)
        .astype(int)
    )
    df["visits_october"] = df["visits_october"].replace(-1, np.nan)

    df["visits_november"] = df["visits_november"].fillna(-1)
    df["visits_november"] = (
        df["visits_november"]
        .astype(str)
        .replace({"K": "*1e3", "M": "*1e6", "B": "*1e9"}, regex=True)
        .map(pd.eval)
        .astype(int)
    )
    df["visits_november"] = df["visits_november"].replace(-1, np.nan)

    df["visits_december"] = df["visits_december"].fillna(-1)
    df["visits_december"] = (
        df["visits_december"]
        .astype(str)
        .replace({"K": "*1e3", "M": "*1e6", "B": "*1e9"}, regex=True)
        .map(pd.eval)
        .astype(int)
    )
    df["visits_december"] = df["visits_december"].replace(-1, np.nan)

    df["bounce_rate"] = (
        df["bounce_rate"].astype(str).str.replace("%", "").astype(float) / 100
    )

    df["pages_per_visit"] = df["pages_per_visit"].astype(float)

    df["avg_visit_duration"] = pd.to_timedelta(
        df["avg_visit_duration"]
    ).dt.total_seconds()

    df["age_distribution_18-25"] = (
        df["age_distribution_18-25"].astype(str).str.replace("%", "").astype(float)
        / 100
    )
    df["age_distribution_25-34"] = (
        df["age_distribution_25-34"].astype(str).str.replace("%", "").astype(float)
        / 100
    )
    df["age_distribution_35-44"] = (
        df["age_distribution_35-44"].astype(str).str.replace("%", "").astype(float)
        / 100
    )
    df["age_distribution_45-54"] = (
        df["age_distribution_45-54"].astype(str).str.replace("%", "").astype(float)
        / 100
    )
    df["age_distribution_55-64"] = (
        df["age_distribution_55-64"].astype(str).str.replace("%", "").astype(float)
        / 100
    )
    df["age_distribution_65+"] = (
        df["age_distribution_65+"].astype(str).str.replace("%", "").astype(float) / 100
    )

    return df
