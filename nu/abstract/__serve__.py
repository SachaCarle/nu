import nu, os
me = nu.entity.spirit(os.path.join('.entity', 'entity.json'))
if not me.body.file.exists():
    me.think('I created a default body.', me.default_body, " at ", me.body.file)
    me.body.set(nu.abstract(me.default_body))
me.awake()
app = me.serve()
#me.think('API loaded, listening.')
