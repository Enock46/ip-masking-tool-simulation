from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mask_ip', methods=['POST'])
def mask_ip():
    target_url = request.form.get('target_url')
    proxy_ip = request.form.get('proxy_ip')
    proxy_port = request.form.get('proxy_port')

    if not target_url or not proxy_ip or not proxy_port:
        return render_template('result.html', error="All fields are required!")

    proxies = {
        "http": f"http://{proxy_ip}:{proxy_port}",
        "https": f"http://{proxy_ip}:{proxy_port}",
    }

    try:
        response = requests.get(target_url, proxies=proxies, timeout=5)
        result = {
            "status_code": response.status_code,
            "headers": response.headers,
            "success": True,
        }
    except requests.exceptions.RequestException as e:
        result = {"error": str(e), "success": False}

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
