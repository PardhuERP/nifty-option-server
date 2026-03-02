from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Nifty Option Chain Server Running"

@app.route("/nifty")
def nifty_option_chain():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)

    data = response.json()
    records = data["records"]["data"]

    output = []

    for row in records:
        if "CE" in row and "PE" in row:
            output.append({
                "strike": row["strikePrice"],
                "ce_oi": row["CE"]["openInterest"],
                "ce_change_oi": row["CE"]["changeinOpenInterest"],
                "pe_oi": row["PE"]["openInterest"],
                "pe_change_oi": row["PE"]["changeinOpenInterest"]
            })

    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
