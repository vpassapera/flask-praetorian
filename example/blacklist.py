import flask
import flask_cors
import flask_praetorian
import flask_sqlalchemy
import tempfile

from runner import runner

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()


# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active


blacklist = set()


def is_blacklisted(jti):
    return jti in blacklist


# Initialize flask app for the example
app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'days': 10000}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 10000}

# Initialize the flask-praetorian instance for the app with is_blacklisted
guard.init_app(app, User, is_blacklisted=is_blacklisted)

# Initialize a local database for the example
local_database = tempfile.NamedTemporaryFile(prefix='local', suffix='.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(local_database)
db.init_app(app)

# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

# Add users for the example
with app.app_context():
    db.create_all()
    db.session.add(User(
        username='TheDude',
        password=guard.encrypt_password('abides'),
    ))
    db.session.add(User(
        username='Walter',
        password=guard.encrypt_password('calmerthanyouare'),
        roles='admin'
    ))
    db.session.add(User(
        username='Donnie',
        password=guard.encrypt_password('iamthewalrus'),
        roles='operator'
    ))
    db.session.add(User(
        username='Maude',
        password=guard.encrypt_password('andthorough'),
        roles='operator,admin'
    ))
    db.session.commit()


# Set up some routes for the example

# curl http://localhost:5000/login -X POST \
#   -d '{"username":"Walter","password":"calmerthanyouare"}'
@app.route('/login', methods=['POST'])
def login():
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return flask.jsonify(ret), 200


# curl http://localhost:5000/protected -X GET \
#   -H "Authorization: Bearer <your_token>"
@app.route('/protected')
@flask_praetorian.auth_required
def protected():
    return flask.jsonify(message='protected endpoint (allowed user {})'.format(
        flask_praetorian.current_user().username,
    ))


@app.route('/blacklist_token', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_required('admin')
def blacklist_token():
    """
    Blacklists an existing JWT by registering its jti claim in the blacklist.

    .. example::
       $ curl http://localhost:5000/blacklist_token -X POST \
         -d '{"token":"<your_token>"}'
    """
    req = flask.request.get_json(force=True)
    data = guard.extract_jwt_token(req['token'])
    blacklist.add(data['jti'])
    return flask.jsonify(message='token blacklisted ({})'.format(req['token']))


# Run the example
if __name__ == '__main__':
    runner(app)
