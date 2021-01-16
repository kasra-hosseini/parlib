#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import multiprocessing as mp
import traceback

class Process(mp.Process):
    """Process and handle exceptions
    CREDIT: https://stackoverflow.com/a/33599967

    Example (from the same link above):

    def target():
        raise ValueError('Something went wrong...')
    
    p = Process(target = target)
    p.start()
    p.join()
    
    if p.exception:
        error, traceback = p.exception
        print(traceback)
    """
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception