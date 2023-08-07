"""
Este script contiene las funciones necesarias para
gestionar y procesar los argumentos de entrada del programa.
"""

import argparse
import hashlib
import sys
import os


def _get_input():
    """
    Obtiene los valores para los argumentos de entrada del programa.
    """
    parser = argparse.ArgumentParser(description='Cracker simple de hashes.')
    
    # Argumentos del programa
    parser.add_argument('-hl', '--hashlist', metavar='hash', type=str, nargs='+',
                        help='Lista de hashes para crackear.')
    parser.add_argument('-hf', '--hashfile', metavar='hashfile', type=os.path.abspath,
                        help='Fichero con hashes para crackear.')
    parser.add_argument('-ag', '--algorithm', metavar='algoritmo', type=str,
                        help='Algoritmo del hash a crackear.')
    parser.add_argument('-wl', '--wordlist', metavar='palabras', type=os.path.abspath,
                        help='Fichero con posibles valores de un hash.')
    
    return parser.parse_args()


def get_args():
    """
    Obtiene los argumentos de entrada del programa si estos son válidos,
    junto a otros datos adicionales para mejorar el funcionamiento del programa.
    Combina los hashes de un fichero y de una lista en un único objeto.
    Añade un nuevo valor para aquellos hashes que no sean válidos.

    :return:    Diccionario con los argumentos de entrada del programa.
    """
    args = _get_input()

    if not _valid_args(args):
        exit(1)

    # Procesar todos los hashes de los argumentos
    (good, bad) = separate_hashes(_merge_hashes(args.hashlist, args.hashfile))

    return {'hashes': good,
            'algorithms': args.algorithm,
            'words': args.wordlist,
            'invalid_hashes': bad}


def _valid_args(args):
    """
    Comprueba los argumentos de entrada del programa.

    :param args:    Argumentos de entrada del programa.
    """
    return ((_is_valid_hashlist(args.hashlist)
             or _is_valid_hashfile(args.hashfile))
            and _is_valid_algorithm(args.algorithm)
            and _is_valid_wordlist(args.wordlist))


def _is_valid_hash(hash: str) -> bool:
    """
    Comprueba si un hash es válido.
    Se considera válido

    :param hash:    Hash a comprobar.

    :return:    True si el hash es válido;
                False en caso contrario.
    """
    # Longitudes de los hashes garantizados (hashlib.algorithms_guaranteed)
    guaranteed_len = [32, 40, 48, 56, 64, 96, 128]
    hexademical = '0123456789abcdefABCDEF'

    if len(hash) not in guaranteed_len or not all(c in hexademical for c in hash):
        return False

    return True


def _is_valid_hashlist(hashes: list[str]) -> bool:
    """
    Comprueba si una lista de hashes contiene al menos un hash válido.

    :param hashes: Lista de hashes a comprobar.

    :return:    True si la lista contiene al menos un hash válido;
                False en caso contrario.
    """
    if hashes is None:
        print('No se ha especificado ningún hash.', file=sys.stderr)
        return False

    if not any(_is_valid_hash(hash) for hash in hashes):
        print('No hay ningún fichero válido en la lista proporcionada.', file=sys.stderr)
        return False

    return True


def _is_valid_hashfile(file: str) -> bool:
    """
    Comprueba si un fichero con hashes contiene al menos un hash válido.

    :param hash: Hash a comprobar.

    :return:    True si el fichero contiene al menos un hash válido;
                False en caso contrario.
    """
    if file is None:
        print('No se ha especificado un fichero de hashes.', file=sys.stderr)
        return False

    if not os.path.isfile(file):
        print(f"El fichero '{file}' no existe.", file=sys.stderr)
        return False

    with open(file, 'r') as f:
        hashes = f.read().splitlines()

    if not any(_is_valid_hash(hash) for hash in hashes):
        print('No hay ningún hash válido en el fichero proporcionado.', file=sys.stderr)
        return False

    return True
    
    
def _is_valid_algorithm(algo: str) -> bool:
    """
    Comprueba si un algoritmo de hash es válido.

    :param algo: Algoritmo de hash a comprobar.

    :return:    True si el algoritmo es válido;
                False en caso contrario.
    """
    if algo is None:
        print('No se ha especificado un algoritmo de hash.')
        
        return False
    
    if algo not in ['md5', 'sha1', 'sha256']:
        print(f"El algoritmo '{algo}' no es válido.", file=sys.stderr)
        print(f"Algoritmos válidos: {hashlib.algorithms_guaranteed}.", file=sys.stderr)
        
        return False
    
    return True


def _is_valid_wordlist(wordlist: str) -> bool:
    """
    Comprueba si un fichero de palabras es válido.

    :param wordlist: Fichero de palabras a comprobar.

    :return:    True si el fichero es válido;
                False en caso contrario.
    """
    if wordlist is None:
        print('No se ha especificado un fichero de palabras.', file=sys.stderr)
        
        return False
    
    if not os.path.isfile(wordlist):
        print(f"El fichero '{wordlist}' no existe.", file=sys.stderr)
        
        return False
    
    return True


def _merge_hashes(hashlist: list[str], hashfile: str) -> set[str]:
    """
    Combina los hashes de una lista literal con los de un fichero.

    :param hashlist:    Lista de hashes.
    :param hashfile:    Fichero de hashes.

    :return:            Unión de los hashes de la lista y el fichero.
    """
    if hashlist is not None and hashfile is not None:
        list_hashes = set(hashlist)

        with open(hashfile, 'r') as f:
            file_hashes = set(f.read().splitlines())

    return list_hashes.union(file_hashes)


def separate_hashes(hashes: set[str]) -> (set[str], set[str]):
    """
    Filtra los hashes válidos de un conjunto de hashes.

    :param hashes: Hashes a filtrar.

    :return:    Tupla con 2 conjuntos de hashes: válidos e inválidos.
    """
    valids = [hash for hash in hashes if _is_valid_hash(hash)]
    invalids = hashes.difference(valids)

    return valids, invalids
