"""
Este script contiene las funciones necesarias para
gestionar y procesar los argumentos de entrada del programa.
"""

import argparse
import hashlib
import sys
import os


def __get_input():
    """
    Obtiene los valores para los argumentos de entrada del programa.
    """
    parser = argparse.ArgumentParser(description='Cracker simple de hashes.')
    
    # Argumentos del programa
    parser.add_argument('-hl', '--hashlist', metavar='lista de hashes', type=str, nargs='+',
                        help='Lista de hashes para crackear.')
    parser.add_argument('-hf', '--hashfile', metavar='fichero de hashes', type=str,
                        help='Fichero con hashes para crackear.')
    parser.add_argument('-ag', '--algorithm', metavar='algoritmo', type=str,
                        help='Algoritmo del hash a crackear.')
    parser.add_argument('-wl', '--wordlist', metavar='palabras', type=str,
                        help='Fichero de palabras a usar (posibles valores de un hash).')
    
    return parser.parse_args()


def get_args():
    args = __get_input()

    if not __valid_args(args):
        exit(1)

    return {'hashes': __merge_hashes(args.hashlist, args.hashfile),
            'algorithm': args.algorithm,
            'wordlist': args.wordlist}


def __valid_args(args):
    """
    Comprueba los argumentos de entrada del programa.

    :param args: Argumentos de entrada del programa.
    """
    return ((__is_valid_hashlist(args.hashlist)
            or __is_valid_hashfile(args.hashfile))
            and __is_valid_algorithm(args.algorithm)
            and __is_valid_wordlist(args.wordlist))


def __is_valid_hashlist(hashes: str) -> bool:
    """
    Comprueba si una lista de hashes es válida.

    :param hashes: Lista de hashes a comprobar.
    """
    if hashes is None:
        print('No se ha especificado ningún hash.')

        return False
    
    # Ligado a la 2ª comprobación de '__is_valid_algorithm()'
    hashes_aux = hashes.copy()

    for hash in hashes_aux:
        if len(hash) != 32 and len(hash) != 40 and len(hash) != 64:
            print(f"{hash} : inválido", file=sys.stderr)

            hashes.remove(hash)

    if 0 < len(hashes):
        return True

    else:
        print('\nNingún hash es válido.', file=sys.stderr)

        return False


def __is_valid_hashfile(file: str) -> bool:
    """
    Comprueba si una lista de hashes contiene al menos un hash válido.

    :param hash: Hash a comprobar.
    """
    if file is None:
        print('No se ha especificado un fichero de hashes.')

        return False

    if not os.path.isfile(file):
        print(f"El fichero '{file}' no existe.", file=sys.stderr)

        return False
    
    return True
    
    
def __is_valid_algorithm(algo: str) -> bool:
    """
    Comprueba si un algoritmo de hash es válido.

    :param algo: Algoritmo de hash a comprobar.
    """
    if algo is None:
        print('No se ha especificado un algoritmo de hash.')
        
        return False
    
    if algo not in ['md5', 'sha1', 'sha256']:
        print(f"El algoritmo '{algo}' no es válido.", file=sys.stderr)
        print(f"Algoritmos válidos: {hashlib.algorithms_guaranteed}.", file=sys.stderr)
        
        return False
    
    return True


def __is_valid_wordlist(wordlist: str) -> bool:
    """
    Comprueba si un fichero de palabras es válido.

    :param wordlist: Fichero de palabras a comprobar.
    """
    if wordlist is None:
        print('No se ha especificado un fichero de palabras.', file=sys.stderr)
        
        return False
    
    if not os.path.isfile(wordlist):
        print(f"El fichero '{wordlist}' no existe.", file=sys.stderr)
        
        return False
    
    return True


def __merge_hashes(hashlist: list, hashfile: str) -> list:
    """
    Combina los hashes de una lista literal con los de un fichero.

    :param hashlist:    Lista de hashes.
    :param hashfile:    Fichero de hashes.
    """
    if hashlist is None:
        hashlist = []

    if hashfile is None:
        return hashlist

    with open(hashfile, 'r') as f:
        hashes = [line.strip() for line in f]

    for hash in hashes:
        hashlist.append(hash)

    return hashlist
