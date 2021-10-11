# pygamemig-dev
## Table of contents
* [About](#about)
* [Installation](#installation)
* [Usage](#about)

## About
Pygamemig is a wrapper for the Pygame 2D engine. It was created for people with little coding and Python knowledge to be able to use a 2D engine. As the complexity of the code necessary is less than that of Pygame, Pygamemig is less powerful than Pygame. Pygamemig is inspired by Unity3D syntax.

## Installation
This projects depends on Python3, so, if not installed head to [Python's homepage](https://python.org) and follow the instructions to install Python3 on your computer.

Then install Pygame, its only dependency:

```python3 -m pip install pygame```

Next download [the latest release of Pygamemig](https://github.com/migouche/pygamemig-dev/releases/latest) and place *pygamemig.py* (the file downloaded) on the same folder as your Python script

## Usage
### Index
* [Importing Pygame](#importing-pygame)
* [Creating a Pygamemig window](#creating-a-pygamemig-window)
* [Main Loop](#main-loop)
* [Windows](#windows)
* [Vectors](#vectors)
* [Objects](#objects)
* [Texts](#texts)
* [Transform](#transform)
* [RectTransform](#recttransform)
* [Inputs](#inputs)
* [Colours](#colours)
### Importing Pygame
On your script, import Pygamemig:

```from pygamemig import *```

### Creating a Pygamemig window
First we have to create a window for our sprites and texts to appear. We will [later](#windows) cover the Window class with more detail
```python
from pygamemig import *

window = Window(800, 600) # creates a window with 800x600 pixels
window = Window(800, 600, "window") # same as above, but sets "window" to the window name
window = Window(800, 600, "window", "icon.png") # same as above, but sets "icon.png" to the window icon
```
### Main Loop
This is the basic main loop a Pygamemig script should have
```python
from pygamemig import *

window = Window(800, 600) # creates a pygamemig window

while window.running: # it is recommended to use window.running as the main loop condition
    window.Update() # this line should be called each iteration of the main loop
print("window has been closed")
```
**From now on, assume that any spaces on titles mean dots. Will be changed later, but it's easier to write it like that for now. So *Window Update* means *Window.Update***

[Window.Update()](#window-update) is a function that will be explained in more detail later. Basically, it updates all sprites and texts on screen.
### Windows
For clarification, in these examples *my_window* and *Window* will be used. *Window* means a call to the class itself, and *my_window* is an instance of the *Window* class.
#### Window Update
Updates everything in the screen.
```python
my_window = Window(600, 600)
my_window.Update()
```
This function will first fill the whole screen whit the [background colour](#window-setbg) and then print all sprites([objects](#objects)) and [texts](texts) on top of that layer
#### Window setTitle
Changes the window title to the function parameter:

```python
my_window.setTitle("new title")
```

#### Window setIcon
Changes the window icon the image whose path was passed as the function parameter:

```python
my_window.setIcon("folder/image.png")
```

#### Window setBG
Sets the background colour to the [colour](#colours) passed as the function parameter:
```python
my_window.setBG(my_colour)
```

#### Window fillBG
Fills the background with the [colour](#colours) specified. This will cover all sprites and texts and is not recommended to use, as [Window.Update()](#window-update) already does it with the right timing:

```python
my_window.fillBG(my_colour)
```

#### Window Quit
This will close the pygamemig window.

```python
my_window.Quit()
```

### Vectors
Vectors are geometric terms representing a point in space. Pygamemig uses 2D vectors, and can be defined as so:

```python
v = Vector2(5, 7) # this 2d vector represents a point 5 pixels to the right and 7 pixels down from the origin
```

**NOTE:** In pygamemig positive *x* values are to the right of the origin, and positive *y* values are below, **not on top** of the origin
The value of the components of vectors can be floating points, but will be put on screen with integer components.

#### Vector2 magnitue
Returns the magnitue of the vector:

```python
v.magnitude() # returns sqrt(5*5 + 7*7)
```

#### Vector2.normalized
Returns a vector with the same direction and [magnitude](#vector2-magnitue) 1:

```python
v.normalized()
```

#### Vector2 zero
Returns an empty vector:

```python
Vector2.zero() # returns Vector2(0, 0)
```

#### Vector2 scale
Returns the [hadamard product](#https://en.wikipedia.org/wiki/Hadamard_product_(matrices)) of the two given vectors:

```python
Vector2.scale(a, b) # returns Vector2(a.x * b.x, a.y * b.y)
```

#### Vector2 scalar
Returns the [dot product](#https://en.wikipedia.org/wiki/Dot_product) of the two given vectors:

```python
Vector2.scalar(a, b) # returns the dot product between a and b
```

#### Vector2 angleDeg
Returns the angle between two vectors in degrees:

```python
Vector2.angleDeg(a, b) # returns the angle that a and b make in degrees
```

#### Vector2 angleRad
Returns the angle between two vectors in radians:

```python
Vector2.angleRad(a, b) # returns the angle that a and b make in radians
```

**NOTE:** Use [Deg2Rad](#deg2rad) and [Rad2Deg](#rad2deg) to convert from radians to vectors and viceversa

#### Vector random
Returns a random [unitary vector](#vector2normalized):

```python
Vector2.random()
```

#### Vector2.degRandom
