from flask import Flask, render_template, jsonify, request, json, redirect
from db import Body, Request, Document, RequestTag, get_session
from sqlalchemy import and_

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
def request_details(req_id):
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

@app.route('/api/all')
def api_all():
    db = get_session()
    reqs = db.query(Request).all()
    return jsonify({'requests': [r.get_public() for r in reqs]})

@app.route('/api/search')
def api_search():
    db = get_session()
    sterms = request.args.get('q')
    if sterms:
        sterms = sterms.split(',')
    else:
        return jsonify({'error': "Search term is required."})
    locs = request.args.get('l')
    if locs:
        locs = locs.split(',')
    if len(sterms) == 0:
        return jsonify({"error": "No search terms."})
    qterms = [Request.title.ilike("%{0}%".format(t)) for t in sterms]
    res = db.query(Request).filter(and_(*qterms))
    return jsonify({'requests': [r.get_public() for r in res.all()]})
    
