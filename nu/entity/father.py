def pray(e):
    def _pray(*args, before_end=None, **kwargs):
        e.think('__PRAY_ENTER__')
        e.think(' '.join([ "'" + str(_) + "'" for _ in args]))
        #e.think(kwargs)
        if before_end:
            before_end()
        e.think("__PRAY_END__")
    return _pray