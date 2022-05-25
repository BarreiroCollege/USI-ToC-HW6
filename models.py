import re
from typing import Any, Dict

from z3 import Bool, And, Implies

__SEARCH_PATTERN = re.compile('[\W_]+')


def str_to_search(s: str) -> str:
    return __SEARCH_PATTERN.sub('', s).lower()


class BaseModel:
    _id, _name = None, None
    __bool = None

    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name
        self.__bool = Bool("{}_{}".format(self.__class__.__name__.lower(), id))

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_search_name(self) -> str:
        return str_to_search(self._name)

    def to_bool(self) -> Bool:
        return self.__bool

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '{}("{}")'.format(self.__class__.__name__, self._name)


class Garment(BaseModel):
    __z_index = None

    def __init__(self, id: int, name: str, z_index: int = None):
        super().__init__(id, name)
        self.__z_index = z_index if z_index is not None else id

    def get_z_index(self) -> int:
        return self.__z_index

    def to_json(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'name': self._name,
            'z_index': self.__z_index,
        }


class Color(BaseModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)

    def to_json(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'name': self._name,
        }


class Cloth:
    __garment, __color = None, None
    __bool, __rule = None, None

    def __init__(self, garment: Garment, color: Color):
        self.__garment = garment
        self.__color = color

        self.__bool = Bool('cloth_{}_{}'.format(color.get_search_name(), garment.get_search_name()))
        self.__rule = Implies(self.__bool, And(garment.to_bool(), color.to_bool()))

    def get_garment(self) -> Garment:
        return self.__garment

    def get_color(self) -> Color:
        return self.__color

    def to_bool(self) -> Bool:
        return self.__bool

    def to_rule(self) -> Bool:
        return self.__rule

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Cloth("{}", "{}")'.format(self.__garment.get_name(), self.__color.get_name())

    def to_json(self) -> Dict[str, Any]:
        return {
            'garment': self.__garment.to_json(),
            'color': self.__color.to_json(),
        }
