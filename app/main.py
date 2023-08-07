#!/bin/python


from src import input
from src import hash_functions


def main():
    """
    Función principal del programa.
    """
    args = input.get_args()

    if not input.valid_args(args):
        exit(1)

    cracked = hash_functions.crack(args.hash, args.algo, args.wordlist)

    if cracked is None:
        print('No se encontró un hash para la lista de palabras.')


if __name__ == '__main__':
    """
    Punto de entrada al ejecutarse como programa.
    """
    main()

    exit(0)
