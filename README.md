# Dojogame

---
## Table of contents
* [About](#about)
* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [Dependencies](#dependencies)
* [License](#license)
* [Documentation](#doc)

---

## About
Dojogame is a 2d graphics engine with an integrated physics motor (Still in WIP). It's open source and cross-platform.
It wraps around pygame, to make its usage easier (making it easier may make it less powerful also).
To follow some kind of structure and standard, dojogame uses Unity3d's syntax.

---

## Installation
For the time being dojogame will stay on the
[testing repository of Python Package Index](https://test.pypi.org/project/dojogame/ "link to the testing project").
To install dojogame on Windows type:

`pip install -i https://test.pypi.org/simple/ dojogame`

To install dojogame on linux type

`pip3 install -i https://test.pypi.org/simple/ dojogame`

---

## Basic Usage
It is recommended to import dojogame like so to avoid typing `dojogame.something` all the time:
````python
from dojogame import *
````
**NOTE:** all methods and classes will be explained in detail on the documentation page

Creating a window:
```python
window = Window(800, 600) # width, height
```

Main game loop:
```python
from dojogame import *

window = Window(800, 800)

while window.running: # Much better that while True: and then break out of it
    #do stuff
    window.update() # Very important to call it every frame
```

Creating an object from image:
```python
my_sprite = Object("path/to/image.png", Vector2(50, 100)) # resizes the image to 50px*100px
```

---

## Dependencies
Dojopy is a wrapper for Pygame. As such, it depends on pygame and, obviously, pygame's dependencies.
Dependency versions:
* pygame >= 2.0.0
* pygame's dependencies:
  * CPython >= 3.6 or PyPy3
  * SDL >= 2.0.0
  * SDL_mixer >= 2.0.0
  * SDL_image >= 2.0.0
  * SDL_ttf >= 2.0.11
  * SDL_gfx (optional, vendored in)
  * NumPy >= 1.6.2 (optional)
  
**NOTE:** pygame's dependencies are pasted from [its README file](https://github.com/pygame/pygame#dependencies)

## License
This library is distributed under [GNU GPL version 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
We reserve the right to place future versions of this library under a different license.

Programs in the `examples` subdirectory are in the public domain.

## Documentation
Detailed documentation is being worked on. Please have in mind this project was not that serious initially,
so some basic things in professional projects might be still in progress. Thank you.



