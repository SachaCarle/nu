from . import Mind, Body
from pydispatch import dispatcher

class Entity:
    Mind = Mind
    Body = Body
    def __init__(self, **body_data):
        body = self.__class__.Body(self, body_data)
        self.__mind__ = self.__class__.Mind(self, body)
    def __call__(self, *args, **kwargs):
        return self.__mind__(*args, **kwargs)
    def __getattr__(self, key):
        return self.__mind__[key]
    def __gt__(self, event_key):
        if isinstance(event_key, str):
            dispatcher.send(event_key, self, self)
        elif isinstance(event_key, (tuple, list)) and isinstance(event_key[-1], dict):
            dispatcher.send(event_key[0], self, self, *event_key[1:-1], **event_key[-1])
        elif isinstance(event_key, (list, tuple)):
            dispatcher.send(event_key[0], self, self, *event_key[1:])
        else:
            assert False, 'Unknow event: ' + repr(event_key)
    def receive(self, event_key, sender=dispatcher.Any):
        assert isinstance(event_key, str), 'Invalid event key: ' + repr(event_key)
        def register_handler(fun):
            dispatcher.connect(fun, signal=event_key, sender=sender)
            return fun
        return register_handler
