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
    parser.add_argument('-hf', '--hashfile', metavar='fichero de hashes', type=os.path.abspath,
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


def __is_valid_hash(hash: str) -> bool:
    """
    Comprueba si un hash es válido.
    Se considera válido

    :param hash: Hash a comprobar.
    """
    # Longitudes de los hashes garantizados (hashlib.algorithms_guaranteed)
    guaranteed_len = [32, 40, 48, 56, 64, 96, 128]
    hexademical = '0123456789abcdefABCDEF'

    if len(hash) not in guaranteed_len and not all(c in hexademical for c in hash):
        print(f"{hash} : inválido", file=sys.stderr)
        return False

    return True


def __is_valid_hashlist(hashes: list[str]) -> bool:
    """
    Comprueba si una lista de hashes contiene al menos un hash válido.

    :param hashes: Lista de hashes a comprobar.
    """
    if hashes is None:
        print('No se ha especificado ningún hash.', file=sys.stderr)
        return False

    if any(__is_valid_hash(hash) for hash in hashes):
        return True


def __is_valid_hashfile(file: str) -> bool:
    """
    Comprueba si un fichero con hashes contiene al menos un hash válido.

    :param hash: Hash a comprobar.
    """
    if file is None:
        print('No se ha especificado un fichero de hashes.', file=sys.stderr)
        return False

    if not os.path.isfile(file):
        print(f"El fichero '{file}' no existe.", file=sys.stderr)
        return False

    with open(file, 'r') as f:
        hashes = f.read().splitlines()

    if any(__is_valid_hash(hash) for hash in hashes):
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


def __merge_hashes(hashlist: list[str], hashfile: str) -> set[str]:
    """
    Combina los hashes de una lista literal con los de un fichero.

    :param hashlist:    Lista de hashes.
    :param hashfile:    Fichero de hashes.
    """
    if hashlist is not None and hashfile is not None:
        list_hashes = set(hashlist)

        with open(hashfile, 'r') as f:
            file_hashes = set(f.read().splitlines())

    return list_hashes.union(file_hashes)
