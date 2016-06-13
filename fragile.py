import os
import random
import string
import sys, getopt

import requests
from flask import Flask
from opbeat.contrib.flask import Opbeat

app = Flask(__name__)


@app.route('/')
def main():
    return 'So far so good...'


@app.route('/errors/group')
def assertion_error():
    """
    Creates a new error group every time this end point is hit
    """
    import imp
    module_name = ''.join(random.sample(string.letters, 10))
    m = imp.new_module(module_name)
    exec _nope_code in m.__dict__
    m.nope()


_nope_code = \
"""
def nope():
    raise AssertionError('Nope')
"""


@app.route('/errors/log')
def key_error():
    """
    Creates an error log that goes to the same group
    """
    return {}['invalid lines?']


@app.route('/release/')
def release():
    return _release(push=True)


@app.route('/bad-release/')
def bad_release():
    return _release(push=False)


def _release(push=True):
    os.chdir(os.path.dirname(__file__))

    f = os.path.join(os.path.dirname(__file__), 'elephant.txt')

    with open(f, "r") as elephant_counter:
        next_elephant = str(elephant_counter.read().count('\n') - 4)

    with open(f, "a") as elephant_song:
        elephant_song.write(next_elephant + ' elephants stood on the web of a spider...\n')

    os.popen('git add elephant.txt').read()
    os.popen('git commit -m "add another elephant"').read()
    if push:
        os.popen('git push').read()

    url = _M.intake_base_url + '/api/v1/organizations/' + _M.organization_id + '/apps/' + _M.app_id + '/releases/'
    rev = os.popen('git log -n 1 --pretty=format:%H').read()
    branch = 'master'  # os.popen('git rev-parse --abbrev-ref HEAD').read()

    h = {'Authorization': 'Bearer ' + _M.secret_token}
    d = {'rev': rev, 'branch': branch, 'status': 'completed'}

    r = requests.post(url, data=d, headers=h)
    assert r.status_code < 300

    return 'SHiP MaSTer'


_M = None


def _instrument():
    """Shall someone init _M first"""
    return Opbeat(
        app,
        organization_id=_M.organization_id,
        app_id=_M.app_id,
        secret_token=_M.secret_token)


def run_flask(env):
    """
    Order of operations in here is relevant.
    Don't do this at home. NEVER.
    """
    global _M

    _M = __import__('sssh.' + env, fromlist=[''])  # lol

    app.config['OPBEAT'] = {'SERVERS': [_M.intake_base_url]}

    _instrument()

    app.run(threaded=True)

if __name__ == '__main__':
    args = sys.argv[1:]
    opts, _ = getopt.getopt(args, '-e:')
    env_str = dict(opts).get('-e', 'local')
    run_flask(env_str)
