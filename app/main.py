#!/bin/env python3.9

import sys

from src import input
from src import cracker


def main():
    """
    Función principal del programa.
    """
    args = input.get_args()

    if args['hashes_ko']:
        print('\nHashes inválidos:')
        print('\n'.join(args['hashes_ko']))

    if args['algorithms_ko']:
        print('\nAlgoritmos inválidos:')
        print(', '.join(args['algorithms_ko']))

    if args['hashes_ok'] or args['algorithms_ok']:
        cracked = cracker.crack(args['hashes_ok'], args['algorithms_ok'], args['words'])

        if cracked is None:
            print('No se encontró un hash para la lista de palabras.')


if __name__ == '__main__':
    """
    Punto de entrada al ejecutarse como programa.
    """
    try:
        main()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    exit(0)
