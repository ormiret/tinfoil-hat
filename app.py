from flask import Flask, render_template, jsonify, request, json, redirect
from db import Body, Request, Document, RequestTag, get_session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/requests')
def requests():
    db = get_session()
    reqs = db.query(Request).all()
    return render_template("requests.html", reqs=reqs[0:20])

@app.route('/request/<req_id>')
def request(req_id):
    db = get_session()
    req = db.query(Request).get(req_id)
    docs = db.query(Document).filter(Document.request == req.id).all()
    if len(docs) > 0:
        doc = docs[0]
    else:
        doc = False
    body = db.query(Body).get(req.body)
    tags = [t.tag for t in db.query(RequestTag).filter(RequestTag.request == req.id)]
    return render_template("request.html", req=req, doc = doc, body=body,
                           tags=tags)

@app.route('/request/search/<query>')
def search(query):
    db = get_session()
    query = '%{0}%'.format(query)
    reqs = db.query(Request).filter(Request.title.ilike(query))
    return render_template("requests.html", reqs=reqs)
