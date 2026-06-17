from flask import Flask, request, Response
import cloudscraper, os

UPSTREAM = os.environ['TARGET_URL']
scraper = cloudscraper.create_scraper()

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def proxy(path):
    url = f"{UPSTREAM}/{path}"
    headers = {k:v for k,v in request.headers if k.lower() != 'host'}
    resp = scraper.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        timeout=30
    )
    excluded_headers = ['content-encoding','content-length','transfer-encoding','connection']
    resp_headers = [(k,v) for k,v in resp.raw.headers.items() if k.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, resp_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
