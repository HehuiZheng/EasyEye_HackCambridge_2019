import time, urllib, urllib.request
def upload_data(data):
    s = time.clock()
    url = "https://zhilingmail.pythonanywhere.com/api/upload_data"
    data = json.dumps(data)
    data = data.encode("utf-8")
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    print(resp.read())
    print(time.clock()-s)
import json

with open('data.txt') as f:
    lines = f.readlines()
    for line in lines:
        upload_data(json.loads(line))

