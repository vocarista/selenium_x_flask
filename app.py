from flask import Flask, jsonify, render_template
import subprocess
import os
from selenium_scripts.get_trends import get_trending_topics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        data = get_trending_topics()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

