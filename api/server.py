import http.server
import json
import base64
from urllib.parse import urlparse

# Load transactions from a JSON file
with open('./data/transactions.json', 'r') as f:
    transactions = json.load(f)

USERNAME = "admin"
PASSWORD = "1234"
HOST = "localhost"
PORT = 8080

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _authenticate(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            self._send_unauthorized()
            return False

        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode()
        username, password = decoded_credentials.split(':')

        if username == USERNAME and password == PASSWORD:
            return True
        else:
            self._send_unauthorized()
            return False

    def _send_unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Access to server"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())

    def do_GET(self):
        if not self._authenticate():
            return

        if self.path == '/transactions':
            # Return all transactions
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(transactions).encode())
        elif self.path.startswith('/transactions/'):
            # Return a specific transaction by ID
            transaction_id = self.path.split('/')[-1]
            transaction = next((t for t in transactions if t['transaction_id'] == transaction_id), None)
            if transaction:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(transaction).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_POST(self):
        if not self._authenticate():
            return

        if self.path == '/transactions':
            # Add a new transaction
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_transaction = json.loads(post_data.decode('utf-8'))
            transactions.append(new_transaction)

            # Save the updated transactions to the file
            with open('../data/transactions.json', 'w') as f:
                json.dump(transactions, f, indent=4)

            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_transaction).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_PUT(self):
        if not self._authenticate():
            return

        if self.path.startswith('/transactions/'):
            # Update an existing transaction
            transaction_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_transaction = json.loads(put_data.decode('utf-8'))

            for i, transaction in enumerate(transactions):
                if transaction['transaction_id'] == transaction_id:
                    transactions[i] = updated_transaction

                    # Save the updated transactions to the file
                    with open('../data/transactions.json', 'w') as f:
                        json.dump(transactions, f, indent=4)

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(updated_transaction).encode())
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, host=HOST, port=PORT):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on {host}:{port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
