import uvicorn
from task11_mcpServer import app

if __name__ == "__main__":
    uvicorn.run("task11_mcpServer:app", host="0.0.0.0", port=7002, reload=True)
    for route in app.routes:
        print(route.path)