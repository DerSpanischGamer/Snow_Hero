import json

from bottle import run, post, request, response

import subprocess

@post('/process')
def my_process():
    print("msg?")
    return 'All done'


subprocess.Popen("python Arduino.py ")
print("slkbn")
run(host='localhost', port=8080, debug=True)
