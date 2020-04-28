class Body(dict):
    def __getitem__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __init__(self, entity, body_data):
        for k, v in body_data.items():
            if isinstance(v, (tuple, list)):
                pass
        dict.__init__(self, body_data)
