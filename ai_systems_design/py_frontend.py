class Component:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name, data=None, methods=None):
        self.name = name
        self.data = data if data is not None else {}
        self.methods = methods if methods is not None else {}
        self.events = {}

    def __repr__(self):
        return f'Component ({self.name}, data={self.data}, methods={self.methods})'


class DataBinder:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.components = {}
        self.rendered = []

    def add_component(self, component):
        self.components[component.name] = component 

    def render(self):
        self.rendered = []
        for component in self.components.values(): self._render_component(component)
        return self.rendered

    def _render_component(self, component):
        # Simulate DOM rendering
        dom = f"<div id='{component.name}'>{component.data['text']}</div>"
        self.rendered.append(dom)
        return dom


class EventDispatcher:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, handler):
        self.listeners[event_type] = handler 

    def trigger_event(self, event_type, data):
        handler = self.listeners.get(event_type)
        if handler: handler(data)
    

class UI:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.data_binder = DataBinder()
        self.event_dispatcher = EventDispatcher()

    def create_component(self, name, data=None, methods=None):
        component = Component(name, data, methods)
        self.data_binder.add_component(component)
        return component

    def bind_data(self, component, key, value):
        component.data[key] = value

    def run(self):
        self.data_binder.render()
        print("Rendered UI:")
        for html in self.data_binder.render():
            print(html)


if __name__ == "__main__":
    ui = UI()
    # Example: create a button component
    button = ui.create_component("button", {"text": "Click Me"}, {"click": ui.event_dispatcher.trigger_event})
    ui.bind_data(button, "text", "Hello world!")
    ui.run()
    