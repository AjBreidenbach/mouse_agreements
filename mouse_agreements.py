from flask import Flask
from flask import request, Response
from document import Document

import json

app = Flask(__name__)

import sys
@app.route('/convert', methods=['POST'])
def convert():
    print(request.data, file=sys.stderr)
    return Response(status=200, response=(Document(request.data).output))
