import itertools
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from z3 import Solver, sat, Implies, Not, And, Or

from models import Garment, Color, Cloth, str_to_search


class FashionStore:
    __garments: List[Garment] = []
    __colors: List[Color] = []
    __clothes: Dict[Garment, List[Color]] = {}
    __rules = []

    def __init__(self):
        self.__garments = []
        self.__colors = []
        self.__clothes = {}
        self.__rules = []

        self.__parse_wardrobe()

    def __parse_wardrobe(self) -> None:
        wardrobe_json = Path().joinpath("data").joinpath("wardrobe.json").absolute()
        assert wardrobe_json.exists() and wardrobe_json.is_file()

        with open(wardrobe_json, "r") as f:
            wardrobe = json.loads(f.read())

        for i, garment in enumerate(wardrobe['garments']):
            g = Garment(i, garment)
            self.__garments.append(g)
        for i, color in enumerate(wardrobe['colors']):
            c = Color(i, color)
            self.__colors.append(c)

        self.__parse_constraints(wardrobe['constraints'])

    def __parse_constraints(self, constraints: List[Dict[str, Any]]):
        for constraint in constraints:
            t, o, values = constraint['type'], constraint['object'], constraint['values']
            if t not in ['not', 'implies']:
                logging.warning('Constraint "{}" is not defined, skipping...'.format(t))
                continue
            if o not in ['garment', 'color']:
                logging.warning('Object "{}" could not be recognized, skipping...'.format(o))
                continue

            for value in values:
                if o == "garment":
                    value = [self.__search_garment(v) for v in value]
                elif o == "color":
                    value = [self.__search_color(v) for v in value]

                if None in value:
                    logging.warning('Constraint "{}" for object "{}" has unrecognized values, skipping...'
                                    .format(t, o))
                    continue

                rule = None
                if t == 'implies':
                    if len(value) != 2:
                        logging.warning('Value [{}] is not of length 2 for constraint "{}" for object "{}", skipping...'
                                        .format(str(value), t, o))
                        continue
                    rule = Implies(value[0].to_bool(), value[1].to_bool())
                elif t == 'not':
                    rule = Not(And([v.to_bool() for v in value]))

                if rule is not None:
                    self.__rules.append(rule)

    def add_cloth(self, garment: Garment, color: Color) -> None:
        assert garment in self.__garments
        assert color in self.__colors

        if garment not in self.__clothes:
            self.__clothes[garment] = []

        if color in self.__clothes[garment]:
            logging.warning('Garment "{}" with color "{}" was already added'
                            .format(garment.get_name(), color.get_name()))
            return
        self.__clothes[garment].append(color)

    def __search_garment(self, g: str) -> Optional[Garment]:
        g = str_to_search(g)
        for garment in self.__garments:
            if garment.get_search_name() == g:
                return garment
        return None

    def __search_color(self, c: str) -> Optional[Color]:
        c = str_to_search(c)
        for color in self.__colors:
            if color.get_search_name() == c:
                return color
        return None

    def parse_clothes(self, data: str) -> None:
        lines = data.strip().split("\n")
        for line in lines:
            line = line.strip()
            splitted = line.split(",")
            if len(splitted) != 2:
                continue

            g, c = splitted
            garment = self.__search_garment(g.strip())
            color = self.__search_color(c.strip())

            if garment is None:
                logging.warning("Garment {} is not available in the wardrobe".format(g))
                continue
            if color is None:
                logging.warning("Color {} is not available in the wardrobe".format(c))
                continue

            self.add_cloth(garment, color)

    @staticmethod
    def __get_used_garments(clothes: List[Cloth]) -> List[Garment]:
        return list(set([cloth.get_garment() for cloth in clothes]))

    @staticmethod
    def __get_used_colors(clothes: List[Cloth]) -> List[Color]:
        return list(set([cloth.get_color() for cloth in clothes]))

    def __generate_possible_dressing(self) -> List[List[Cloth]]:
        garment, colors = zip(*self.__clothes.items())
        perms = [dict(zip(garment, v)) for v in itertools.product(*colors)]

        dressings = []
        for perm in perms:
            dressing = []
            for garment, color in perm.items():
                dressing.append(Cloth(garment, color))
            dressings.append(dressing)
        return dressings

    def __generate_solver(self, clothes: List[Cloth]) -> Solver:
        solver = Solver()

        for rule in self.__rules:
            solver.add(rule)
        for cloth in clothes:
            solver.add(cloth.to_rule())

        for garment in FashionStore.__get_used_garments(clothes):
            cs = list(filter(lambda c: c.get_garment() == garment, clothes))
            solver.add(Implies(
                garment.to_bool(),
                Or([c.to_bool() for c in cs])
            ))
        for color in FashionStore.__get_used_colors(clothes):
            cs = list(filter(lambda c: c.get_color() == color, clothes))
            solver.add(Implies(
                color.to_bool(),
                Or([c.to_bool() for c in cs])
            ))

        solver.add(Or([cloth.to_bool() for cloth in clothes]))
        return solver

    def dress(self) -> List[List[Cloth]]:
        dresses = []
        for dressing in self.__generate_possible_dressing():
            solver = self.__generate_solver(dressing)
            result = solver.check()

            if result != sat:
                continue
            model = solver.model()

            dress = []
            for cloth in dressing:
                if model.eval(cloth.to_bool()):
                    dress.append(cloth)
            dresses.append(dress)

        dresses.sort()
        dresses = list(d for d, _ in itertools.groupby(dresses))
        return dresses
