import time
import json
from collections import defaultdict 

class Redis:
    def __init__(self):
        self.data = {
            "strings": [],
            "hashes": {},
            "lists": [],
            "sets": set(),
            "sorted_sets": {},
            "pubsub": {}
        }
        self.rdv = None
        self.aof = None
        self.commands = {
            "GET": self.get,
            "SET": self.set,
            "DEL": self.del_,
            "INCR": self.incr,
            "DECR": self.decr,
            "EXPIRE": self.expire,
            "PEXPIRE": self.pexpire,
            "TTL": self.ttl,
            "PFADD": self.pfadd,
            "PFCOUNT": self.pfcount,
            "PERSIST": self.persist,
        }

    def run(self): 
        while True:
            cmd = input("Enter command (quit to exit): ").strip()
            if cmd == "quit": break 
            self.process_command(cmd)

    def process_command(self, cmd):
        if cmd not in self.commands: print("Unknown command."); return
        self.commands[cmd]()

    def get(self, key):
        if key in self.data["strings"]: return self.data["strings"][key]
        return None 
    
    def set(self, key, value):
        self.data["strings"][key] = value
        return True 
    
    def del_(self, key):
        if key in self.data["strings"]: del self.data["strings"][key]; return True
        return False

    def incr(self, key):
        if key in self.data["strings"]: return self.data["strings"][key] + 1
        return None
    
    def decr(self, key):
        if key in self.data["strings"]: return self.data["strings"][key] - 1
        return None
    
    def expire(self, key, seconds):
        if key in self.data["strings"]: self.data["strings"][key] = seconds; return True
        return False 
    
    def pexpire(self, key, seconds):
        if key in self.data["strings"]: self.data["strings"][key] = seconds; return True
        return False 
    
    def ttl(self, key): 
        if key in self.data["strings"]: return self.data["strings"][key]
        return -1
    
    def persist(self, key):
        if key in self.data["strings"]: self.data["strings"][key] = True; return True
        return False
    
    def pfcount(self, key):
        if key in self.data["strings"]: return self.data["strings"][key]
        return 0
    
    def pfadd(self, key, value):
        if key in self.data["strings"]: self.data["strings"][key].add(value); return True
        return False
    
    def run_rdb(self):
        # Simulate RDB snapshot
        self.rdv = {
            "strings": self.data["strings"],
            "hashes": self.data["hashes"],
            "lists": self.data["lists"],
            "sets": self.data["sets"],
            "sorted_sets": self.data["sorted_sets"],
        }
        print("RDB snqpshot saved")

    def run_aof(self):
        # Simulate AOF Logging
        self.aof = {"commands": []}
        print("AOF Logging started.")

if __name__ == "__main__":
    redis = Redis()
    redis.run()