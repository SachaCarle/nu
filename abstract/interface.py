from .exception import AbstractException
import numbers
from common import WithLambda
from inspect import currentframe, getframeinfo


sealing_debug = {

}
def open_seal(kls, self):
    #print ('\tOPEN', id(self))
    if object.__getattribute__(self, "__abstract_sealing__"):
        return object.__setattr__(self, '__abstract_sealing__', False)
    else:
        raise AbstractException('Cant open')
def close_seal(kls, self):
    return object.__setattr__(self, '__abstract_sealing__', True)
    #print ('\tCLOSE', id(self))


class AbIMode:
    def __init__(self, this, **kwargs):
        self.this = this
        self.opts = kwargs
    def __call__(self):
        return self.__class__.__name__
class ABI_OBJECT(AbIMode):
    def iter_abi_object(self):
        return iter(dir(self.this.__abstract__)) # TODO REDO pas beau :(
class UNIT(AbIMode):
    def iter_unit(self):
        return iter([self.this.__abstract__])
class ELEMENTS(AbIMode):
    def iter_elements(self):
        res = self.this.__abstract__
        if 'els_method_name' in self.opts.keys():
            res = getattr(self.this.__abstract__,self.opts['els_method_name'])()
        return iter(res)
class ABSTRACT(AbIMode):
    def iter_abstract(self):
        res = self.this.__abstract__
        return iter(res)

class AbstractInterface(object):

    @classmethod
    def size(kls, self):
        with kls.unseal(self):
            return self.__sizeof__()

    @classmethod
    def unseal(kls, self):
        return WithLambda(
            lambda: open_seal(kls, self),
            lambda: close_seal(kls, self)
        )

    def __started__(self):
        self.__sealed__()
    def __sealed__(self):
        object.__setattr__(self, '__abstract_sealing__', True)
        # ______________________ INIT
    def __init__(self, this=None):
        object.__setattr__(self, '__abstract_sealing__', False)
        t = type(this)
        not_found = True
        self.__mode__ = None
        self.__type__ = t
        if this is None:
            # None / Void
            self.__abstract__ = this
            not_found = False
        elif isinstance(this, AbstractInterface):
            # <>
            self.__abstract__ = this
            not_found = self.__init_abstract__()
        elif isinstance(this, numbers.Number) or isinstance(this, str):
            # 0123456789
            self.__abstract__ = this
            not_found = self.__init_unit__()
        elif isinstance(this, (list, dict, set, tuple)):
            self.__abstract__ = this
            not_found = self.__init_elements__()
        elif isinstance(this, object):
            self.__abstract__ = this
            not_found = self.__init_object__()
        if not_found: # "STRINGS !!!!!"
            raise AbstractException("Unknow object: " + str(this) + str(this is None))
        self.__started__()
    def __init_unit__(self):
        self.__mode__ = UNIT(self)
        return False
    def __init_elements__(self):
        if isinstance(self.__abstract__, (list, set)):
            self.__mode__ = ELEMENTS(self)
            return False
        if isinstance(self.__abstract__, dict):
            self.__mode__ = ELEMENTS(self, els_method_name='items')
            return False
        return True
    def __init_object__(self):
        self.__mode__ = ABI_OBJECT(self)
        return False
    def __init_abstract__(self):
        #print (self, self.__abstract__, self.__type__)
        self.__mode__ = ABSTRACT(self)

    # --------------------------------------------------------------     .
#    def __get__(self, this, kls):
#        with AbstractInterface.unseal(self):
#            return self.__abstract__
    def __get__(self, this, kls):
        #print (getframeinfo(currentframe()).lineno, "GET", self, this, kls)
        return self
    def  __getattribute__(self, key):
        #print (getframeinfo(currentframe()).lineno, 'GETATTRIBUTE', key)
        if key.startswith('__') and key.startswith('__'):
            if object.__getattribute__(self, "__abstract_sealing__") == False:
                return object.__getattribute__(self, key)
            else:
                raise AbstractException("Can't access ", key, " on ", self, " Because sealed")
        mode = object.__getattribute__(self, '__mode__')
        if mode and mode() == "ABI_OBJECT":
            value = object.__getattribute__(self, "__abstract__")
            return getattr(value, key)
        if mode and mode() == "ABSTRACT":
            value = object.__getattribute__(self, "__abstract__")
            return getattr(value, key)
        raise AbstractException("__getattribute__ not defined", key)
    # --------------------------------------------------------------     .


    # --------------------------------------------------------------     =
    def __set__(self, this, value):
        with AbstractInterface.unseal(self):
            self.__init__(value)
    def __set_init__(self, this, key):
        raise AbstractException(f'__set_init__ UNDEFINED ==> \n{self} \n\tassigned to \n{this} \n\tat \n{key}')
    def  __setattr__(self, key, value):
        #print (getframeinfo(currentframe()).lineno, "\tSETATTR\t", "\t", key)
        if object.__getattribute__(self, "__abstract_sealing__") == False:
            if key.startswith('__') and key.startswith('__'):
                #print ("\tA\t")
                return object.__setattr__(self, key, value)
        ABI_SET = False
        mode = object.__getattribute__(self, '__mode__')
        if mode and mode() == "ABI_OBJECT":
            self_value = object.__getattribute__(self, "__abstract__")
            setattr(self_value, key, value)
            ABI_SET = True
        if mode and mode() == "ABSTRACT":
            self_value = object.__getattribute__(self, "__abstract__")
            ab_mode = object.__getattribute__(self_value, '__mode__')
            if ab_mode:
                if ab_mode() in ['ABSTRACT', "ABI_OBJECT"]:
                    setattr(self_value, key, value)
                    ABI_SET = True
                else:
                    input()
                    print ('dramatic exit')
                    exit()
        if ABI_SET:
            if isinstance(value, AbstractInterface):
                with AbstractInterface.unseal(value):
                    if value.__mode__ and value.__mode__() == "ABI_OBJECT":
                        value.__set_init__(key, self)
                        return #print ("\tB\t")
                    elif isinstance(value.__abstract__, AbstractInterface):
                        value.__set_init__(key, self)
                        return #print ("\tC\t")
                    else: return #print ("\tD\t")
            elif mode: return #print ("\tE\t")
            else: return #print ("\tF\t")
        raise AbstractException(str(ABI_SET)  + "\n\t" + "-" + repr(self) + "__setattr__ not defined\t" + key  + "\t" + str(value))
    # --------------------------------------------------------------     =


    # --------------------------------------------------------------     ""
    def __str__(self):
        if object.__getattribute__(self, "__abstract_sealing__"):
            with AbstractInterface.unseal(self):
                return f"<{self.__class__.__name__}({self.__type__.__name__}): {repr(self.__abstract__)}>"
        else: return repr(self)
    def __repr__(self):
        return f"""<{object.__getattribute__(self, "__class__").__name__}({object.__getattribute__(self, "__type__").__name__})>"""
    # --------------------------------------------------------------     ""



    # --------------------------------------------------------------     FOR
    def __iter__(self):
        with AbstractInterface.unseal(self):
            if self.__type__ is type(None):
                return iter([])
            mode = self.__mode__()
            if mode == 'ABI_OBJECT':
                return self.__mode__.iter_abi_object()
            elif mode == 'UNIT':
                return self.__mode__.iter_unit()
            elif mode == 'ELEMENTS':
                return self.__mode__.iter_elements()
            elif mode == 'ABSTRACT':
                return self.__mode__.iter_abstract()
            else:
                raise AbstractException(f"Unknow mode: ", mode)
    # --------------------------------------------------------------     FOR





    # --------------------------------------------------------------     ( )
        def __call__(self, *args, **kwargs):
            raise AbstractException(f"{repr(self)}.__call__({args}, {kwargs})")
    # --------------------------------------------------------------     ( )





    # --------------------------------------------------------------     []
    # --------------------------------------------------------------     []


    # --------------------------------------------------------------     ==
    # --------------------------------------------------------------     ==


    # --------------------------------------------------------------     +
    # --------------------------------------------------------------     -
    # --------------------------------------------------------------     *
    # --------------------------------------------------------------     /
