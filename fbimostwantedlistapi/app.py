import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    current_page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    params = {'page': current_page}
    if search:
        params['title'] = search
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params = params)
    data = response.json()

    items = data.get('items', [])
    total = data.get('total', 0)
    current_page = data.get('page', current_page)

    return render_template('index.html', items=items, total=total, page=current_page, search=search)
if __name__ == '__main__':
    app.run(debug=True)