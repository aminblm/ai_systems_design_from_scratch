class LoadBalancer:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, servers):
        self.servers = servers 

    def handle_requests(self, request):
        for server in self.servers:
            response = server(request)
            if response: return response
            continue
    

def server1(request):
    if request == "hello": return "Hello, welcome to the Load Balancer."
    else: return None

def server2(request):
    if request == "world": return "World! This is server 2."
    else: return None 

def server3(request): 
    if request == "bye": return "Goodbye! Have a great day."
    else: return None 

if __name__ == "__main__":
    lb = LoadBalancer([server1, server2, server3])
    print("Load balancer is running, type a request to send it to a server.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit": break 
        print(f'Load Balancer: {lb.handle_requests(user_input.lower())}')