import nu, os
me = nu.entity.spirit('entity.json')
def loop(app):
    me.think('Hello there')

me.loop = loop
me.think('Hello World')
if not me.body.file.exists():
    me.think('I will create my body')
    me.body.set(nu.abstract('body.html'))
if 'FLASK_APP' in os.environ:
    app = me.body.serve()
    me.think('API loaded, listening')
else:
    me.think("Created")