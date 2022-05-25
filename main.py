import logging

from store import FashionStore


def demo():
    store = FashionStore()
    with open('data/example.txt', 'r') as f:
        store.parse_clothes(f.read())
    dresses = store.dress()
    for dress in dresses:
        print(dress)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s | %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    demo()
