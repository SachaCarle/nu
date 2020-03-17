import nu, os
me = nu.entity.spirit('entity.json')
if not me.body.file.exists():
    me.think('I created a default body.', me.default_body)
    me.body.set(nu.abstract(me.default_body))
me.awake()
app = me.serve()
#me.think('API loaded, listening.')
