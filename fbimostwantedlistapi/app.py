import requests
import json
from flask import Flask, render_template, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    current_page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '', type=str).strip().lower()

    params = {'page': current_page}
    if name:
        params['title'] = name

    response = requests.get('https://api.fbi.gov/wanted/v1/list', params=params)
    data = response.json()

    items = data.get('items', [])
    total = data.get('total', 0)
    current_page = data.get('page', current_page)

    return render_template('index.html', items=items, total=total, page=current_page, name=name)

@app.route('/wanted/<uid>')
def wanted_detail(uid):
    try:
        response = requests.get(f'https://api.fbi.gov/@wanted-person/{uid}')
        response.raise_for_status() 
        person = response.json()

        return render_template('fbi.html', person=person)

    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
        abort(404, description="Person not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        abort(500, description="An unexpected error occurred.")

if __name__ == '__main__':
    app.run(debug=True)