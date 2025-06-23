from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Render + Playwright is working!"

@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url="}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
        return jsonify({"html": html[:1000] + "..."}), 200  # show preview
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
