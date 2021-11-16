from threading import Thread
from queue import Queue
from contextlib import AbstractContextManager

class ParallelMerge(AbstractContextManager):
    _quit = False
    _finished_threads = 0

    def __init__(self, *iterators, sentinel=object(), queue_maxsize=0, daemon=False):
        self._sentinel = sentinel
        self._queue = Queue(maxsize=queue_maxsize)
        self._threads = [Thread(name=repr(it), target=self._run, args=[it, idx]) for idx, it in enumerate(iterators)]
        for thread in self._threads:
            thread.daemon = daemon

    def _run(self, iterator, idx):
        try:
            for value in iterator:
                if self._quit:
                    break
                self._queue.put(value)
                print(idx)
        finally:
            self._queue.put(self._sentinel)

    def __iter__(self):
        while self._finished_threads < len(self._threads):
            value = self._queue.get()
            if value == self._sentinel:
                self._finished_threads += 1
            else:
                yield value

    def __enter__(self):
        for thread in self._threads:
            thread.start()
        return self

    def __exit__(self, *_):
        self._quit = True
        for _ in self:
            pass
        for thread in self._threads:
            thread.join()
