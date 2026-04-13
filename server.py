import http.server, json, re, os

PORT = 8765
BASE = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=BASE, **k)

    def do_POST(self):
        if self.path == '/save-layout':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            page = body.get('page', '')
            pills = body.get('pills', [])
            if not re.match(r'^[a-z]+$', page):
                self.send_response(400)
                self.end_headers()
                return
            fp = os.path.join(BASE, page, 'index.html')
            if not os.path.exists(fp):
                self.send_response(404)
                self.end_headers()
                return
            with open(fp, 'r', encoding='utf-8') as f:
                html = f.read()
            count = 0
            for pill in pills:
                name = pill['name']
                new_style = 'left:{}px;top:{}px;width:{}px;height:{}px'.format(
                    pill['left'], pill['top'], pill['width'], pill['height'])
                # Strip emoji - keep only ASCII text
                ascii_name = re.sub(r'[^\x20-\x7E]', '', name).strip()
                if len(ascii_name) < 3:
                    continue
                # Replace & with &amp; for HTML matching
                html_name = ascii_name.replace('&', '&amp;')
                search = re.escape(html_name[:20])
                pattern = r'(<div class="pill [^"]*" style=")([^"]+)(">\s*<div class="pill-header">[^<]*?' + search + r')'
                m = re.search(pattern, html, re.DOTALL)
                if m:
                    html = html[:m.start(2)] + new_style + html[m.end(2):]
                    count += 1
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'saved': count}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    print('Server on http://localhost:{}'.format(PORT))
    http.server.HTTPServer(('', PORT), Handler).serve_forever()
