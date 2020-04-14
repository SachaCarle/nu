from . import AbstractInterface, AbstractException

class Cobj(object): pass

LS = [
AbstractInterface(),
AbstractInterface(0),
AbstractInterface(0.67),
AbstractInterface('hello'),
# []
AbstractInterface([]),
AbstractInterface([0, 1, 4, "heee"]),
AbstractInterface(["hello", {'lolz': None}]),
AbstractInterface([
    ["hello", {'lolz': None}],
    "Should not be linked by default:",
    AbstractInterface('Hello There !!'),
    ]),
# {}
AbstractInterface({}),
AbstractInterface({0: 'loz', "ex": 5678}),
AbstractInterface({2: ['a', 6], "lol": {"mdr": "nope"}}),
# Other
AbstractInterface(set(['a', 'b', 'c'])),
# FUNCTIONS ? / CALLABLE
# OBJECT
AbstractInterface(Cobj()),
# CLASS

AbstractInterface(AbstractInterface()),
AbstractInterface(AbstractInterface(Cobj()))
]


FOR = "for"
ATTR = "ATTR"
SIZE = "SIZE"
FIELDS = "fziojef"
DIR = "kekfe"
SEADLED = "okeofkes"
tests = [
    SIZE,
    FOR,
    ATTR,
    FIELDS,
    DIR,
    SEADLED,
]

def _print (toggle, *args, **kwargs):
    if toggle == True:
        print ("TEST\t", *args, **kwargs)

_print (True, "___________________TEST___________________")
for x in LS:
    with AbstractInterface.unseal(x):
        mode = x.__mode__
        _type = x.__type__
        _VALUE = x.__abstract__
        if mode and mode() == 'ABSTRACT':
            with AbstractInterface.unseal(_VALUE):
                _VALUE_mode = _VALUE.__mode__

    _print(True, "\n\n!!\t\t", x, mode)

    def try_sealed():
        if SEADLED in tests:
            try:
                _print (x)
                _print (x.__abstract__)
            except AbstractException as identifier:
                pass
            else:
                _print ("UNEXPECTED EXCEPTION")
                assert False
        return True

    assert try_sealed()
    if SIZE in tests:
        s = AbstractInterface.size(x)
        _print (' - SIZE START', s)

    assert try_sealed()
    if FOR in tests:
        _print(" - FOR", x)
        for _ in x:
            _print ('\t', _)


    assert try_sealed()
    if FIELDS in tests:
        _print (" - FIELDS ASSERT OF", x, " --> ", mode)
        TRIIFER = False
        if mode:
            _print ('OEZOEK   -> ', mode())
            if ( mode() == "ABSTRACT" and _type == AbstractInterface):
                print (repr(x), mode(), _type)
                print (
                    _VALUE,
                    _VALUE_mode
                )
                if _VALUE_mode and _VALUE_mode() in ["ABI_OBJECT", "ABSTRACT"]:
                    input()
                    TRIIFER = True
        if mode and (mode() in ["ABI_OBJECT"] or TRIIFER) :
            x.field_name = "Abi_Object interface is working !!"
            _print (x.field_name)
            try:
                # testing ABI.do = ABI()
                _print (x)
                x.abi_name = AbstractInterface()
                _print (x.abi_name)
            except AbstractException as identifier:
                raise identifier
            else:
                _print ("UNEXPECTED EXCEPTION?")
                #assert False
            try:
                # testing ABI.do = ABI()
                x.abi_hard_name = AbstractInterface(Cobj())
                _print (x.abi_hard_name)
            except AbstractException as identifier:
                pass
            else:
                _print ("UNEXPECTED EXCEPTION?")
                assert False
        else:
            try:
                x.field_name = "LOLZ"
            except AbstractException as identifier:
                pass
            else:
                _print ( "UNEXPECTED EXCEPTION", x)
                with AbstractInterface.unseal(x):
                    assert x.__type__ == AbstractInterface
            try:
                _print (x.field_name)
            except AbstractException as identifier:
                pass
            else:
                _print (True, "UNEXPECTED EXCEPTION", repr(x), _type)
                input()
                assert False


    assert try_sealed()
    if DIR in tests:
        _print (" - DIR OF", x)
        _print (dir(x))
        _print (list(iter(x)))

    assert try_sealed()
    if ATTR in tests:
        _print (" - ATTRIBUTE OF", x)
        class Exemple:
            attr_name = x
        _print (Exemple.attr_name)
        y = Exemple()
        _print (y.attr_name)
        y.attr_name = 0
        _print (y.attr_name)

    assert try_sealed()
    if SIZE in tests:
        assert s == AbstractInterface.size(x)

    assert try_sealed()

print ('FINISHED PROPERLY')