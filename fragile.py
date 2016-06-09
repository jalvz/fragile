import sys, getopt
from flask import Flask
from opbeat.contrib.flask import Opbeat

app = Flask(__name__)


def instrument(env):
    return Opbeat(
        app,
        organization_id=env.organization_id,
        app_id=env.app_id,
        secret_token=env.secret_token)


@app.route('/')
def main():
    return 'So far so good...'


@app.route('/errors/runtime')
def key_error():
    return {}['boom']


if __name__ == '__main__':
    args = sys.argv[1:]
    opts, _ = getopt.getopt(args, 'env:')
    env_str = opts.get('env', 'local')
    m = __import__('conf.' + env_str, fromlist=[''])
    instrument(m)
    app.run()
