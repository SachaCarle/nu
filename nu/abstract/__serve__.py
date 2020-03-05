import nu, os
me = nu.entity.spirit('entity.json')
me.awake()
if not me.body.file.exists():
    #me.think('I created a default body.')
    me.body.set(nu.abstract('body.html'))
app = me.serve()
#me.think('API loaded, listening.')
