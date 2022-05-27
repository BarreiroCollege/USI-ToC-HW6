import re
from abc import ABC
from typing import Any, Dict

from z3 import Bool, And, Implies

__SEARCH_PATTERN = re.compile('[\W_]+')


def str_to_search(s: str) -> str:
    return __SEARCH_PATTERN.sub('', s).lower()


class BaseModel(ABC):
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

    def __lt__(self, o: object):
        if not isinstance(o, BaseModel):
            return 1
        return self._id < o._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BaseModel):
            return False
        return self._id == o._id

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '{}("{}")'.format(self.__class__.__name__, self._name)

    def to_json(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'name': self._name,
        }


class Garment(BaseModel):
    __z_index = None

    def __init__(self, id: int, name: str, z_index: int = None):
        super().__init__(id, name)
        self.__z_index = z_index if z_index is not None else id

    def get_z_index(self) -> int:
        return self.__z_index


class Color(BaseModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)


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

    def __lt__(self, o: object):
        if not isinstance(o, Cloth):
            return 1
        if self.__garment == o.__garment:
            return self.__color < o.__color
        return self.__garment < o.__garment

    def __hash__(self) -> int:
        return hash((self.__garment, self.__color))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Cloth):
            return False
        return self.__garment == o.__garment and self.__color == o.__color

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Cloth("{}", "{}")'.format(self.__garment.get_name(), self.__color.get_name())

    def to_json(self) -> Dict[str, Any]:
        return {
            'garment': self.__garment.to_json(),
            'color': self.__color.to_json(),
            'image': '{}/{}.png'.format(self.__garment.get_search_name(), self.__color.get_search_name()),
            'z_index': self.__garment.get_z_index(),
        }
