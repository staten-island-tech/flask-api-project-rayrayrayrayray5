import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    current_page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '', type=str)
    crime = request.args.get('crime', '', type = str)

    params = {'page': current_page}
    if name:
        params['title'] = name
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params = params)
    data = response.json()

    items = data.get('items', [])
    total = data.get('total', 0)
    current_page = data.get('page', current_page)

    if crime:
         items = [item for item in items if crime.lower() in str(item.get('description', '')).lower()]

    return render_template('index.html', items=items, total=total, page=current_page, name = name, crime = crime)
if __name__ == '__main__':
    app.run(debug=True)