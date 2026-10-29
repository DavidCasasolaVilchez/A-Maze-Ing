*This project has been created as part of the 42 curriculum by dcasasol, avaldivi.*

# A-Maze-ing

## Descripción

A-Maze-ing es un generador y visualizador de laberintos desarrollado en Python
como parte del currículo de 42. El objetivo es construir un laberinto
reproducible desde un archivo de configuración, abrir un camino entre una
entrada y una salida, encontrar una solución y mostrarla en la terminal.

El proyecto incluye el patrón obligatorio de 42, laberintos perfectos o
imperfectos, colores ANSI, visualización del camino y exportación a
`result.txt`.

## Estructura

```text
develop/
├── main.py                 # Menú principal
├── config.txt              # Configuración por defecto
├── default_config.txt      # Plantilla
├── Makefile                # Entorno virtual y ejecución
├── Model/
│   ├── Cell.py             # Celdas y paredes
│   ├── Panel.py            # Generación y resolución
│   ├── Movement.py         # Movimientos del backtracking
│   ├── Walls.py            # Estado de paredes
│   ├── Enums/              # Direcciones, tipos y modos de display
│   └── Exceptions/         # Errores del dominio
└── Utils/
    ├── ArgsParser.py       # Lectura y validación de configuración
    ├── ConquerCell.py      # Selección de la siguiente celda
    ├── GoBack.py           # Retroceso
    ├── PanelToTxt.py       # Exportación
    └── DisplayerUtils.py   # Presentación y colores
```

## Instrucciones

### Requisitos

- Python 3.10 o superior.
- `make` es opcional.
- Una terminal compatible con ASCII y colores ANSI.

No hay dependencias externas; se utiliza la biblioteca estándar de Python.

### Instalación y ejecución

```bash
cd amazing/develop
make run
```

`make run` crea `venv/` y ejecuta `main.py`. También puede ejecutarse
manualmente con:

```bash
python3 main.py
```

El menú permite:

1. Regenerar el laberinto.
2. Mostrar u ocultar el camino más corto.
3. Cambiar los colores.
4. Salir.

Para limpiar el entorno, las cachés y el resultado:

```bash
make clean
```

## Archivo de configuración

El programa lee `config.txt`. Cada línea utiliza el formato `KEY=VALUE`.

```text
WIDTH=25
HEIGHT=25
ENTRY=3,12
EXIT=2,18
OUTPUT_FILE=file.txt
PERFECT=False
SEED=1213865872316517358710
DISPLAY_MODE=complete
```

| Clave | Formato | Descripción |
|---|---|---|
| `WIDTH` | Entero, mínimo `20` | Anchura del laberinto. |
| `HEIGHT` | Entero, mínimo `15` | Altura del laberinto. |
| `ENTRY` | `fila,columna` | Coordenadas de entrada. |
| `EXIT` | `fila,columna` | Coordenadas de salida. |
| `OUTPUT_FILE` | Texto | Nombre configurado para la salida. |
| `PERFECT` | `True` o `False` | Conserva o permite caminos alternativos. |
| `SEED` | Entero | Semilla para la generación reproducible. |
| `DISPLAY_MODE` | `complete` o `asciibase` | Modo de visualización. |

`default_config.txt` contiene las mismas claves sin valores y sirve como
plantilla. Actualmente `PanelToTxt` genera siempre `result.txt`; el valor de
`OUTPUT_FILE` se valida, pero todavía no cambia ese nombre.

## Algoritmo de generación del laberinto

Se utiliza una búsqueda en profundidad aleatoria (*randomized depth-first
search*) con backtracking:

1. Se crea una cuadrícula con todas las paredes cerradas.
2. Se marca la figura de 42 como zona no transitable.
3. Se selecciona un vecino no visitado al azar y se rompen las paredes de
   ambas celdas.
4. Cuando una celda no tiene vecinos disponibles, se retrocede mediante una
   pila de movimientos.
5. Si `PERFECT=False`, se abren algunas paredes válidas adicionales.
6. Se busca la ruta entre entrada y salida y se muestra la solución más corta.

### ¿Por qué este algoritmo?

DFS con backtracking es sencillo, eficiente en memoria y produce naturalmente
un laberinto perfecto cuando no se abren paredes adicionales. La pila hace
explícito el retroceso y la semilla permite reproducir generaciones para
depurar y comparar resultados.

## Código reutilizable

- `Panel` puede reutilizarse para generar y resolver laberintos con otros
  tamaños, entradas, salidas y semillas.
- `Cell` y `Walls` encapsulan el estado de cada celda y mantienen simétricas
  las paredes de celdas vecinas.
- `ArgsParser` sirve para leer y validar otros archivos `KEY=VALUE`.
- `DisplayerUtils` permite cambiar la presentación sin modificar el algoritmo.
- `conquer_cell` y `go_back` aíslan la selección de vecinos y el backtracking.
- `PanelToTxt` ofrece una representación hexadecimal reutilizable para guardar
  o procesar la cuadrícula.

## Funcionalidades avanzadas

- Laberintos perfectos e imperfectos mediante `PERFECT`.
- Patrón central de 42 con un color diferenciado.
- Mostrar u ocultar la solución desde el menú.
- Modos `complete` y `asciibase`.
- Cambio interactivo de colores de bordes, entrada, salida, camino y figura.
- Exportación de la cuadrícula, coordenadas y pasos a `result.txt`.

## Equipo y gestión del proyecto

### Roles

- **dcasasol:** creó la estructura inicial del proyecto, el modelo de celdas,
  paredes y paneles, las enumeraciones y excepciones, y la generación del
  patrón de 42. También implementó la generación base del laberinto, la
  visualización ASCII, el uso de la semilla para controlar la aleatoriedad,
  la generación de laberintos imperfectos, la resolución de conflictos y el
  menú interactivo con selección de colores.
- **avaldivi:** desarrolló y terminó el resolver, incluyendo la búsqueda desde
  la entrada y la salida y la eliminación de ciclos. También implementó la
  exportación del laberinto a texto, refactorizó partes de las celdas y del
  resolver, limpió archivos generados y añadió el `Makefile` y la ejecución
  mediante un entorno virtual.

### Planificación y evolución

El plan inicial dividía el trabajo en modelo de datos, generación, resolución y
presentación. Durante el desarrollo se añadió una etapa específica de
validación y se incorporaron después el modo imperfecto, el camino visible,
los colores y la exportación para cubrir las funcionalidades avanzadas.

### Qué funcionó bien y qué se puede mejorar

Funcionó bien separar `Model/` y `Utils/`, utilizar una pila explícita para el
backtracking y conservar una semilla para reproducir casos. El menú facilitó
probar rápidamente distintas generaciones.

Como mejoras futuras, `OUTPUT_FILE` debería controlar realmente el nombre de
salida, las coordenadas deberían validarse de forma consistente como
fila/columna y sería conveniente añadir pruebas automatizadas para semillas,
dimensiones límite, coordenadas inválidas y resolución.

### Herramientas utilizadas

- Python y su biblioteca estándar.
- `make` para automatizar el entorno virtual y la ejecución.
- Git para el control de versiones.
- Terminal ANSI para la visualización coloreada.
- Editor/IDE y herramientas de análisis estático para inspección y depuración.

## Recursos

- [Documentación de Python](https://docs.python.org/3/)
- [Módulo `random` de Python](https://docs.python.org/3/library/random.html)
- [Estructuras de datos de Python](https://docs.python.org/3/tutorial/datastructures.html)
- [Búsqueda en profundidad](https://en.wikipedia.org/wiki/Depth-first_search)
- [Algoritmos de generación de laberintos](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Códigos de escape ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)

### Uso de la IA

Se utilizó IA como apoyo, no como sustituto de la comprensión del código. Se
empleó para revisar la estructura del proyecto, explicar el algoritmo DFS con
backtracking implementado en `Panel.py`, `ConquerCell.py` y `GoBack.py`,
organizar las instrucciones y la documentación de la configuración, proponer
la estructura de este README y revisar su redacción.

La implementación del modelo, el generador, el resolver, el display, el menú y
la exportación forman parte del código del proyecto y fueron revisados por el
autor.