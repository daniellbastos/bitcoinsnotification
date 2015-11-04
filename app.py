import functools
from bottle import jinja2_view, route, run

view = functools.partial(jinja2_view, template_lookup=['templates'])


@route('/', name='index')
@view('index.html')
def index():
    return {'title': 'Hello World'}


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000, debug=True)
