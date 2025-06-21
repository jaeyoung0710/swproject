from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200) 
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = '<html><body><h1>It is my HTTP server</h1></body></html>'
        self.wfile.write(response.encode('utf-8'))


def run_server():
    host = ''
    port = 8080
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f'Serving on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
