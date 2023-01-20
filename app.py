from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime
import yaml
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app)

def crawl_website(url):
    return requests.get(url).text

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    # get all tags
    tags = soup.find_all()

    class_list = set()
    for tag in tags:
        # find all element of tag
        for i in soup.find_all( tag ):
            if i.has_attr( "class" ):
                if len( i['class'] ) != 0:
                    class_list.add(" ".join( i['class']))
    print(class_list)


API_V1 = '/api/1.0'

@app.route(API_V1 + '/ping', methods=['GET'])
def ping():
    return "pong"

@app.route(API_V1 + '/info', methods=['GET'])
def info():
    return jsonify({
        'version': API_V1,
        'project': 'aicollaborationservices',
        'service': 'website-crawler',
        'language': 'python',
        'type': 'api',
        'date': str(datetime.datetime.now()),
    })

@app.route(API_V1 + '/crawl', methods=['POST', 'OPTIONS'])
@cross_origin()
def crawl():
    data = request.json

    # crawl the website and extract the content
    html = crawl_website(data['url'])

    # extract the content from the html
    content = extract_content(html)



    response = jsonify({ 'content': content })

    return response

@app.route(API_V1 + '/definition', methods=['GET'])
def definition():
    with open("./openapi.yml", 'r') as stream:
        try:
            return jsonify(yaml.safe_load(stream))
        except yaml.YAMLError as exception:
            return jsonify(exception)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)