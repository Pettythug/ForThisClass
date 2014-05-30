from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    count = 0;
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        count = 0
        check = True
        personal = False
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:      
            name, txt = msg['speak'], msg['txt']
            count = len(txt.split())            
            for x in txt.split():
                count -= 1
                word = x[1:]                
                if x.startswith('+') and personal == False:
                    count = 0
                    check = False                   
                    if word in subs.keys():
                        if name not in subs.get(word):
                            subs.setdefault(word,[]).append(name) 
                    else:
                        subs.update({word:[name]})                    
                   
                elif x.startswith("#") and personal == False and check == True:
                    count = 0
                    check = False
                    while not check:                       
                        if word in subs:
                            for value in subs.get(word):
                                for h in handlers:
                                    if value in handlers.get(h) and value != self:
                                        h.do_send(msg)
                                        check = True
                                                                   
                elif x.startswith('-') and personal == False: 
                    count = 0  
                    check = False                
                    if word in subs.keys():
                        if name in subs.get(word):
                            subs.setdefault(word,[]).remove(name) 
                            
                            
                elif x.startswith("@"):
                    for h in handlers:
                        for j in handlers.get(h):
                            if x == j:
                                h.do_send(msg) 
                                check = False 
                                personal == True 
                elif count == 0 and check == True and personal == False: 
                    broadcast({'speak': name, 'txt': txt})


Listener(8888, MyHandler)
while 1:
    poll(0.05)
