from network import Listener, Handler, poll
from time import sleep


handlers = {}  # map client handler to user name
i = 0
class MyHandler(Handler):
    
    def on_open(self):
        print "welcome"
        
    def on_close(self):
        print 'Goodbye'
        del handlers[self]
        for h in handlers:
            h.do_send("goodbye")
    def on_msg(self, msg):
        if 'join' in msg:
            print handlers.viewvalues()
            username = msg['join']
            if not msg['join'] in handlers:
                handlers[self] = msg['join']
            else:
                handlers[self].append(msg['join'])
            handlers[self] = msg['join']
            userName = username + " Joined"
            for h in handlers:
                h.do_send(userName)
            for h in handlers:
                h.do_send('Users: ' + handlers[self])
        elif 'speak' in msg:
            for h in handlers :
                print h
                if h != msg['speak']:
                    h.do_send(msg['speak'] + ': ' + msg['txt'])
        elif 'close' in msg:
            self.on_close(self)
        
        print msg
       
        
        
        
    
class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)
while 1:
    poll()
    sleep(0.05)  # seconds

