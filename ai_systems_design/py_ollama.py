class SimpleChatbot:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        # Disctionary of predifined responses
        self.responses = {
            "hello": "Hello! How can I assist you today?",
            "hi": "Hi there! How can I help you?",
            "how are you": "I'm just a simple chatbot. How can I assist you?",
            "good day": "Good day! How can I help you?",
            "bye": "Goodbye! Have a great day!",
            "what is your name?": "I'm a simple chatbot. I don't have a name.",
            "what can you do?": "I can answer questions and chat with you.",
            "thank you": "You're welcome! 😊",
            "how to get started?": "You can ask me anything, and I'll try my best to help!"
        }
        
    def get_response(self, user_input):
        if user_input in self.responses: return self.responses[user_input]
        else: return "Sorry, I can't help with that!"

if __name__ == "__main__":
    chatbot = SimpleChatbot()
    while True:
        user_input = input("User: ")
        if user_input == "exit": break
        print(f'Bot: {chatbot.get_response(user_input)}')