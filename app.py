import json

from flask import Flask, abort, jsonify, request

import inspection
from inspector import Inspector

app = Flask(__name__)


@app.route("/search", methods=["GET"])
def search():
    restaurant_name = request.args.get("restaurant_name")
    cuisine = request.args.get("cuisine")
    zip_code = request.args.get("zip_code")
    limit = request.args.get("limit")
    results = []

    if limit == None:
        limit = 10
    else:
        limit = int(limit)

    for inspection in Inspector.get_inspections():
        if not restaurant_name or restaurant_name.lower() in inspection.restaurant_name.lower():
            if not cuisine or cuisine.lower() in inspection.cuisine.lower():
                if not zip_code or zip_code.lower() in inspection.zipcode.lower():
                    results.append(inspection)

    results.sort(key=lambda x: x.restaurant_id)


    results = results[:limit]

    output = []
    for data in results:
        output.append(data.to_json())

    return jsonify({"data":output})























if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
