<div align="center">
    <img src=".github/readme/h4cking-pro light.png#gh-light-mode-only" alt="H4 logo (claro)" width="450" />
    <img src=".github/readme/h4cking-pro dark.png#gh-dark-mode-only" alt="H4 logo (oscuro)" width="450" />
    <p>
        Un programa simple para <i>crackear</i> hashes
    <p>
</div>


# Descripción

Este es un programa orientado a la obtención de elementos a partir de hashes.

## Características

- Crackeo de hashes con algoritmos garantizados por el módulo `hashlib`.
- Acepta hashes de distintos formatos a la vez, junto a distintos algoritmos.
- Acepta entrada de hashes mediante lista de cadenas, fichero, o ambas a la vez.
- Identificación de hashes válidos e inválidos.
- Identificación de algoritmos válidos e inválidos.
- Ejecución minimalista: solo se procesan los datos válidos.

> **Note**  
> Un hash se considera válido si cumple estas 2 condiciones:  
> - Su longitud es la de algún resultado de los algoritmos garantizados por el módulo `hashlib` (comprobable con `hashlib.algorithms_guaranteed`).
> - Sus caracteres son exclusivamente hexadecimales.
>   
> Un algoritmo se considera válido si está garantizado por el módulo `hashlib` (comprobable con `hashlib.algorithms_guaranteed`).

# Instalación

1. Instalar [Python 3.9](https://www.python.org/downloads) (mínimo).
2. Clonar el repositorio.
3. Instalar las dependencias (`pip install -r requirements.txt`).


# Ejecución

Este script puede usarse como un comando de terminal o con `python3.9`.

Otorga permisos de ejecución al script principal `main.py` y el sistema lo ejecutará con el intérprete de Python:

```shell
sudo chmod +x app/main.py
```

A partir de aquí, puedes consultar la ayuda con la opción `-h` o `--help`:

```shell
./app/main.py -h
```

```
usage: main.py [-h] [-hl hash [hash ...]] [-hf hashfile] [-ag algorithm [algorithm ...]]
               [-wl wordlist]

Cracker simple de hashes.

optional arguments:
  -h, --help            show this help message and exit
  -hl hash [hash ...], --hashlist hash [hash ...]
                        hash(es) to crack
  -hf hashfile, --hashfile hashfile
                        file with hashes to crack
  -ag algorithm [algorithm ...], --algolist algorithm [algorithm ...]
                        algorithm(s) to crack the hashes
  -wl wordlist, --wordlist wordlist
                        file with possible values of a hash
```

También es posible usarlo como un módulo de Python de la forma habitual:

```shelll
python3.9 app/main.py <args>
```

## Ejemplo

```shell
./app/main.py -hl 1D616F28163414582BA7E2EB400485B9 d616f28163414582ba7e2eb400485b9 c06ed8affb5cdfab49fd531429fe1929 358169735b397d125511972057478501 2378648237 32485725dshjfg -hf hashes.txt -ag md5 md8 sha1 MD5 sha420 sha256 -wl h4ckingyou.txt
```

```text
Hashes inválidos:
d616f28163414582ba7e2eb400485b9
2378648237
32485725dshjfg

Algoritmos inválidos:
md8, sha420

Hashes válidos:
1d616f28163414582ba7e2eb400485b9 : srgalan  (md5)
358169735b397d125511972057478501 * no encontrado
7b4bf604ff3032c625532a803eaedddc : H4CKINGPRO   (md5)
c06ed8affb5cdfab49fd531429fe1929 : sleepy_rafa  (md5)
e772e0266541435a1b52df6bb498cb62e6749c95e59b580d71c9fb16b4125af9 : srgalan  (sha256)
```

## Argumentos

El proyecto funciona con 4 tipos de argumentos distintos, pero si no se proporciona ninguno, su comportamiento por defecto es mostrar la ayuda (equivalente a `./main.py -h`).

> **Note**  
> Los argumentos `-hl` y `-hf` son compatibles entre sí y de hecho, cumplen la misma función:
> definir los hashes a crackear. Si se proporcionan ambos, se combinarán en un único dato.

### `-hl` / `--hashlist`

El programa recibe una una lista de hashes como argumento de entrada y comprueba que haya al menos un hash válido para poder operar.

Si todo es correcto, se procederá a intentar crackear cada hash válido de la lista.

### `-hf` / `--hashfile`

El programa recibe un fichero de texto con hashes como argumento de entrada y comprueba que el fichero sea accesible y que haya al menos un hash válido para poder operar.

Si todo es correcto, se procederá a intentar crackear cada hash válido del fichero.

### `-ag` / `--algorithms`

El programa recibe una lista de algoritmos como argumento de entrada y comprueba que haya al menos un algoritmo válido para poder operar.

Si todo es correcto, se procederá a intentar crackear cada hash válido de los argumentos anteriores con cada algoritmo válido de la lista.

### `-wl` / `--wordlist`

El programa recibe un archivo de texto con posibles valores de un hash como argumento de entrada y comprueba que el fichero sea accesible y tenga contenido.

Si todo es correcto, se procederá a intentar crackear cada hash válido de los argumentos anteriores con cada algoritmo válido de los argumentos anteriores y cada posible valor del archivo.
