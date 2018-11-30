import time
import json
from http.server import BaseHTTPRequestHandler


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print('{0} -- [{1}] {2}'.format(self.address_string(), 
                                        self.date_time_string(),
                                        self.requestline))
        fname = str(int(time.time())) + '.json'
        with open(fname, 'w') as f:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = json.loads(post_data)
            json.dump(post_data, f, indent=2)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.wfile.write('POST request {0}'.format(post_data).encode('utf-8'))

