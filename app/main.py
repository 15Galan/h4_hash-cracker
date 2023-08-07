#!/bin/python


from src import input
from src import cracker


def main():
    """
    Función principal del programa.
    """
    args = input.get_args()

    cracked = cracker.crack(args['hashes'], args['algorithms'], args['words'])

    if cracked is None:
        print('No se encontró un hash para la lista de palabras.')

    if args['invalid_hashes']:
        print()
        for hash in args['invalid_hashes']:
            print(f"{hash} - inválido")


if __name__ == '__main__':
    """
    Punto de entrada al ejecutarse como programa.
    """
    try:
        main()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)
        exit(1)

    exit(0)
