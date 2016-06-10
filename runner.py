import requests

from fragile import run_flask

if __name__ == '__main__':
    run_flask('prd')
    for _ in range(20):
        print 'crush it...'
        requests.get('/errors/log')

