from flask import Flask, request, Response
import socket
import os
import time
import sys
import netifaces

app = Flask(__name__)

exit_code = -1
start_time = time.time()

@app.route('/')
@app.route('/hostname')
def do_hostname():
    try:
        hostname = socket.gethostname()
        return hostname + '\n'
    except Exception as e:
        return f'Error: {str(e)}!\n'

@app.route('/echo', methods=['POST'])
def do_echo():
    data = request.get_data(as_text=True)
    return Response(data, content_type='text/plain')

@app.route('/echoheaders')
def do_echoheaders():
    headers = [f'{key}={value}' for key, value in request.headers.items()]
    return '\n'.join(headers) + '\n'

@app.route('/fqdn')
def do_fqdn():
    try:
        fqdn = socket.getfqdn()
        return fqdn + '\n'
    except Exception as e:
        return f'Error: {str(e)}!\n'

@app.route('/ip', methods=['GET'])
def do_ip():
    try:
        ip_addresses = []
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                for entry in addresses[netifaces.AF_INET]:
                    ip_addresses.append(entry['addr'])
        return '\n'.join(ip_addresses) + '\n'
    except Exception as e:
        return f'Error: {str(e)}!\n'

@app.route('/env')
def do_env():
    env_variables = [f'{key}={value}' for key, value in os.environ.items()]
    return '\n'.join(env_variables) + '\n'

@app.route('/healthz')
def do_healthz():
    uptime = time.time() - start_time
    return f'Uptime {uptime:.2f}\nOK\n'

@app.route('/healthz-fail')
def do_fail_healthz():
    fail_at = 10.0
    uptime = time.time() - start_time
    if uptime < fail_at:
        return f'still OK, {fail_at - uptime:.1f} seconds before failing\n'
    else:
        return f'failed since {uptime - fail_at:.1f} seconds\n'
    
@app.route('/exit/<int:code>')
def do_exit(code):
    global exit_code
    exit_code = code
    return f'Exiting with code {code}\n'

@app.teardown_request
def teardown(exception):
    if exit_code != -1:
        os._exit(exit_code)

if __name__ == '__main__':
    serve_port = int(os.getenv('TEST_SERVICE_PORT', '8080'))

    app.run(host='0.0.0.0', port=serve_port)
