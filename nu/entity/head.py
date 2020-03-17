from flask import Flask, render_template, jsonify, send_file, request
from flask_script import Manager
from pathlib import Path
import sys, os, nu, json

def pythoncode(nupath='', **kwargs):
    mindpath = Path('mind.py')
    code = mindpath.read_text()
    return code

def awake(e):
    def _awake():
        mind = pythoncode()
        globs = {
                    'nu': nu,
                    'me': e
                }
        exec(mind, globs)
    return _awake

def define(e):
    def _define_creator(path, **ks_p):
        def _define_route(fun):
            def _register_route(app):
                #print ('Hello there', e, path, fun, app)
                app.route(path, **ks_p)(fun)
                # TODO: already registered
            e.head.routes[path] = _register_route
        return _define_route
    return _define_creator

def serve(e):
    def _serve():
        app = Flask(__name__)

        for path, fun in e.head.routes.items():
            fun(app)

        @app.route('/')
        def body():
            return send_file(str(os.path.join(e.location, 'body.html')), mimetype='application')
        @app.route('/kill')
        def endme():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
            return app.response_class(
                response=json.dumps({
                        "result": "Ended"
                    }),
                status=200,
                mimetype='application/json'
            )

#        @app.route('/<path:p>')
#        def index_js(p):
#            return send_file(str(os.path.join(e.location, p)), mimetype='application')

        return app
    return _serve
