---
title: 'Python HTTP client'
summary: 'Python HTTP client examples'
url: 'tips/:slug'
date: '2025-06-19T20:15:25Z'
categories: ['tips']
tags: ['python','http','client']
draft: false
legacy_id: 5091
---

## References

- https://docs.python.org/3/library/http.client.html
- https://pypi.org/project/requests/
- [Python HTTP server]({{< relref "python-http-server" >}})

## http.client (stdlib)

> https://docs.python.org/3/library/http.client.html

Example:

```python
$ cat http-client.py
#!/usr/bin/env python3

from json import dumps as json_dumps, loads as json_loads
from http.client import HTTPConnection   # likewise for HTTPSConnection

if __name__ == "__main__":
    conn = HTTPConnection("127.0.0.1",4444)
    conn.request(
        "POST",
        "/post-file",
        body = json_dumps(dict(req="my-data")),
        headers = {
            "Content-Type": "application/json",
        },
    )
    resp = conn.getresponse()
    print("status =",resp.status,"reason =",resp.reason)
    for k,v in resp.getheaders():
        print(k,":",v)
    buf = resp.read()
    js = json_loads(buf.decode())
    print(json_dumps(js,sort_keys=True,indent=2))
```

Execution using example from [Python HTTP server](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6):

```
$ python3 http-client.py
status = 200 reason = OK
Server : BaseHTTP/0.6 Python/3.10.12
Date : Mon, 14 Oct 2024 15:15:45 GMT
Content-type : application/json
{
  "body": {
    "req": "my-data"
  },
  "headers": "Host: 127.0.0.1:4444|Accept-Encoding: identity|Content-Length: 18|Content-Type: application/json||",
  "len": 18,
  "path": "/post-file",
  "res": "ok"
}
```

Some more examples from https://docs.python.org/3/library/http.client.html (only one, there are more):

```python
import http.client
host = "docs.python.org"
conn = http.client.HTTPSConnection(host)
conn.request("GET", "/3/", headers={"Host": host})
response = conn.getresponse()
print(response.status, response.reason)
200 OK
```
```python
import http.client
conn = http.client.HTTPSConnection("localhost", 8080)
conn.set_tunnel("www.python.org")
conn.request("HEAD","/index.html")
```

## requests

> https://pypi.org/project/requests/

Install:

```
$ python -m pip install requests
```

Example:

```python
$ cat http-request.py
#!/usr/bin/env python3

from json import dumps as json_dumps
import requests

if __name__ == "__main__":
    #r = requests.get('http://127.0.0.1:4444',auth=('user','pass'))   # http or https
    r = requests.post(
        url = 'http://127.0.0.1:4444',
        json = dict(hello = "world, as usual"),  # alt: data
        auth=('user','pass'),
        headers={'X-demo':'hello'},
    )   # http or https
    print("code =",r.status_code)
    print("headers =",r.headers)
    print("encoding =",r.encoding)
    print(json_dumps(r.json(),indent=2,sort_keys=True))  # alt: r.text
```

Execution using example from [Python HTTP server](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6):

```
$ python3 http-request.py
code = 200
headers = {'Server': 'BaseHTTP/0.6 Python/3.10.12', 'Date': 'Mon, 14 Oct 2024 15:34:45 GMT', 'Content-type': 'application/json'}
encoding = utf-8
{
  "body": {
    "hello": "world, as usual"
  },
  "headers": "Host: 127.0.0.1:4444|User-Agent: python-requests/2.25.1|Accept-Encoding: gzip, deflate|Accept: */*|Connection: keep-alive|X-demo: hello|Content-Length: 28|Content-Type: application/json|Authorization: Basic dXNlcjpwYXNz||",
  "len": 28,
  "path": "/",
  "res": "ok"
}
```
