from pymongo import MongoClient
from flask import Flask, request, redirect, url_for, render_template
import json

host = "140.112.28.103"
port = 11111
user = "solring"
pwd = "460852"
dbname = "TWcompany"
url = "mongodb://%s:%s@%s:%d" % (user, pwd, host, port)

db = None
col = None

app = Flask(__name__)

def to_node(d):
    return {"id": d["id"],
            "name": d["name"],
            "market": d["market"] }

@app.route("/")
def mainpage():
    return render_template('index.html')

@app.route("/company/search", methods=['POST'])
def search_byname():
    print "QQ"
    query = request.form['query']
    print "company/search/"+query
    data = col.find_one({ "id" : query})
    if data:
        return redirect(url_for("/company/%s" % data["id"]))
    else:
        return render("index.html")

@app.route("/company/<int:cid>.json")
def getJsonById(cid):
    if col == None:
        return "database collection unavailable."
    
    #res = "---- company %d ----<br>" % cid
    nodes = []
    links = []

    data = col.find({ "id" : str(cid) })
    if data:
        center1 = data[0]  # choose the first result
        data2 = db["directorOver10"].find({"id" : str(cid)}) 
        center2 = data2[0]
        
        c = to_node(center1)
        nodes.append(c)        
        for n in center2["directors"]:
            fake = {"id": "", "name": n, "market": "unknown"}
            links.append({"src": c, "dst": fake})
            nodes.append(fake)
    
    result = json.dumps({"center": c, "nodes": nodes, "links": links})
    return result

@app.route("/company/<int:cid>")
def show_company(cid):
    

    #if data:
    #    for k, v in data.items():
    #        res += "%s : %s<br>" %(k, v)
    #else:
    #    res += "Cannot find company with id %d" % cid
    return render_template('graph.html', cid=cid)
    


if __name__ == "__main__":
    
    dbclient = MongoClient(host, port)
    db = dbclient[dbname]
    db.authenticate(user, pwd)
    col = db["basicInfo"]
    print "========== data base initialized =========="
    #cols = db.collection_names(include_system_collections=False)

    app.debug = True
    app.run()

