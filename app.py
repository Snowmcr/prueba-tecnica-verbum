from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

df = pd.read_parquet("cleaned_olympic_data.parquet", engine="fastparquet")
noc_regions = pd.read_csv("noc_regions.csv")

df = df.merge(noc_regions, how="left", on="NOC")

with open("kpi.json", "r") as f:
    kpi = json.load(f)


# Toma un código NOC como parámetro de consulta y devuelve una lista JSON de todos los atletas (Nombre, Deporte, Medalla) de ese NOC. Agrega el nombre del país a cada elemento de la lista JSON
@app.route("/athlete_data_by_noc", methods=["GET"])
def athlete_data_by_noc():
    # Obtener NOC
    noc_code = request.args.get("noc").upper()
    if not noc_code:
        return jsonify({"error": "NOC code is required"}), 400

    # Filtrar atletas por NOC
    filtered_df = df[df["NOC"] == noc_code][["Name", "Sport", "Medal", "region"]]
    result = filtered_df.to_dict(orient="records")

    return jsonify(result)


@app.route("/kpi", methods=["GET"])
def get_kpi():
    return jsonify(kpi)


if __name__ == "__main__":
    app.run(debug=True)
