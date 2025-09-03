"""
A Flask REST API for querying Olympic athlete data and KPIs.
"""

import json
from typing import Dict, Tuple

import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)


def load_data() -> Tuple[pd.DataFrame, Dict]:
    """
    Load and prepare Olympic data and KPIs.

    Returns:
        tuple: (merged_dataframe, kpi_dictionary)
    """
    data_parquet = "cleaned_olympic_data.parquet"
    noc_regions_csv = "noc_regions.csv"
    kpi_json = "olympic_kpi.json"

    df = pd.read_parquet(data_parquet, engine="fastparquet")
    noc_regions = pd.read_csv(noc_regions_csv)
    df_merged = df.merge(noc_regions, how="left", on="NOC")

    with open(kpi_json, "r", encoding="utf-8") as f:
        kpi_data = json.load(f)

    return df_merged, kpi_data


df, kpi = load_data()


@app.route("/athlete_data_by_noc", methods=["GET"])
def athlete_data_by_noc():
    """
    Get athlete data filtered by NOC (National Olympic Committee) code.

    Query Parameters:
        noc (str): NOC code

    Returns:
        JSON: List of athletes with Name, Sport, Medal, and region
    """
    noc_code = request.args.get("noc", "").upper().strip()
    filtered_df = df[df["NOC"] == noc_code]

    if filtered_df.empty:
        return jsonify(
            {
                "message": f"No athletes found for NOC code: {noc_code}",
                "noc": noc_code,
                "data": [],
            }
        )

    result_df = filtered_df[["Name", "Sport", "Medal", "region"]].copy()
    athletes_data = result_df.to_dict(orient="records")

    return jsonify(
        {
            "noc": noc_code,
            "region": (
                athletes_data[0]["region"] if athletes_data else "Unknown Region"
            ),
            "total_records": len(athletes_data),
            "data": athletes_data,
        }
    )


@app.route("/kpi", methods=["GET"])
def get_kpi():
    """
    Get calculated KPIs.

    Returns:
        JSON: Dictionary of KPI metrics
    """
    kpi_response = {
        "metrics": kpi,
        "sports_count": len(kpi),
        "analysis_period": "2000-present",
    }

    return jsonify(kpi_response)


if __name__ == "__main__":
    app.run(debug=True)
