from subjects import subject, place
from digital_assistant import digital_assistant
"""
Setup for trying the dialogue system, it creates an assistant loads the data
into the assistant and the initalizes a dialogue
"""


def main():
    mArIa = setup_digital_assistant()
    mArIa.initalize_dialogue()


"""
Setup function for the digital assistant
"""


def setup_digital_assistant():
    mArIa = digital_assistant(name='mArIa')

    mArIa.add_subject(import_resturants())
    mArIa.add_subject(import_shops())
    mArIa.add_subject(import_post_offices())

    return mArIa


"""
The data for the subject shops
"""


def import_shops():
    shops = subject(name='Shops', tags=['purchase', 'buy', 'shop', 'store'])

    shops.add_place(
        place(name='Filur',
              tags=['kid', 'clothes', 'toys'],
              price=2,
              opening=10,
              closing=18))

    shops.add_place(
        place(name='So Sweet',
              tags=['candy', 'cigaretts', 'smoke', 'snus'],
              price=3,
              opening=10,
              closing=20))

    shops.add_place(
        place(name='Majornas saker från förr',
              tags=['antique', 'lamps', 'furniture', 'second hand'],
              price=3,
              opening=12,
              closing=18))

    return shops


"""
The data for the subject resturnats
"""


def import_resturants():
    resturant = subject(name='Resturants',
                        tags=['drink', 'eat', 'resturant', 'food'])
    resturant.add_place(
        place(name='The Red Lion',
              tags=['beer', 'burger', 'english'],
              price=2,
              opening=16,
              closing=22))

    resturant.add_place(
        place(name='Tullen',
              tags=['fish', 'meat', 'potatoes', 'swedish', 'cosy', 'beer'],
              price=2,
              opening=16,
              closing=1))

    resturant.add_place(
        place(name='Tapasbaren',
              tags=['tapas', 'spanish', 'wine', 'cosy'],
              price=3,
              opening=17,
              closing=20))

    resturant.add_place(
        place(name='Korv Kiosk',
              tags=['sausage', 'mashed potatoes', 'simple'],
              price=1,
              opening=10,
              closing=20))

    return resturant


"""
The data for the subject post offices
"""


def import_post_offices():
    post_office = subject(name='Post offices',
                          tags=['mail', 'package', 'pick'])

    post_office.add_place(
        place(name='Maria Livs',
              tags=['Post nord', 'food', 'store'],
              price=2,
              opening=9,
              closing=22))

    post_office.add_place(
        place(name='Pressbyrån',
              tags=['Schenker', 'coffe', 'bun', 'buns', 'cake', 'cakes'],
              price=3,
              opening=7,
              closing=23))

    post_office.add_place(
        place(name='So Sweet',
              tags=['DHL', 'candy', 'snus', 'cigarettes'],
              price=3,
              opening=10,
              closing=20))

    return post_office


if __name__ == "__main__":
    main()
