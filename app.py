from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Nifty Option Chain Server Running"

@app.route("/nifty")
def nifty_option_chain():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

        session = requests.Session()

        # First request to get cookies (VERY IMPORTANT for NSE)
        session.get("https://www.nseindia.com", headers=headers)

        response = session.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch from NSE",
                "status_code": response.status_code
            })

        data = response.json()

        if "records" not in data:
            return jsonify({"error": "Invalid response structure from NSE"})

        records = data["records"]["data"]

        output = []

        for row in records:
            if "CE" in row and "PE" in row:
                output.append({
                    "strike": row.get("strikePrice"),
                    "ce_oi": row["CE"].get("openInterest", 0),
                    "ce_change_oi": row["CE"].get("changeinOpenInterest", 0),
                    "pe_oi": row["PE"].get("openInterest", 0),
                    "pe_change_oi": row["PE"].get("changeinOpenInterest", 0)
                })

        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
