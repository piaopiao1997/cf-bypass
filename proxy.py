from flask import Flask, request, Response
import cloudscraper
import os

UPSTREAM = 'https://muyuan.do'

scraper = cloudscraper.create_scraper()
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def proxy(path):
    url = f"{UPSTREAM}/{path}"

    # 转发所有请求头，但移除 Host（避免冲突）
    headers = {}
    for k, v in request.headers:
        if k.lower() == 'host':
            continue
        headers[k] = v

    # 获取原始请求体
    data = request.get_data()

    try:
        resp = scraper.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            timeout=30
        )
    except Exception as e:
        return Response(f"Upstream error: {e}", status=502)

    # 构造返回的响应头
    excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    resp_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded]

    return Response(resp.content, resp.status_code, resp_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
