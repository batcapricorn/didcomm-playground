from flask import Flask, request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/topic/<path:subpath>', methods=['POST'])
def handle_all_requests(subpath):
    data = request.json
    logging.info(f"Webhook received POST request for subpath: {subpath}, data: {data}")
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
