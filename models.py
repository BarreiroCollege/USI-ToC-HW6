import re

from z3 import Bool, And

__SEARCH_PATTERN = re.compile('[\W_]+')


def str_to_search(s: str) -> str:
    return __SEARCH_PATTERN.sub('', s)


class Garment:
    __id, __name = None, None
    __bool = None

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
        self.__bool = Bool("g_{}".format(self.__id))

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_search_name(self) -> str:
        return str_to_search(self.__name)

    def to_bool(self) -> Bool:
        return self.__bool

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Garment("{}")'.format(self.__name)


class Color:
    __id, __name = None, None
    __bool = None

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
        self.__bool = Bool("c_{}".format(self.__id))

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_search_name(self) -> str:
        return str_to_search(self.__name)

    def to_bool(self) -> Bool:
        return self.__bool

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Color("{}")'.format(self.__name)


class Cloth:
    __garment, __color = None, None
    __bool = None

    def __init__(self, garment: Garment, color: Color):
        self.__garment = garment
        self.__color = color
        self.__bool = And(garment.to_bool(), color.to_bool())

    def get_garment(self) -> Garment:
        return self.__garment

    def get_color(self) -> Color:
        return self.__color

    def to_bool(self) -> Bool:
        return self.__bool

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Cloth("{}", "{}")'.format(self.__garment.get_name(), self.__color.get_name())
