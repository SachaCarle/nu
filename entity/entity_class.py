from . import Mind, Body

class Entity:
    Mind = Mind
    Body = Body
    def __init__(self, **body_data):
        body = self.__class__.Body(self, body_data)
        self.__mind__ = self.__class__.Mind(self, body)
    def __call__(self, *args, **kwargs):
        return self.__mind__(*args, **kwargs)