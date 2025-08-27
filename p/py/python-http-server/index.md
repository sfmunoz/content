# Python HTTP server

Python HTTP server examples

- [References](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#references)
- [Example](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#example)
  - [Execution](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#execution)
  - [Example: GET](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#example-get)
  - [Example: POST](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#example-post)
- [Alternatives](https://gist.github.com/sfmunoz/47b9e237776f491f71dcf8726b780ee6#alternatives)

## References

- https://docs.python.org/3/library/http.server.html
- [Python HTTP client](https://gist.github.com/sfmunoz/fcb08d624b27128111e1961f5b143051)

## Example

```python
$ cat http-server.py
#!/usr/bin/env python3

from os import getenv
from json import dumps as json_dumps, loads as json_loads
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus

HTTP_PORT = 4444

class MyHTTPServer(HTTPServer):
    def server_bind(self):
        print("MyHTTPServer.server_bind()",self.server_address)
        return HTTPServer.server_bind(self)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self,request,client_address,server):
        print("MyHTTPRequestHandler.__init__()",request,client_address,server)
        BaseHTTPRequestHandler.__init__(self,request,client_address,server)

    def __send_reply(self,http_code,js):
        js['headers'] = str(self.headers).replace("\n","|")
        js['path'] = self.path
        buf = json_dumps(js,sort_keys=True,indent=2) + "\n"
        self.send_response(http_code)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(buf.encode().decode('unicode-escape').encode('UTF-8'))

    def do_GET(self):
        self.__send_reply(HTTPStatus.METHOD_NOT_ALLOWED,dict(error="method not allowed"))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body_buf = self.rfile.read(length)
        body_js = json_loads(body_buf)
        js = dict(res="ok",len=length,body=body_js)
        self.__send_reply(HTTPStatus.OK,js)

def http_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', HTTP_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()  # lo para el handler con 'shutdown()'

if __name__ == "__main__":
    if getenv("SIMPLE") == "1":
        http_server()
    else:
        http_server(MyHTTPServer,MyHTTPRequestHandler)
```

### Execution

```
$ python3 http-server.py
```
### Example: GET
```
$ curl -v http://127.0.0.1:4444/get-file.txt
*   Trying 127.0.0.1:4444...
* Connected to 127.0.0.1 (127.0.0.1) port 4444 (#0)
> GET /get-file.txt HTTP/1.1
> Host: 127.0.0.1:4444
> User-Agent: curl/7.81.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 405 Method Not Allowed
< Server: BaseHTTP/0.6 Python/3.10.12
< Date: Mon, 14 Oct 2024 15:05:25 GMT
< Content-type: application/json
<
{
  "error": "method not allowed",
  "headers": "Host: 127.0.0.1:4444|User-Agent: curl/7.81.0|Accept: */*||",
  "path": "/get-file.txt"
}
* Closing connection 0
```
### Example: POST
```
$ curl -v -d '{"req":"request"}' -H Content-Type:application/json http://127.0.0.1:4444/post-file.txt
*   Trying 127.0.0.1:4444...
* Connected to 127.0.0.1 (127.0.0.1) port 4444 (#0)
> POST /post-file.txt HTTP/1.1
> Host: 127.0.0.1:4444
> User-Agent: curl/7.81.0
> Accept: */*
> Content-Type:application/json
> Content-Length: 17
>
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.10.12
< Date: Mon, 14 Oct 2024 15:05:47 GMT
< Content-type: application/json
<
{
  "body": {
    "req": "request"
  },
  "headers": "Host: 127.0.0.1:4444|User-Agent: curl/7.81.0|Accept: */*|Content-Type: application/json|Content-Length: 17||",
  "len": 17,
  "path": "/post-file.txt",
  "res": "ok"
}
* Closing connection 0
```

## Alternatives

From [https://docs.python.org/3/library/http.server.html](https://docs.python.org/3/library/http.server.html):

```python
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
```
```
python -m http.server
```
```
python -m http.server 9000
```
```
python -m http.server --bind 127.0.0.1
```
```
python -m http.server --directory /tmp/
```
```
python -m http.server --protocol HTTP/1.1
```

---

#tip 5090