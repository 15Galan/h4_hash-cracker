"""
Este script contiene las funciones necesarias para
gestionar y procesar los argumentos de entrada del programa.
"""

import argparse
import hashlib
import sys
import os


def get_args():
    """
    Obtiene los valores para los argumentos de entrada del programa.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    # Argumentos del programa
    parser.add_argument('--hash', metavar='hash', type=str,
                        help='Hash(es) para crackear.')
    parser.add_argument('-a', '--algo', metavar='algoritmo', type=str,
                        help='Algoritmo del hash a crackear.')
    parser.add_argument('-w', '--wordlist', metavar='palabras', type=str,
                        help='Fichero de palabras a usar (posibles valores de un hash).')
    
    return parser.parse_args()


def valid_args(args):
    """
    Comprueba los argumentos de entrada del programa.

    :param args: Argumentos de entrada del programa.
    """
    return (__is_valid_hash(args.hash)
            and __is_valid_algorithm(args.algo)
            and __is_valid_wordlist(args.wordlist))


def __is_valid_hash(hash: str) -> bool:
    """
    Comprueba si un hash es válido.

    :param hash: Hash a comprobar.
    """
    if hash is None:
        print('No se ha especificado un hash.')
        
        return False
    
    # Ligado a la 2ª comprobación de '__is_valid_algorithm()'
    if len(hash) != 32 and len(hash) != 40 and len(hash) != 64:
        print(f"El hash '{hash}' no es válido.", file=sys.stderr)
        print('Los hashes válidos son de 32, 40 y 64 caracteres.', file=sys.stderr)
        
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
