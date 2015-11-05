import functools
import os
import pymongo
from bottle import jinja2_view, route, run, redirect
from con import mongolab
from bit_update import bitcoinaverage

view = functools.partial(jinja2_view, template_lookup=['templates'])


@route('/', name='index')
@view('index.html')
def index():
    history_list = mongolab.find().sort('timestamp', pymongo.DESCENDING)
    return {'history_list': history_list}


@route('/update/', name='update')
def update():
    bitcoinaverage()
    redirect('/')

if __name__ == "__main__":
    ip = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8000))
    debug = ip == '0.0.0.0'
    run(host=ip, port=port, debug=debug)
