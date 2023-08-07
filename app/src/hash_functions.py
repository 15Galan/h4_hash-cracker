"""
Este script contiene funciones con las que gestionar y procesar hashes.
"""

import hashlib
import sys


def hash_md5(string: str) -> str:
    """
    Calcula el hash de una cadena usando el algoritmo MD5.

    :param string: Cadena a la que se le calculará el hash.
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def hash_sha1(string: str) -> str:
    """
    Calcula el hash de una cadena usando el algoritmo SHA1.

    :param string: Cadena a la que se le calculará el hash.
    """
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def hash_sha256(string: str) -> str:
    """
    Calcula el hash de una cadena usando el algoritmo SHA256.

    :param string: Cadena a la que se le calculará el hash.
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def hash_any(string: str, algo: str) -> str:
    """
    Calcula el hash de una cadena usando un algoritmo determinado.

    :param string:  Cadena a la que se le calculará el hash.
    :param algo:    Algoritmo de hash a usar.
    """
    hasher = hashlib.new(algo)
    
    try:
        hasher.update(string.encode('utf-8'))
        hash = hasher.hexdigest()

    except:
        print(f"Error al calcular el hash '{algo}' de '{string}'.", file=sys.stderr)
        exit(1)
    
    return hash


def crack(hashes: list, algorithm: str, wordlist: str) -> dict[str, str]:
    """
    Crackea un hash usando un algoritmo y una lista de palabras determinados.

    :param hashes:      Hashes a crackear.
    :param algorithm:   Algoritmo de hash a usar.
    :param wordlist:    Fichero de palabras a usar.
    """
    with open(wordlist, 'r') as file:       # Leer el fichero de palabras
        words = file.read().splitlines()    # y separarlas por líneas

    cracks = {}

    for hash in hashes:
        for word in words:
            crack = hash_any(word, algorithm)

            print(f"{hash} : {word}\r", end='')

            if crack == hash:
                cracks[hash] = word
                break

        if cracks.get(hash) is not None:
            print(f'{hash} : {cracks[hash]}')

        else:
            print(f'{hash} : no encontrado')

    return cracks
