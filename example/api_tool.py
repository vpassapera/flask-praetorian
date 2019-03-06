import flask
import flask_cors
import logging
import os

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


# Initialize flask app for the example
app = flask.Flask(__name__)
app.debug = True
cors = flask_cors.CORS(app)


@app.route('/')
@app.route('/basic')
def basic():
    return flask.render_template(
        'basic.html',
        scripts=os.listdir(app.static_folder),
        api_port=5000,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


@app.route('/refresh')
def refresh():
    return flask.render_template(
        'refresh.html',
        scripts=os.listdir(app.static_folder),
        api_port=5010,
        access_lifespan=30,
        refresh_lifespan=2*60,
    )


@app.route('/blacklist')
def blacklist():
    return flask.render_template(
        'blacklist.html',
        scripts=os.listdir(app.static_folder),
        api_port=5020,
        access_lifespan=10000*24*60*60,
        refresh_lifespan=10000*24*60*60,
    )


@app.route('/custom')
def custom():
    return flask.render_template(
        'custom.html',
        scripts=os.listdir(app.static_folder),
        api_port=5030,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


@app.route('/register')
def register():
    return flask.render_template(
        'register.html',
        scripts=os.listdir(app.static_folder),
        api_port=5040,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


# Run the example
if __name__ == '__main__':
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Starts the api tool',
    )
    parser.add_argument('-H', '--host', default='0.0.0.0')
    parser.add_argument('-p', '--port', default=5000)
    parser.add_argument('-l', '--logfile')
    args = parser.parse_args()
    if args.logfile is not None:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
    app.run(host=args.host, port=args.port)
