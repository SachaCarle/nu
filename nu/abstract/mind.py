me.think('Where can I go ?', nu.drives)
if str(me.location).startswith('C'):
    me.move('D:\\')
elif 'C' in nu.drives:
    me.move('C:\\')