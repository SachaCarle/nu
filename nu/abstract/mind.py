import nu, sys, os
from pathlib import Path
me = nu.entity.spirit('entity.json')
me.think('Hello World')
if not me.body.file.exists():
    me.think('I will create my body')
    me.body.set(nu.abstract('body.html'))
if 'FLASK_APP' in os.environ:
    app = me.body.serve()
    me.body.show()
    me.think('API loaded, listening')
else:
    me.think("Created")