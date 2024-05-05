from http.server import BaseHTTPRequestHandler, HTTPServer
import pyodbc
from DigitalSignature import DigitalSignature
import base64
import os
import urllib.parse
import cgi

FRONTEND_DIRECTORY = 'C:/Users/Admin/OneDrive/Рабочий стол/Course Work/Front'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path

        if path == '/':
            file_path = os.path.join(FRONTEND_DIRECTORY, 'index.html')
        else:
            file_path = os.path.join(FRONTEND_DIRECTORY, path[1:])
    
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                if file_path.endswith('.html'):
                    mime_type = 'text/html'
                elif file_path.endswith('.css'):
                    mime_type = 'text/css'
                elif file_path.endswith('.js'):
                    mime_type = 'application/javascript'
                else:
                    mime_type = 'text/plain'  
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File not found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        username =post_data.split('\n')[3]
        signature_data = post_data.split('\n')[7]

        ds = DigitalSignature()
        ds.generate_rsa_key_pair(2048)
        signature = ds.sign_data(signature_data)

        if self.save_to_database(username, signature):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(base64.b64encode(signature))
        else:
            self.send_error(500, 'Failed to save data to database')

    def save_to_database(self, username, signature):
        try:
            server = 'GWTN156-5\SQLEXPRESS'  
            database = 'DigitalSignature' 
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            db = pyodbc.connect(conn_str)
            cursor = db.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='UserData' and xtype='U')
                CREATE TABLE UserData (
                    UserID INT IDENTITY PRIMARY KEY,
                    Username VARCHAR(255),
                    Signature VARCHAR(MAX)  -- Изменяем тип столбца на VARCHAR для хранения строки
                )
            """)
            db.commit()
            
            cursor.execute("SELECT * FROM UserData WHERE Username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                cursor.execute("UPDATE UserData SET Signature = ? WHERE Username = ?", (base64.b64encode(signature).decode('utf-8'), username))
            else:
                cursor.execute("INSERT INTO UserData (Username, Signature) VALUES (?, ?)", (username, base64.b64encode(signature).decode('utf-8')))
            db.commit()
            cursor.close()
            db.close()
            print("Data inserted successfully")
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e.args[0])
            return False


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port', port)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
