def add(e):
    def _add(component_name):
        @e.memory.alter
        def __acode__(data):
            if not 'data' in data['components']:
                data['components']['data'] = []
            data['components']['data'].append(component_name)
            return data
    return _add
