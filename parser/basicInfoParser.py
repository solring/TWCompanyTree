import json
import urllib
import urllib2
from pyquery import PyQuery as pq

types = ['sii', 'otc', 'rotc', 'pub']

companys = {}

def outputResult(outfile):
    ofd = open(outfile, 'w')
	c = 0
	ofd.write("[")
    for k, comp in companys.iteritems():
		ofd.write(", \n") if c == 0
        ofd.write("%s" % json.dumps(comp, ensure_ascii=False, encoding='utf-8'))
		c += 1
	ofd.write("]")
    ofd.close()

def parseDirectors(market_type):

    # POST request and get response
    url = "http://mops.twse.com.tw/mops/web/ajax_quickpgm"
    otcForm = {
		"encodeURIComponent" : "1",
		"firstin" : "true",
		"step" : "4",
		"checkbtn" : "1"},
		"queryName" : "co_id",
		"TYPEK2" : market_type,
		"code1" : "",
		"keyword4" : ""}

    req_data = urllib.urlencode(values)
    req = urllib2.Request(url, req_data)
    res = urllib2.urlopen(req)
    raw_doc = res.read()
    #print raw_doc
    encoding = 'utf-8'
    if res.headers.has_key('content-encoding'): 
        encoding = res.headers['content-encoding']

    doc = pq(raw_doc.decode(encoding)) # get the DOM
    print "encoding = %s" % doc.encoding
    
    # customize for each website
    table = pq(doc('table').filter('#zoom')) # get the table with class .hasBorder
    for row in table.items('tr'):
        c=1
        i=""
        for col in row.items('td'):
            outstr = col.text().encode(encoding)
            print 'outstr = ', outstr
            if c==1:    # id
                if outstr == "": pass
                i=outstr
                if outstr not in companys:
                    companys[i] = {}
                    companys[i]["id"] = i
            elif c==2:  # company name
                companys[i]["abbr1"] = outstr
            elif c==3:
                companys[i]["abbr2"] = outstr
            elif c==4:
                companys[i]["name"] = outstr
            elif c==5:
                companys[i]["market"] = outstr
            elif c==6:
                companys[i]["industry"] = outstr
            elif c==7:
                companys[i]["note"] = outstr
            else:
                # do nothing
                print c
            c += 1
        print '-----------'

if __name__ == '__main__':
    #parseDirectors('sii')
    for t in types:
       parseDirectors(t)
       outputResult("directorOver10_%s.json" % t)
