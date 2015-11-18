# -*- coding: utf-8 -*-
import os
import jinja2
import json

from bottle import Bottle, static_file, redirect, request, response
from bottle import TEMPLATE_PATH as T

from con import foxbit
from actions import save_foxbit, save_contact

PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
T.insert(0, TEMPLATE_PATH)

app = Bottle()


@app.route('/', name='index')
@app.route('/<status>/', name='index')
def index(status=None):
    msg = None
    if status == 'ok':
        msg = 'Cadastro realizado com sucesso! Agora é só aguardar sua \
               notificação.'
    elif status == 'error':
        msg = 'Ocorreu um erro. Tente novamente.'
    last_data = foxbit.find().sort('timestamp', -1)
    if last_data.count() > 0:
        last_data = last_data[0]
        last_data['timestamp'] = last_data['timestamp'].strftime('%d/%m/%Y %H:%M')
    template = JINJA_ENVIRONMENT.get_template('index.html')
    return template.render({'last_data': last_data, 'msg': msg, 'status': status})


@app.route('/update/', name='update')
def update():
    save_foxbit()
    redirect('/')


@app.route('/save/', method='POST', name='save')
def save():
    email = request.POST['email']
    rules = request.POST['rules']
    value = request.POST['value']
    if email and rules and value:
        data = {
            'email': email,
            'rules': rules,
            'value': float(value),
            'sent': False
        }
        save_contact(data)
        redirect('/ok/')
    redirect('/error/')


@app.route('/history/', name='history')
def history():
    data = []
    for item in foxbit.find().sort('timestamp', -1):
        data.append({
            'timestamp': item['timestamp'].strftime('%d/%m/%Y'),
            'last': item['last']
        })
    response.content_type = 'application/json'
    return json.dumps(data)


@app.route('/robots.txt')
def serve_robots():
    return static_file('robots.txt', root=STATIC_PATH)


@app.route('/static/<path:path>', name='static')
def static(path):
    yield static_file(path, root=STATIC_PATH)


if __name__ == "__main__":
    ip = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8000))
    debug = ip == '0.0.0.0'
    app.run(host=ip, port=port, debug=debug)
