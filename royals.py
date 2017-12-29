from flask import Flask, redirect, request, Response, url_for
from flask_socketio import SocketIO, send
import json
import os
from logic.utilities import status_code
import logic.utilities as utils
from logic.api_actions import Actions


app = Flask(__name__)
app.config['SECRET_KEY'] = utils.random_string(16)
socketio = SocketIO(app)
api_actions = Actions()
actions = api_actions.initialize_actions(socketio)
help_actions = {}
for key in actions.keys():
    action = actions[key]
    action.pop("function")
    help_actions[key] = action


def dict_to_json(dct):
    return json.dumps(dct, indent=4, separators=(',', ': '))


def handle_parameters(params, headers):
    arguments = {}
    success = True
    for param in params:
        arguments[param] = request.form.get(param, None)
        if arguments[param] is None:
            success = False
            return success, arguments
    for param in headers:
        try:
            arguments[param] = request.headers[param]
        except KeyError:
            success = False
            return success, arguments
    return success, arguments


@app.before_request
def before_request():
    if request.url.startswith('http://') and (not request.url.startswith('http://localhost')):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(location=url, code=status_code.redirect)


@app.route('/')
@app.route('/index.php')
@app.route('/default.aspx')
def index():
    return app.send_static_file('index.html')


@app.route('/logo')
def index():
    return app.send_static_file('img/royals.png')


# serve files from root url instead of static directory
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


@app.route('/api', methods=["POST", "GET"])
def api_main():
    out = {
        "success": True,
        "message": "This is a help command. Read the key actions to see all the available actions on the api",
        "actions": help_actions
    }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/api/<string:action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_actions(action):
    out = {
        "success": False,
        "message": "Use POST for action "+action+" and provide all the parameters as in the key params and headers."
    }
    try:
        if action in actions:
            params = actions[action]["parameters"]
            headers = actions[action]["headers"]
            description = actions[action]["description"]
            method = actions[action]["method"]
            out["params"] = params
            out["headers"] = headers
            out["message"] = description
            out["method"] = method
            if request.method == method:
                success, args = handle_parameters(params, headers)
                if success:
                    if "function" in actions[action]:
                        out = actions[action]["function"](**args)
                    else:
                        out["message"] = "Action "+action+" is not yet implemented, come back soon"
                else:
                    out["message"] = "Please provide all the headers and parameters as " \
                                     "provided in key headers and params"
            else:
                out["message"] = "Wrong method, please retry using method "+method
        else:
            out["message"] = "Unknown action, please check: "+url_for("/api")
    except Exception as e:
        utils.log_error("API action error:", str(e))
        out["message"] = "An e"
    return Response(dict_to_json(out), content_type="text/json")


@socketio.on('connect')
def connected(message, mess2):
    print("Client connected")
    print(message)
    send('connect', {'success': False})


@socketio.on('disconnect')
def disconnected(message, mess2):
    print("Client Disconnected")
    print(message)
    send('disconnect', {'success': False})


# Handle JSON data from an unnamed event
@socketio.on('json')
def handle_json(_json):
    print('received json: ' + str(_json))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app=app, host='0.0.0.0', port=port)
