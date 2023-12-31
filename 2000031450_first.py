import requests
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except (requests.RequestException, ValueError):
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    numbers = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]

        for future in futures:
            try:
                result = future.result()
                numbers.extend(result)
            except requests.Timeout:
                pass

    numbers = sorted(list(set(numbers)))

    return jsonify({"numbers": numbers})

if __name__ == '__main__':
    app.run(port=8008)
