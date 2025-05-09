# curl "http://127.0.0.1:5000/primes?limit=100"

from flask import Flask, request, jsonify
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.testtool import getPrimeinNumN

app = Flask(__name__)
# 在网页上展示Hello, World!
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/primes', methods=['GET'])
def primes():
    try:
        # 获取查询参数 'limit'
        limit = int(request.args.get('limit'))
        if limit < 2:
            return jsonify({"error": "Limit must be at least 2."}), 400
        
        # 调用外部模块中的函数获取质数列表
        primes = getPrimeinNumN(limit)
        
        # 返回 JSON 响应
        return jsonify(primes), 200
    except ValueError:
        return jsonify({"error": "Invalid input. Limit must be an integer."}), 400
    
if __name__ == '__main__':
    app.run(debug=True)