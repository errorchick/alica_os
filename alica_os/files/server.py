import http.server
import socketserver
import urllib.parse
import subprocess
import os
import json

PORT = 8080

ROOT_DIR = "/" 

# Защищенные папки (чтобы ты не убил систему)
PROTECTED = ["/etc", "/bin", "/sbin", "/lib", "/usr", "/boot", "/data"]

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == '/api/ls':
            req_path = query.get('path', ['/'])[0]
            full_path = os.path.join(ROOT_DIR, req_path.lstrip('/'))
            files = []
            try:
                for name in os.listdir(full_path):
                    if name.startswith('.'): continue
                    fp = os.path.join(full_path, name)
                    files.append({"name": name, "type": "dir" if os.path.isdir(fp) else "file"})
            except:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())

        elif path == '/api/create':
            req_path = query.get('path', [''])[0]
            typ = query.get('type', ['file'])[0]
            full_path = os.path.join(ROOT_DIR, req_path.lstrip('/'))
            # Защита
            if any(full_path.startswith(p) for p in PROTECTED):
                self.send_response(403)
                self.end_headers()
                return
            try:
                if typ == 'dir':
                    os.makedirs(full_path, exist_ok=True)
                else:
                    open(full_path, 'a').close()
            except:
                pass
            self.send_response(200)
            self.end_headers()

        elif path == '/api/delete':
            req_path = query.get('path', [''])[0]
            full_path = os.path.join(ROOT_DIR, req_path.lstrip('/'))

            if any(full_path.startswith(p) for p in PROTECTED):
                self.send_response(403)
                self.end_headers()
                return
            try:
                subprocess.run(['rm', '-rf', full_path])
            except:
                pass
            self.send_response(200)
            self.end_headers()

        elif path == '/api/read':
            req_path = query.get('path', [''])[0]
            full_path = os.path.join(ROOT_DIR, req_path.lstrip('/'))
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
            except:
                content = "File not found or access denied"
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode())

        elif path == '/api/write':
            req_path = query.get('path', [''])[0]
            content = query.get('content', [''])[0]
            full_path = os.path.join(ROOT_DIR, req_path.lstrip('/'))
            # Защита
            if any(full_path.startswith(p) for p in PROTECTED):
                self.send_response(403)
                self.end_headers()
                return
            try:
                with open(full_path, 'w') as f:
                    f.write(content)
            except:
                pass
            self.send_response(200)
            self.end_headers()

        elif path == '/api/exec':
            cmd = query.get('cmd', [''])[0]
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10).decode('utf-8', errors='replace')
            except subprocess.CalledProcessError as e:
                output = e.output.decode('utf-8', errors='replace')
            except Exception as e:
                output = str(e)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(output.encode())

        else:
            try:
                with open('/data/myos/www/index.html', 'r') as f:
                    html = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode())
            except:
                self.send_response(404)
                self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"error OS Server run port {PORT} (Full Disk Access)")
    httpd.serve_forever()