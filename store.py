import json
import logging
from pathlib import Path
from typing import Optional, List

from z3 import Solver, Implies, Not, And, sat, Or

from models import Garment, Color, Cloth, str_to_search


class FashionStore:
    __garments, __colors = [], []
    __clothes = []
    __rules = []

    def __init__(self):
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

        for constraint in wardrobe['constraints']:
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

    def add_cloth(self, cloth: Cloth) -> None:
        assert cloth.get_garment() in self.__garments
        assert cloth.get_color() in self.__colors

        if cloth in self.__clothes:
            logging.warning('Cloth("{}", "{}") was already added'
                            .format(cloth.get_garment().get_name(), cloth.get_color().get_name()))
            return
        self.__clothes.append(cloth)

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

            cloth = Cloth(garment, color)
            self.add_cloth(cloth)

    def __has_garment_in_any_cloth(self, garment: Garment) -> bool:
        for cloth in self.__clothes:
            if cloth.get_garment() == garment:
                return True
        return False

    def __get_not_available_garments(self) -> List[Garment]:
        garments = []
        for garment in self.__garments:
            if self.__has_garment_in_any_cloth(garment):
                continue
            garments.append(garment)
        return garments

    def __generate_solver(self) -> Solver:
        solver = Solver()
        for rule in self.__rules:
            solver.add(rule)
        for cloth in self.__clothes:
            solver.add(Or(cloth.to_bool()))
        for garment in self.__get_not_available_garments():
            solver.add(Not(garment.to_bool()))
        return solver

    def dress(self) -> None:
        solver = self.__generate_solver()
        if solver.check() == sat:
            print("Checks")
            print(solver.model())
