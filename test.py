import nuthon

code = nuthon.imp('./target.py', {
    'B': '"B ok"',
    'C': 'print ("C ok")',
    'E': 'print (e)'
})
print (code)
code({
    'D': 'D ok',
    'e': 'E ok',
})