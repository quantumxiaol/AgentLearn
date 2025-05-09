# 运行结果
## FastAPI
运行`python ./task6/server.py`创建服务端

    INFO:     Started server process [24812]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     127.0.0.1:58228 - "GET /primes?limit=100 HTTP/1.1" 200 OK
    INFO:     127.0.0.1:58258 - "GET /primes?limit=100 HTTP/1.1" 200 OK
    INFO:     Shutting down
    INFO:     Waiting for application shutdown.
    INFO:     Application shutdown complete.
    INFO:     Finished server process [24812]


运行`curl "http://127.0.0.1:8000/primes?limit=100"`测试接收

StatusCode        : 200
StatusDescription : OK
Content           : [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 72
                    Content-Type: application/json
                    Date: Fri, 09 May 2025 08:28:54 GMT
                    Server: uvicorn

                    [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
Forms             : {}
Headers           : {[Content-Length, 72], [Content-Type, application/json], [Date, Fri, 09 May 2025 08:28:54 GMT], [Server, uvicorn]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 72

PS C:\work\AgentLearn> python ./task6/client.py

[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

## Flask
运行`python ./task6/flaskServer.py`创建服务端
 * Serving Flask app 'flaskServer'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 135-347-441
127.0.0.1 - - [09/May/2025 16:59:20] "GET / HTTP/1.1" 404 -
127.0.0.1 - - [09/May/2025 17:00:00] "GET /primes?limit=100 HTTP/1.1" 200 -

运行`curl "http://127.0.0.1:5000/primes?limit=100"`得到结果

StatusCode        : 200
StatusDescription : OK
Content           : [
                      2,
                      3,
                      5,
                      7,
                      11,
                      13,
                      17,
                      19,
                      23,
                      29,
                      31,
                      37,
                      41,
                      43,
                      47,
                      53,
                      59,
                      61,
                      67,
                      71,
                      73,
                      79,
                      83,
                      89,
                      97
                    ]

RawContent        : HTTP/1.1 200 OK
                    Connection: close
                    Content-Length: 149
                    Content-Type: application/json
                    Date: Fri, 09 May 2025 09:00:00 GMT
                    Server: Werkzeug/3.1.3 Python/3.11.0

                    [
                      2,
                      3,
                      5,
                      7,
                      11,
                      13,
                    ...
Forms             : {}
Headers           : {[Connection, close], [Content-Length, 149], [Content-Type, application/json], [Date, Fri, 09 May 2025 09:00:00 GMT]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 149