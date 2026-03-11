from flask import Flask, jsonify, request, send_file
import pandas as pd
from sklearn.cluster import KMeans

app = Flask(__name__)

# Load CSV once at startup
df = pd.read_csv("All_Diets.csv")
df = df.rename(columns={"Protein(g)": "Protein", "Carbs(g)": "Carbs", "Fat(g)": "Fat"})
df[["Protein", "Carbs", "Fat"]] = df[["Protein", "Carbs", "Fat"]].fillna(df[["Protein", "Carbs", "Fat"]].mean())

# Get all unique diet types for the filter dropdown
diet_types = sorted(df["Diet_type"].str.strip().str.lower().unique())


@app.route("/")
def index():
    return send_file("dashboard.html")


@app.route("/api/diet-types")
def get_diet_types():
    """Return all unique diet types for populating the filter dropdown."""
    types = sorted(df["Diet_type"].str.strip().unique(), key=str.lower)
    return jsonify({"data": types})


@app.route("/api/nutritional-insights")
def nutritional_insights():
    """Average Protein, Carbs, Fat per diet type. Optional ?diet= filter."""
    filtered = df.copy()
    diet = request.args.get("diet", "").strip()
    if diet and diet.lower() != "all":
        filtered = filtered[filtered["Diet_type"].str.lower() == diet.lower()]

    avg = filtered.groupby("Diet_type")[["Protein", "Carbs", "Fat"]].mean().reset_index()
    avg = avg.round(2)
    return jsonify({"data": avg.to_dict(orient="records")})


@app.route("/api/recipes")
def recipes():
    """Paginated recipe list. Optional ?diet= filter, ?page= and ?per_page= for pagination."""
    filtered = df.copy()
    diet = request.args.get("diet", "").strip()
    if diet and diet.lower() != "all":
        filtered = filtered[filtered["Diet_type"].str.lower() == diet.lower()]

    page = max(1, request.args.get("page", 1, type=int))
    per_page = max(1, min(100, request.args.get("per_page", 10, type=int)))

    total = len(filtered)
    total_pages = max(1, -(-total // per_page))  # ceiling division
    page = min(page, total_pages)

    start = (page - 1) * per_page
    end = start + per_page
    page_data = filtered.iloc[start:end]

    records = page_data[["Diet_type", "Recipe_name", "Cuisine_type", "Protein", "Carbs", "Fat"]].to_dict(orient="records")

    return jsonify({
        "data": records,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages
    })


@app.route("/api/clusters")
def clusters():
    """KMeans clustering of diet types based on average macronutrients."""
    avg = df.groupby("Diet_type")[["Protein", "Carbs", "Fat"]].mean().reset_index()

    n_clusters = min(3, len(avg))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    avg["cluster"] = kmeans.fit_predict(avg[["Protein", "Carbs", "Fat"]])

    avg = avg.round(2)
    return jsonify({"data": avg.to_dict(orient="records")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
