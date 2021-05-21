import json
import collections
import logging
import tornado.web
from .newmessage import global_message_buffer

class MessageSaver(tornado.web.RequestHandler):
    def post(self):
        save_value = self.get_argument("save")
        # print("SAVE!!!", save_value, type(save_value))
        if save_value == "false":
            pass
        else:
            fout = open("save_dialog_music.txt", "a")
            cache = global_message_buffer.cache
            dialog = []
            response_spo = {}
            for c in cache:
                dialog.append(c["body"])
                dialog.append(c["response"])
                spos = c["retrieval_spo"]
                response = c["response"]
                response_spo[response] = spos
            sample = collections.OrderedDict()
            sample["dialog"] = dialog
            sample["spos"] = response_spo
            sample = json.dumps(sample, ensure_ascii=False)
            fout.write(sample + "\n")
            fout.close()


class MessageSaver2(tornado.web.RequestHandler):
    def post(self):
        save_value = self.get_argument("save")
        # print("SAVE!!!", save_value, type(save_value))
        if save_value == "false":
            pass
        else:
            fout = open("save_dialog_film.txt", "a")
            cache = global_message_buffer.cache2
            dialog = []
            response_spo = {}
            for c in cache:
                dialog.append(c["body"])
                dialog.append(c["response"])
                spos = c["retrieval_spo"]
                response = c["response"]
                response_spo[response] = spos
            sample = collections.OrderedDict()
            sample["dialog"] = dialog
            sample["spos"] = response_spo
            sample = json.dumps(sample, ensure_ascii=False)
            fout.write(sample + "\n")
            fout.close()                
