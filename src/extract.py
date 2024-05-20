import re
import os
import math
import csv
import json
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def write_to_csv(data_list, csv_file):
    headers = list(data_list[0].keys())

    try:
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for data in data_list:
                row = [
                    data["website"],
                    data["global_rank"],
                    data["total_visits"],
                    data["bounce_rate"],
                    data["pages_per_visit"],
                    data["avg_visit_duration"],
                    data["visits_october"],
                    data["visits_november"],
                    data["visits_december"],
                    data["rank_october"],
                    data["rank_november"],
                    data["rank_december"],
                    json.dumps(data["top_countries"]),
                    data["age_distribution_18-25"],
                    data["age_distribution_25-34"],
                    data["age_distribution_35-44"],
                    data["age_distribution_45-54"],
                    data["age_distribution_55-64"],
                    data["age_distribution_65+"],
                ]
                writer.writerow(row)
        logger.info(f"data has been written to {csv_file}")
    except IOError:
        logger.error(f"error occured while writing to {csv_file}")


def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "lxml")

    website = (
        os.path.basename(file_path)
        .removeprefix("similarweb-")
        .removesuffix("-com.html")
    )

    data_dict = {
        "website": website,
        "global_rank": "",
        "total_visits": "",
        "bounce_rate": "",
        "pages_per_visit": "",
        "avg_visit_duration": "",
        "visits_october": "",
        "visits_november": "",
        "visits_december": "",
        "rank_october": -1,
        "rank_november": -1,
        "rank_december": -1,
        "top_countries": "",
        "age_distribution_18-25": "",
        "age_distribution_25-34": "",
        "age_distribution_35-44": "",
        "age_distribution_45-54": "",
        "age_distribution_55-64": "",
        "age_distribution_65+": "",
    }

    data_dict["global_rank"] = soup.find("p", class_="wa-rank-list__value").text.strip()

    total_visits = (
        soup.find("p", {"data-test": "total-visits"}).find_next_sibling("p").text
    )
    data_dict["total_visits"] = total_visits

    bounce_rate = (
        soup.find("p", {"data-test": "bounce-rate"}).find_next_sibling("p").text
    )
    data_dict["bounce_rate"] = bounce_rate

    pages_per_visit = (
        soup.find("p", {"data-test": "pages-per-visit"}).find_next_sibling("p").text
    )
    data_dict["pages_per_visit"] = pages_per_visit

    avg_visit_duration = (
        soup.find("p", {"data-test": "avg-visit-duration"}).find_next_sibling("p").text
    )
    data_dict["avg_visit_duration"] = avg_visit_duration

    data_labels = soup.select("tspan.wa-traffic__chart-data-label")

    if data_labels:
        data_dict["visits_october"] = data_labels[0].text
        data_dict["visits_november"] = data_labels[1].text
        data_dict["visits_december"] = data_labels[2].text

    top_countries_section = soup.find_all("div", class_="wa-geography__country-info")
    top_countries = {}
    for country_div in top_countries_section:
        country_name = country_div.find(
            ["a", "span"], class_="wa-geography__country-name"
        ).text
        country_traffic = country_div.find(
            "span", class_="wa-geography__country-traffic-value"
        ).text
        top_countries[country_name] = country_traffic

    data_dict["top_countries"] = top_countries

    percentage_labels = soup.select("tspan.wa-demographics__age-data-label")

    if percentage_labels:
        data_dict["age_distribution_18-25"] = percentage_labels[0].text
        data_dict["age_distribution_25-34"] = percentage_labels[1].text
        data_dict["age_distribution_35-44"] = percentage_labels[2].text
        data_dict["age_distribution_45-54"] = percentage_labels[3].text
        data_dict["age_distribution_55-64"] = percentage_labels[4].text
        data_dict["age_distribution_65+"] = percentage_labels[5].text

    plot_border = soup.select_one(".highcharts-plot-border")
    height = float(plot_border["height"])

    y_axis_labels = soup.select(
        ".highcharts-axis-labels.highcharts-yaxis-labels > text"
    )
    min_value = float(y_axis_labels[0].text.replace(",", ""))
    max_value = float(y_axis_labels[-1].text.replace(",", ""))

    markers = soup.select(
        ".highcharts-markers.highcharts-series-0.highcharts-line-series.highcharts-tracker > path"
    )
    y_coords = []
    for marker in markers:
        d_attr = marker["d"]
        y_coord = float(d_attr.split()[-2])
        y_coords.append(y_coord)

    y_axis_values = []
    for y_coord in y_coords:
        y_axis_value = min_value + ((max_value - min_value) / height) * (y_coord)
        y_axis_values.append(math.floor(y_axis_value))

    data_dict["rank_october"] = y_axis_values[0]
    data_dict["rank_november"] = y_axis_values[1]
    data_dict["rank_december"] = y_axis_values[2]

    logger.info(f"HTML parsing complete for {file_path}")
    return data_dict
