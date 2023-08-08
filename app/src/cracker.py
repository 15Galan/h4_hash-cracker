"""
Este script contiene funciones con las que gestionar y procesar hashes.
"""

import hashlib
import sys


def hash_generic(string: str, algo: str) -> str:
    """
    Calcula el hash de una cadena usando un algoritmo determinado.

    :param string:  Cadena a la que se le calculará el hash.
    :param algo:    Algoritmo de hash a usar.

    :return:    Hash de la cadena.
    """
    hasher = hashlib.new(algo)
    
    try:
        hasher.update(string.encode('utf-8'))
        hash = hasher.hexdigest()

    except:
        print(f"Error al calcular el hash '{algo}' de '{string}'.", file=sys.stderr)
        exit(1)
    
    return hash


def crack(hashes: list[str], algorithm: list[str], wordlist: str) -> dict[str, tuple[str, str]]:
    """
    Crackea un hash usando un algoritmo y una lista de palabras determinados.

    :param hashes:      Hashes a crackear.
    :param algorithm:   Algoritmos de hash a usar.
    :param wordlist:    Fichero de palabras a usar.

    :return:    Diccionario con los hashes crackeados.
    """
    with open(wordlist, 'r') as file:       # Leer el fichero de palabras
        words = file.read().splitlines()    # y separarlas por líneas

    cracks = {}     # Estructura del diccionario '{hash: (palabra, algoritmo)}'

    for hash in sorted(hashes):
        for algo in sorted(algorithm):
            for word in words:
                crack = hash_generic(word, algo)    # Hash de la palabra (intento)

                print(f"{hash} : {word}\t({algo})\r", end='')

                if crack == hash:
                    cracks[hash] = (word, algo)     # Almacenar el hash crackeado
                    break

            # Si se encontró un hash, no se necesita probar más algoritmos
            if cracks.get(hash) is not None:
                break

        # Mostrar información del hash tras haber intentado crackearlo
        if cracks.get(hash) is not None:
            print(f'{hash} : {cracks[hash][0]}\t({cracks[hash][1]})')

        else:
            print(f'{hash} * no encontrado')

    return cracks
