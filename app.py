import functools
import os
from bottle import jinja2_view, route, run

view = functools.partial(jinja2_view, template_lookup=['templates'])


@route('/', name='index')
@view('index.html')
def index():
    return {'title': 'Hello World'}


if __name__ == "__main__":
    ip = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8000))
    debug = ip == '0.0.0.0'
    run(host=ip, port=port, debug)
