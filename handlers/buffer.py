import yaml
import logging
import argparse
import propeller.paddle as propeller
import paddlehub as hub
from easydict import EasyDict as edict
from tornado.concurrent import Future
from .knowledge_retrieval_tornado import train_erniesage_base_predict
# from .unilm import main_test

class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache2 = []
        '''
                self.cache 格式如下:
                [{'id': ..., 'body': 输入的内容, 'secret_message': 机器回复的内容}]
                '''
        self.cache_size = 200
        self.module = hub.Module("Dialog_music")
        self.module2 = hub.Module("Dialog_film")

    def wait_for_messages(self, cursor=None):
        result_future = Future()
        if cursor:
            new_count = 0
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.cache[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        future.set_result([])

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if (len(self.cache) > self.cache_size):
                self.cache = self.cache[-self.cache_size:]

    def new_messages2(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache2.extend(messages)
        if (len(self.cache2) > self.cache_size):
                self.cache2 = self.cache2[-self.cache_size:]
   
    def return_messages():
        return self.cache 
