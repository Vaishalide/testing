from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Playwright Flask API is running!"

@app.route("/scrape")
def scrape():
    url = request.args.get("https://rarestudy.site/media/HRQgh-s1TsFIVhW9rLkmCY-PkTLxPhvZ9j19wtUZ08lk2cL_6mvqcWauYNGM7ESWjbXJY9yUaGq1tP09uSy911VWuvWwlL9Vm8hgQeLk69WQ1DBeeaOgSLZaN_hitfYmqZAbsZ27m508J2fLUu_KALo7XNYjqtYeuFq_rPSUOoTy2a8yIZ8ZQi4VrYIoGhJ49ju10nREiXresVDg5GbvRF7QZx7YpSMoQcXzKu1R44KMr7S8EjkhTVxxJyK4672of3syfp-4iSJ3F2l6pZ7b5X3eqLDyXERljh79-DWFiTsjhJBk9ffuWADNJqXupfTmf6ZrEF4pgheD2O9KGUtWTtOZnoYr5U4V3z1NHqCSq9dLizF5fVaYGu_06RayJkWu")
    if not url:
        return jsonify({"error": "Missing ?url param"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
        return jsonify({"html": html[:1000] + "..."}), 200  # Return first 1000 chars
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
