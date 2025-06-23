from seleniumbase import Driver
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ SeleniumBase Cloudflare Bypass is running"

@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url parameter"}), 400

    try:
        driver = Driver(uc=True, headless=True)
        driver.uc_open_with_reconnect(url, max_retries=4)
        driver.uc_gui_click_captcha()  # optional
        driver.wait(5)  # wait to finish loading
        html = driver.page_source
        driver.quit()
        return jsonify({"html": html[:2000]})  # return preview
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
