import dev_key
import json
import httplib

baseurl = "www.googleapis.com"
bodyurl = "/urlshortener/v1/url?key=" + dev_key.googlekey
headers = {"Content-Type": "application/json"}

def shorten(url):
    toreturn = "Error"
    msg = json.dumps({"longUrl": url})
    conn = httplib.HTTPSConnection(baseurl)
    conn.request("POST", bodyurl, msg, headers)
    response = conn.getresponse()
    if response.status == 200 and response.reason == "OK":
        data = response.read()
        result = json.loads(data)
        toreturn = result['id']
    conn.close()
    return toreturn
