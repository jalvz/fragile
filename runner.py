import threading
from multiprocessing import Process


import requests
import thread

from fragile import run_flask

if __name__ == '__main__':

    thread.start_new_thread(run_flask, ('prd',))

    f = lambda: requests.get('http://localhost:5000/errors/log')
    ts = []
    for e in range(500):
        #f()
        t = Process(target=f)  # threading.Thread(target=f)
        ts.append(t)
        t.start()
        #   thread.start_new_thread(requests.get, ('http://localhost:5000/errors/log',))
        print 'Sent error {}'.format(e)

    for t in ts:
        t.join()

    #import time
    #time.sleep(10)

    print 'done'
