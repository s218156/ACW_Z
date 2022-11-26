#!/usr/bin/env python3
import http.server
import socketserver
import re
import os
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs


#print('source code for "http.server":', http.server.__file__)


class web_server(http.server.SimpleHTTPRequestHandler):
    
   def do_GET(self):

        print(self.path)
        path = urlparse(self.path)
        params = parse_qs(path.query) 
        
        if path.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()            
            if params.get('str', None):
                parameter = params.get('str')[0]
                result = {'lowercase': 0, 'uppercase': 0, 'digits': 0, 'special': 0}
                for sign in parameter:
                    if sign.islower():
                    	result['lowercase'] += 1
                    elif sign.isupper():
                    	result['uppercase'] += 1
                    elif sign.isdigit():
                    	result['digits'] += 1
                result['special']=len(parameter)-result['digits']-result['uppercase']-result['lowercase']
                
                self.wfile.write(str.encode(str(result)))
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080


print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
