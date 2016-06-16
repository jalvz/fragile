import logging

from fragile import _instrument

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

import multiprocessing as mp


def send_errors(batch):

    opbeat = _instrument('prd')

    for j in range(batch):
        opbeat.client.capture('Message', param_message={'message': 'Hello there, again 3'}),
    for transport in opbeat.client._transports.values():
        transport.close()


if __name__ == '__main__':

    processes = [mp.Process(target=send_errors, args=(20,)) for x in range(1, 10)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
