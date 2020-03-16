class IndentationFeedback(Exception):
    def __init__(self, *args):
        Exception.__init__(self)
        self.args = args



# UNUSED ?
def indent_mesure(l, indent, indent_type='    '):
    _indent = indent
    i = 0
    try:
        while _indent > 0:
            if l[0:len(indent_type)] != indent_type:
                raise IndentationFeedback(l[0:len(indent_type)])
            l = l[len(indent_type):]
            _indent -= 1
        i += 1
    except IndentationFeedback:
        return False
    return True