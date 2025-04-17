from http.server import HTTPServer, BaseHTTPRequestHandler
import smtplib
from email.mime.text import MIMEText
from urllib.parse import parse_qs
import json
import os
import mimetypes

class EmailHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Serve static files
        path = self.path
        if path == '/':
            path = '/index.html'
        
        try:
            # Remove query parameters if any
            if '?' in path:
                path = path.split('?')[0]
                
            file_path = os.path.join(os.getcwd(), path.lstrip('/'))
            
            # Check if file exists
            if os.path.isfile(file_path):
                # Determine content type
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                # Send headers
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                
                # Send file content
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                # File not found
                print(f"File not found: {file_path}")
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - File Not Found')
        except Exception as e:
            print(f"Error serving file: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'500 - Server Error: {str(e)}'.encode())

    def do_POST(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Get form data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form_data = parse_qs(post_data.decode('utf-8'))
        
        name = form_data.get('name', [''])[0]
        email = form_data.get('email', [''])[0]
        message = form_data.get('message', [''])[0]
        
        try:
            # Email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "netfolio.rk@gmail.com"
            app_password = "qbek qvtj zhca jfvy"
            receiver_email = "Raghunath.Kunigiri@slu.edu"
            
            # Create message
            email_content = f"""
            New Contact Form Submission
            
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            """
            
            msg = MIMEText(email_content)
            msg['Subject'] = "Your Netfolio Contact Form Submission"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
            
            self.wfile.write(json.dumps({'status': 'success'}).encode())
        except Exception as e:
            print(f"Error: {str(e)}")
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, EmailHandler)
    print('Server running on port 8000...')
    print('Open your browser and navigate to http://localhost:8000')
    print(f'Serving files from: {os.getcwd()}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()