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
                        help='hash(es) to crack')
    parser.add_argument('-hf', '--hashfile', metavar='hashfile', type=os.path.abspath,
                        help='file with hashes to crack')
    parser.add_argument('-ag', '--algolist', metavar='algorithm', type=str, nargs='+',
                        help='algorithm(s) to crack the hashes')
    parser.add_argument('-wl', '--wordlist', metavar='wordlist', type=os.path.abspath,
                        help='file with possible values of a hash')
    
    return parser.parse_args()


def _normalize_input(args):
    """
    Normaliza los argumentos de entrada del programa.

    :param args:    Argumentos de entrada del programa.

    :return:    Argumentos de entrada normalizados.
    """
    if args.hashlist is not None:
        args.hashlist = [hash.lower() for hash in args.hashlist]

    if args.algolist is not None:
        args.algolist = [algo.lower() for algo in args.algolist]

    return args


def get_args():
    """
    Obtiene los argumentos de entrada del programa si estos son válidos,
    junto a otros datos adicionales para mejorar el funcionamiento del programa.
    Combina los hashes de un fichero y de una lista en un único objeto.
    Añade un nuevo valor para aquellos hashes que no sean válidos.

    :return:    Diccionario con los argumentos de entrada del programa.
    """
    args = _normalize_input(_get_input())

    if not _valid_args(args):
        exit(1)

    # Procesar todos los hashes y algoritmos de los argumentos
    good_hashes, bad_hashes = separate_hashes(_merge_hashes(args.hashlist, args.hashfile))
    good_algorithms, bad_algorithms = separate_algorithms(args.algolist)

    return {'hashes_ok': good_hashes,
            'hashes_ko': bad_hashes,
            'algorithms_ok': good_algorithms,
            'algorithms_ko': bad_algorithms,
            'words': get_words(args.wordlist)}


def _valid_args(args):
    """
    Comprueba los argumentos de entrada del programa.

    :param args:    Argumentos de entrada del programa.
    """
    return (_are_valid_hashes(args.hashlist, args.hashfile)
            and _is_valid_algolist(args.algolist)
            and _is_valid_wordlist(args.wordlist))


def _is_valid_hash(hash: str) -> bool:
    """
    Comprueba si un hash es válido, siendo válido si tiene una longitud
    acorde al resultado de algún algoritmo de hash y si está en hexadecimal.

    Se usan los algoritmos garantizados por hashlib.

    :param hash:    Hash.

    :return:    True si el hash es válido;
                False en caso contrario.
    """
    # Longitudes de los hashes garantizados (hashlib.algorithms_guaranteed)
    guaranteed_len = [32, 40, 48, 56, 64, 96, 128]
    hexadecimal = '0123456789abcdefABCDEF'

    if len(hash) not in guaranteed_len or not all(c in hexadecimal for c in hash):
        return False

    return True


def _is_valid_hashlist(hashes: list[str]) -> bool:
    """
    Comprueba si una lista de hashes contiene al menos un hash válido.

    :param hashes:  Lista de hashes.

    :return:    True si la lista contiene al menos un hash válido;
                False en caso contrario.
    """
    if not any(_is_valid_hash(hash) for hash in hashes):
        print('No hay ningún hash válido en la lista proporcionada.', file=sys.stderr)
        return False

    return True


def _is_valid_hashfile(file: str) -> bool:
    """
    Comprueba si un fichero con hashes contiene al menos un hash válido.

    :param file:    Fichero con hashes.

    :return:    True si el fichero contiene al menos un hash válido;
                False en caso contrario.
    """
    if not os.path.isfile(file):
        print(f"El fichero '{file}' no existe.", file=sys.stderr)
        return False

    # Abrir el fichero para validar su contenido
    with open(file, 'r') as f:
        hashes = f.read().splitlines()

    if not any(_is_valid_hash(hash) for hash in hashes):
        print('No hay ningún hash válido en el fichero proporcionado.', file=sys.stderr)
        return False

    return True


def _are_valid_hashes(hashes: list[str], file: str) -> bool:
    """
    Comprueba si una lista de hashes y un fichero de hashes contienen al menos
    un hash válido.

    :param hashes:  Lista de hashes.
    :param file:    Fichero con hashes.

    :return:    True si la lista o el fichero contienen al menos un hash válido;
                False en caso contrario.
    """
    _list, _file = True, True

    # No se ha especificado ningún hash (ni lista, ni fichero)
    if hashes is None and file is None:
        print('No se ha especificado ningún hash.', file=sys.stderr)
        return False

    # Se ha especificado uno o más hashes (lista o fichero)
    if hashes:
        _list = _is_valid_hashlist(hashes)

        if not _list and file is None:
            print('La lista no contiene hashes válidos.', file=sys.stderr)

    if file:
        _file = _is_valid_hashfile(file)

        if not _file and hashes is None:
            print('El fichero no contiene hashes válidos.', file=sys.stderr)

    return _list or _file


def _is_valid_algorithm(algorithm: str) -> bool:
    """
    Comprueba si un algoritmo de hash es válido, siendo válido si está
    garantizado por hashlib.

    :param algorithm:   Algoritmo de hash.

    :return:    True si el algoritmo es válido;
                False en caso contrario.
    """
    # Comparación en minúsculas para evitar errores
    return algorithm.lower() in [a.lower() for a in hashlib.algorithms_guaranteed]

    
def _is_valid_algolist(algolist: list[str]) -> bool:
    """
    Comprueba si una lista de algoritmos de hash contiene al menos un algoritmo válido.

    :param algolist:    Lista de algoritmos.

    :return:    True si la lista contiene al menos un algoritmo válido;
                False en caso contrario.
    """
    if algolist is None:
        print('No se ha especificado un algoritmo de hash.')
        return False

    if not any(_is_valid_algorithm(algorithm) for algorithm in algolist):
        print('No hay ningún algoritmo válido en la lista proporcionada.', file=sys.stderr)
        return False
    
    return True


def _is_valid_wordlist(wordlist: str) -> bool:
    """
    Comprueba si un fichero de palabras es válido.

    :param wordlist:    Fichero de palabras a comprobar.

    :return:    True si el fichero es válido;
                False en caso contrario.
    """
    if wordlist is None:
        print('No se ha especificado un fichero de palabras.', file=sys.stderr)
        return False
    
    if not os.path.isfile(wordlist):
        print(f"El fichero '{wordlist}' no existe.", file=sys.stderr)
        return False

    # Abrir el fichero para validar su contenido
    with open(wordlist, 'r') as f:
        words = f.read().splitlines()

    if len(words) == 0:
        print(f"El fichero '{wordlist}' está vacío.", file=sys.stderr)
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
        hashes = set(hashlist)

        with open(hashfile, 'r') as f:
            file_hashes = set(f.read().splitlines())

    return hashes.union(file_hashes)


def separate_hashes(hashes: set[str]) -> (set[str], set[str]):
    """
    Filtra los hashes válidos de un conjunto de hashes.

    :param hashes: Hashes a filtrar.

    :return:    Tupla con 2 conjuntos de hashes: válidos e inválidos.
    """
    valids = set([h for h in hashes if _is_valid_hash(h)])
    invalids = hashes.difference(valids)

    return valids, invalids


def separate_algorithms(algorithms: list[str]) -> (set[str], set[str]):
    """
    Filtra los algoritmos válidos de una lista de algoritmos.

    :param algorithms:  Algoritmos a filtrar.

    :return:    Tupla con 2 conjuntos de algoritmos: válidos e inválidos.
    """
    valids = set([a for a in algorithms if _is_valid_algorithm(a)])
    invalids = set(algorithms).difference(valids)

    return valids, invalids


def get_words(wordlist: str) -> set[str]:
    """
    Obtiene las palabras de un fichero de palabras.
    Elimina las palabras repetidas.

    :param wordlist:    Fichero de palabras.

    :return:    Conjunto de palabras.
    """
    with open(wordlist, 'r') as f:
        words = f.read().splitlines()

    return set(words)
