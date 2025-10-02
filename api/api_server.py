from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from base64 import b64decode


# ensure project root is on sys.path so local package `dsa` can be imported
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dsa.parse_sms import parse_sms_xml

HOST = 'localhost'
PORT = 8000

transactions = parse_sms_xml('./modified_sms_v2.xml')
transactions_dict = {t['id']: t for t in transactions}  # dictionary for fast lookup

USERNAME = "admin"
PASSWORD = "password"

def check_auth(header):
    if not header:
        return False
    auth_type, credentials = header.split()
    if auth_type != 'Basic':
        return False
    decoded = b64decode(credentials).decode()
    user, pwd = decoded.split(':')
    return user == USERNAME and pwd == PASSWORD

class RequestHandler(BaseHTTPRequestHandler):
    def _send_headers(self, code=200, content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="API"')
        self.end_headers()
        self.wfile.write(b'Unauthorized')

    def do_GET(self):
        if not check_auth(self.headers.get('Authorization')):
            return self._unauthorized()

        path_parts = self.path.strip('/').split('/')
        if self.path.startswith('/transactions'):
            if len(path_parts) == 1:  # GET /transactions
                self._send_headers()
                self.wfile.write(json.dumps(list(transactions_dict.values())).encode())
            elif len(path_parts) == 2:  # GET /transactions/{id}
                tid = path_parts[1]
                transaction = transactions_dict.get(tid)
                if transaction:
                    self._send_headers()
                    self.wfile.write(json.dumps(transaction).encode())
                else:
                    self._send_headers(404)
                    self.wfile.write(json.dumps({'error': 'Not found'}).encode())

        # if self.path.startswith('/'): #and self.path != '/transactions':
        #     self._send_headers(200, 'text/html')
        #     self.wfile.write(b"<html><body><h1>Transaction API</h1><p>Use /transactions endpoint.</p></body></html>")

    def do_POST(self):
        if not check_auth(self.headers.get('Authorization')):
            return self._unauthorized()

        if self.path == '/transactions':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            new_transaction = json.loads(post_data)
            transactions_dict[new_transaction['id']] = new_transaction
            self._send_headers(201)
            self.wfile.write(json.dumps(new_transaction).encode())

    def do_PUT(self):
        if not check_auth(self.headers.get('Authorization')):
            return self._unauthorized()

        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            tid = path_parts[1]
            if tid in transactions_dict:
                content_length = int(self.headers.get('Content-Length', 0))
                put_data = self.rfile.read(content_length)
                updated_transaction = json.loads(put_data)
                transactions_dict[tid] = updated_transaction
                self._send_headers()
                self.wfile.write(json.dumps(updated_transaction).encode())
            else:
                self._send_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_DELETE(self):
        if not check_auth(self.headers.get('Authorization')):
            return self._unauthorized()

        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            tid = path_parts[1]
            if tid in transactions_dict:
                deleted = transactions_dict.pop(tid)
                self._send_headers()
                self.wfile.write(json.dumps(deleted).encode())
            else:
                self._send_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())

if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f'Server running at http://{HOST}:{PORT}')
    server.serve_forever()
