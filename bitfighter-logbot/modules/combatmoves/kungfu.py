

import moves
import random
import time

class KungFu():

    logMessage = "%Y-%m-%d %H:%M:%S> Module(%(name)s): %(message)s"

    def __init__(self, bot):
        # Reference to our main bot
        self.bot = bot
        
        # IRC message body, not the corpse
        self.body = None
        self.damaged = {'status':False, 'time': 0}
        self.idle = {'status':True, 'time': time.time()}
        
    def name(self):
        return self.__class__.__name__
    

    def on_privmsg(self, c, e):
        self._on_msg(c, e)

    def on_pubmsg(self, c, e):
        self._on_msg(c, e)

    def on_ctcp(self, c, e):
        ctcptype = e.arguments[0]
        if ctcptype == "ACTION":
            self._on_msg(c, e)
        elif ctcptype == "PING":
            self.on_ping(c, e)
        else:
            # Just ignore it
            #SingleServerIRCBot.on_ctcp(self, c, e)
            pass

    def on_ping(self, c, e):
        target = e.target
        random.seed()
        if self.damaged['status']:
            if random.randint(1,100) * self._get_modifier(self.damaged['time']) > random.randint(50,150):
                print time.strftime(self.logMessage, time.gmtime()) % {
                    'message': "Still damaged",
                    'name': self.name()
                }
                self.damaged['time'] = time.time()
                n = random.randint(0,len(moves.damagedmsg)-1)
                self.bot.prvmsg_append_to_log(c, target, moves.damagedmsg[n])
            else:
                print time.strftime(self.logMessage, time.gmtime()) % {
                    'message': "Still damaged, but no message",
                    'name': self.name()
                }
        else:
            if random.randint(1,100) * self._get_modifier(self.idle['time']) > random.randint(80,200):
                print time.strftime(self.logMessage, time.gmtime()) % {
                    'message': "Idle event",
                    'name': self.name()
                }
                self.idle['time'] = time.time()
                n = random.randint(0,len(moves.idlemsg)-1)
                self.bot.prvmsg_append_to_log(c, target, moves.idlemsg[n])

    def _get_modifier(self, t1):
        return abs(int(time.time() - t1) / 60 ) * 0.10

    def _on_msg(self, c, e):
        target = e.target

        self.body = e.arguments[0]
        if self.body == '' or self.body[0] == "<" or self.body[0:1] == " <":
            return

        if self.body[0] == ':':
            pass # special commands
        elif self.bot._nickname.lower() in self.body.lower():
            random.seed()
            if "repair" in self.body and self.damaged['status']:
                self.damaged.update({'status': False, 'time': time.time()})
                self.bot.prvmsg_append_to_log(c, target, "Good as new, I think. Am I leaking?")
                return

            for move in list(moves.attacks):
                if move in self.body:
                    n = random.randint(0,len(moves.getdamagemsg)-1)
                    self.bot.prvmsg_append_to_log(c, target, moves.getdamagemsg[n])
                    self.damaged.update({'status': True, 'time': time.time()})
                    return
            n = random.randint(1, len(moves.scaredmsg)) - 1
            self.bot.prvmsg_append_to_log(c, target, moves.scaredmsg[n])
            
