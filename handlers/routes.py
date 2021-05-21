from handlers.mainhandler import MainHandler
from handlers.newmessage import MessageNewHandler
from handlers.newmessage import MessageNewHandler2
from handlers.updatemessage import MessageUpdatesHandler
from handlers.savemessage import MessageSaver, MessageSaver2

route = [
            (r"/", MainHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/new2", MessageNewHandler2),
            (r"/a/message/updates", MessageUpdatesHandler),
            (r"/a/message/save", MessageSaver),
            (r"/a/message/save2", MessageSaver2)
        ]
