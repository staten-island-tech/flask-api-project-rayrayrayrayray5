import requests
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page':current_page})
    data = json.loads(response.content)
    total = data['total']
    current_page = data['page']
    title = data['items'][0]['title']
    return render_template('index.html', total=total, page=current_page, title=title)

if __name__ == '__main__':
    app.run(debug=True)