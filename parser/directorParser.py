import json
import urllib
import urllib2
from pyquery import PyQuery as pq

types = ['sii', 'otc', 'rotc', 'pub']

companys = {}

def outputResult(outfile):
    ofd = open(outfile, 'w')
    for k, comp in companys.iteritems():
        ofd.write("%s,\n" % json.dumps(comp, encoding='unicode'))
    ofd.close()

def parseDirectors(target):
    url = "http://mops.twse.com.tw/mops/web/ajax_t93sb06"
    values = {  'encodeURIComponent': '1',
                'step': '1',
                'firstin': '1',
                'off':'1',
                'TYPEK':target }

    req_data = urllib.urlencode(values)
    req = urllib2.Request(url, req_data)
    res = urllib2.urlopen(req)
    raw_doc = res.read()
    #print raw_doc
    encoding = 'utf-8'
    if res.headers.has_key('content-encoding'): 
        encoding = res.headers['content-encoding']

    doc = pq(raw_doc.decode(encoding))
    print "encoding = %s" % doc.encoding
    table = pq(doc('table').filter('.hasBorder'))
    for row in table.items('tr'):
        #print row
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
                    companys[i]["directors"] = []
            elif c==2:  # company name
                companys[i]["name"] = outstr
            elif c==3:
                companys[i]["directors"].append(outstr)
            elif c==4:
                companys[i]["type"] = outstr
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
