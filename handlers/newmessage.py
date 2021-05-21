import logging
import paddlehub as hub
import tornado.web
import uuid
import json
from .buffer import MessageBuffer
from .knowledge_retrieval_tornado import train_erniesage_base_predict

global_message_buffer = MessageBuffer()

class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):        
        history_messages = global_message_buffer.cache
        query = []
        
        if len(history_messages) >= 1:
            start_index = max(len(history_messages) - 7, 0)
            query_messages = history_messages[start_index:]
            for message in query_messages:
                query.append(message["body"])
        query.append(self.get_argument("body"))
        
        ''' 
        if len(history_messages) >= 1:
            start_index = max(len(history_messages) - 7, 0)
            query_messages = history_messages[start_index:]
            for message in query_messages:
                query.append(message["body"])
                query.append(message["response"])
        query.append(self.get_argument("body")) 
        '''
        # 都没有加上response的信息！
        query_re = ' '.join(query)  # 用于检索知识
        query_ge = '|'.join(query)  # 用于生成对话

        klgs = train_erniesage_base_predict.kr_main(query_re)[:5]
        klgs_ge = '|'.join(klgs)
        input_text_ = "%s:%s" % (query_ge, klgs_ge)
        input_text_ = input_text_[:510]
        input_text = [input_text_]
        # 生成回复
        # print(input_text)
        result = global_message_buffer.module.generate(texts=input_text,
                                                       use_gpu=True,
                                                       beam_width=1)[0][0]
        
        # klgs = ["超级星光大道", "超级星光大道", "超级星光大道", "超级星光大道", "超级星光大道"]
        # result = "Just for test"
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
            "retrieval_spo": klgs,
            "response": result
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        message["html_kg"] = tornado.escape.to_basestring(
            self.render_string("kg_music.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message) # 默认会转换为json字符串返回
        global_message_buffer.new_messages([message])

class MessageNewHandler2(tornado.web.RequestHandler):
    def post(self):
        history_messages = global_message_buffer.cache2
        
        query = []
        if len(history_messages) >= 1:
            start_index = max(len(history_messages) - 7, 0)
            query_messages = history_messages[start_index:]
            for message in query_messages:
                query.append(message["body"])
        query.append(self.get_argument("body2"))
        query_re = ' '.join(query)  # 用于检索知识
        query_ge = '|'.join(query)  # 用于生成对话
        klgs = train_erniesage_base_predict.kr_main2(query_re)[:5]
        klgs_ge = '|'.join(klgs)
        input_text_ = "%s:%s" % (query_ge, klgs_ge)
        input_text_ = input_text_[:510]
        input_text = [input_text_]
        # 生成回复
        result = global_message_buffer.module2.generate(texts=input_text,
                                                                    use_gpu=True,
                                                                    beam_width=1)[0][0]
        
        # klgs = ["超级大笨蛋", "超级大笨蛋", "超级大笨蛋", "超级大笨蛋", "超级大笨蛋"]
        # result = "Just for fun"
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body2"),
            "retrieval_spo": klgs,
            "response": result
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        message["html_kg"] = tornado.escape.to_basestring(
            self.render_string("kg_music.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message) # 默认会转换为json字符串返回
        global_message_buffer.new_messages2([message])



