from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json

import os
import subprocess as sp

# subprocess
workoutbotproc = None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = str(self.rfile.read(content_length))
        response = BytesIO()

        global workoutbotproc

        if os.environ['SLACK_VERIFICATION_TOKEN'] not in body:
            response.write(b'Invalid request origin')
            self.send_response(403)
            self.end_headers()
            self.wfile.write(response.getvalue())

        if "stop" in body:
            response.write(b'Workout lottery stopped')
            if workoutbotproc is not None:
                sp.Popen.terminate(workoutbotproc)
                workoutbotproc = None
        elif "start" in body:
            if workoutbotproc is None:
                response.write(b'Workout lottery started')
                workoutbotproc = sp.Popen(['python3','slackbotExercise.py'])
            else:
                response.write(b'Workout lottery already running')
        elif "status" in body:
            response.write(b'Server status up and running')
        else :
            response.write(b'Unsupported command')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.getvalue())


port = os.environ.get('PORT', 5000)
httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
print("Web Server Running")
httpd.serve_forever()