import extract
import transform
import analyze
import load
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    html_files = [
        "assets/similarweb-byte-trading-com.html",
        "assets/similarweb-crunchbase-com.html",
        "assets/similarweb-google-com.html",
        "assets/similarweb-pitchbook-com.html",
        "assets/similarweb-stripe-com.html",
    ]

    all_data = []

    for file in html_files:
        result = extract.parse_html(file)
        all_data.append(result)

    extract.write_to_csv(all_data, "data/extracted.csv")

    df = transform.clean("data/extracted.csv")

    load.write_to_sqlite(df)

    analyze.plot_visits_month_on_month(df)
    analyze.plot_rank_month_on_month(df)
    analyze.plot_growth_score(df)


if __name__ == "__main__":
    main()
