from flask import Flask, render_template, jsonify, request, json, redirect
from db import Body, Request, Document, RequestTag, get_session, serialise_reqs
from sqlalchemy import and_, or_

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("/front/")

@app.route('/requests')
def requests():
    db = get_session()
    reqs = db.query(Request).all()[0:20]
    db.close()
    return render_template("requests.html", reqs=reqs)

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
    db.close()
    return render_template("request.html", req=req, doc = doc, body=body,
                           tags=tags)

@app.route('/request/search/<query>')
def search(query):
    db = get_session()
    query = '%{0}%'.format(query)
    reqs = db.query(Request).filter(Request.title.ilike(query)).all()
    db.close()
    return render_template("requests.html", reqs=reqs)

@app.route('/api/all')
def api_all():
    db = get_session()
    reqs = db.query(Request).all()
    db.close()
    return jsonify({'requests': serialise_reqs(reqs)})

@app.route('/api/search')
def api_search():
    db = get_session()
    sterms = request.args.get('q')
    if sterms:
        sterms = sterms.split(',')
    else:
        return jsonify({'error': "Search term is required."})
    if len(sterms) == 0:
        return jsonify({"error": "No search terms."})
    qterms = [or_(Request.title.ilike("%{0}%".format(t)),
                  RequestTag.tag.ilike("%{0}%".format(t))) for t in sterms]
    res = db.query(Request).join(RequestTag).filter(and_(*qterms))
    locs = request.args.get('l')
    if locs:
        locs = locs.split(',')
        lterms = [Body.name.ilike("%{0}%".format(l)) for l in locs]
        res  = res.join(Body).filter(or_(*lterms))
    res = res.all()
    db.close()
    return jsonify({'requests': serialise_reqs(res)})
    

@app.route('/api/documents/<int:req_id>')
def api_document(req_id):
    db = get_session()
    docs = db.query(Document).filter(Document.request == req_id).all()
    docs = [{'id': d.id, 'url': d.url, 'req_id': d.request, 'text':d.text} for d in docs]
    db.close()
    return jsonify({'documents': docs})
