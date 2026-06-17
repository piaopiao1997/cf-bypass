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

    # 复制所有请求头（去掉Host避免冲突）
    headers = {}
    for k, v in request.headers:
        if k.lower() == 'host':
            continue
        headers[k] = v

    try:
        # 直接获得解压后的文本（cloudscraper 自动处理 gzip）
        resp = scraper.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            timeout=30
        )
        # 返回纯文本，状态码，以及干净的头
        return Response(
            resp.text,              # 已解压的字符串
            status=resp.status_code,
            headers={'Content-Type': resp.headers.get('Content-Type', 'application/json')}
        )
    except Exception as e:
        return Response(f"Proxy error: {e}", status=502)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
