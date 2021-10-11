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
* [RealTime](#realtime)
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

[Window.Update()](#windowupdate) is a function that will be explained in more detail later. Basically, it updates all sprites and texts on screen.

### Windows
For clarification, in these examples *my_window* and *Window* will be used. *Window* means a call to the class itself, and *my_window* is an instance of the *Window* class.

#### Window.Update
Updates everything in the screen.

```python
my_window = Window(600, 600)
my_window.Update()
```

This function will first fill the whole screen whit the [background colour](#windowsetbg) and then print all sprites([objects](#objects)) and [texts](#texts) on top of that layer

#### Window.setTitle
Changes the window title to the function parameter:

```python
my_window.setTitle("new title")
```

#### Window.setIcon
Changes the window icon the image whose path was passed as the function parameter:

```python
my_window.setIcon("folder/image.png")
```

#### Window.setBG
Sets the background colour to the [colour](#colours) passed as the function parameter:
```python
my_window.setBG(my_colour)
```

#### Window.fillBG
Fills the background with the [colour](#colours) specified. This will cover all sprites and texts and is not recommended to use, as [Window.Update()](#windowupdate) already does it with the right timing:

```python
my_window.fillBG(my_colour)
```

#### Window.Quit
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

#### Vector2.magnitue
Returns the magnitue of the vector:

```python
v.magnitude() # returns sqrt(5*5 + 7*7)
```

#### Vector2.normalized
Returns a vector with the same direction and [magnitude](#vector2magnitue) 1:

```python
v.normalized()
```

#### Vector2.zero
Returns an empty vector:

```python
Vector2.zero() # returns Vector2(0, 0)
```

#### Vector2.scale
Returns the [hadamard product](https://en.wikipedia.org/wiki/Hadamard_product_(matrices)) of the two given vectors:

```python
Vector2.scale(a, b) # returns Vector2(a.x * b.x, a.y * b.y)
```

#### Vector2.scalar
Returns the [dot product](https://en.wikipedia.org/wiki/Dot_product) of the two given vectors:

```python
Vector2.scalar(a, b) # returns the dot product between a and b
```

#### Vector2.angleDeg
Returns the angle between two vectors in degrees:

```python
Vector2.angleDeg(a, b) # returns the angle that a and b make in degrees
```

#### Vector2.angleRad
Returns the angle between two vectors in radians:

```python
Vector2.angleRad(a, b) # returns the angle that a and b make in radians
```

**NOTE:** Use [Deg2Rad](#deg2rad) and [Rad2Deg](#rad2deg) to convert from radians to vectors and viceversa

#### Vector.random
Returns a random [unitary vector](#vector2normalized):

```python
Vector2.random()
```

#### Vector2.degRandom
Returns a random vector contained between two angles given in degrees:

```python
Vector2.degRandom(0, 180) # returns a random vector that forms from 0º to 180º with any horizontal line
```

#### Vector2.radRandom
Returns a random vector contained between two angles given in radians

```python
Vector2.radRandom(0, 3) # returns a random vector that forms from 0 radians to 3 radians with any horizontal line
```

### Objects
Objects are all the sprites that have to be displayed on screen. [Texts](#texts) are **not** objects, we will cover them later on. Once declared, objects will be automatically displayed on screen without any other method calls. Objects are declared like so:

```python
# Object(img, scale)
obj = Object("img/sprite1.png", Vector2(100, 100))
```

In this example the object *obj* will have the image *img/sprite1.png* and will be resized to be 100 pixels wide and 100 pixels tall. An objects [position](#transformposition), [rotation](#transformrotation), and [scale](#transformscale) are controlled throught its [Transform](#transform).

### Texts
Texts are the other type of entity that can be displayed on screen with Pygamemig. They are declared like so:

```python
# Text(font, size, textColour, backgroundColour)
txt = Text("freesansbold.ttf", 15, Colours.black, Colours.white)
```

In this example, the text *txt* will have the *freesansbold* font, a font size of 15, black text, and white background. **NOTE:** For now, transparent background is impossible in Pygamemig

#### Text.Text
Changes the text displayed by the one passed:

```python
txt.Text("new text") # changes the text displayed by txt with "new text"
```

#### Text.setSize
Changes the size of the text:

```python
txt.setSize(20) # changes txt size to 20
```

#### Text.setTextColor
Changes the font colour:

```python
txt.setTextColor(Colours.red) # changes the font colour to red
```

#### Text.setTextColour
Equivalent to [Text.setTextColor()](#textsettextcolor)

#### Text.setBGColor
Changes the background colour of the text:

```python
txt.setBGColor(Colours.green) # changes the background colour to green
```

#### Text.setBGColour
Equivalent to [Text.setBGColor](#textsetbgcolor)

For more info on colours see [Colour](#colours). A text [position](#recttransformposition), [rotation](#recttransformrotation), and [scale](#recttransformscale) are controlled through its [RectTransform](#recttransform)

### Transform
An objects Transform determines its [position](#transformposition), [rotation](#transformrotation), and [scale](#transformscale). There is no need to declare any Transform ever, as Pygamemig does it already for every [Object](#objects)

#### Transform.position
An objects position is expressed with a [Vector2](#vectors). The position origin is in the top left corner of the window, so that increasing the *x* value will move the object right, and increasing the *y* value will move the object down. To change an objects position, you can use:

```python
obj.transform.position = Vector2(100, 100)
```
or:
```python
obj.transform.setPos(Vector2(100, 100)) # it is recommended to use this function instead of changing the property directly
```

or use [Transform.Translate()](#transformtranslate).

#### Transform.translate
Instead of overriding the position, translate() adds the translation to the current position:

```python
obj.transform.translate(Vector2(200, 250)) # this will add Vector2(200, 250) to the current position
```

So, if the position of *obj* is [Vector2](#vectors)(50, 100), then the new position will be [Vector2](#vectors)(250, 350).

**NOTE:** For every translation it is **very** recommended to use [RealTime.dt](#realtimedeltatime)

#### Transform.rotation
An objects' rotation is expressed in degrees. To change an objects' rotation you can use:

```python
obj.transform.rotation = 180
```
or:
```python
obj.transform.setRot(180) # it is recommended to use this function instead of changing the property directly
```

or use [Transform.Rotate()](#transformrotate)

#### Transform.rotate
Instead of overriding the rotation, rotate() add the new rotation to the current rotation:

```python
obj.transform.rotate(180) # this will add 180º to the current rotation
```

If the rotation of *obj* was 90, the new rotation would be 270.

**NOTE:** For every translation it is **very** recommended to use [RealTime.dt](#realtimedeltatime)


#### Transform.scale
An objects scale is expressed with a [Vector2](#vectors), and it can be changed using:

```python
obj.transform.scale = Vector2(100, 100)
```
or:
```python
obj.transform.setScale(Vector(100, 100)) # it is recommended to use this function instead of changing the property directly
```

### RectTransform
A texts Transform determines its [position](#recttransformposition), [rotation](#recttransformrotation), and [scale](#recttransformscale). There is no need to declare any Transform ever, as Pygamemig does it already for every [Object](#objects)

#### RectTransform.position
A texts position is expressed with a [Vector2](#vectors). The position origin is in the top left corner of the window, so that increasing the *x* value will move the text right, and increasing the *y* value will move the text down. To change a texts position, you can use:

```python
txt.rectTransform.position = Vector2(100, 100)
```
or:
```python
txt.rectTransform.setPos(Vector2(100, 100)) # it is recommended to use this function instead of changing the property directly
```

or use [RectTransform.Translate()](#recttransformtranslate).

#### RectTransform.translate
Instead of overriding the position, translate() adds the translation to the current position:

```python
txt.RectTransform.translate(Vector2(200, 250)) # this will add Vector2(200, 250) to the current position
```

So, if the position of *txt* is [Vector2](#vectors)(50, 100), then the new position will be [Vector2](#vectors)(250, 350).

**NOTE:** For every translation it is **very** recommended to use [RealTime.deltaTime](#realtimedeltatime)

#### RectTransform.rotation
A texts' rotation is expressed in degrees. To change an objects' rotation you can use:

```python
txt.RectTransform.rotation = 180
```
or:
```python
obj.transform.setRot(180) # it is recommended to use this function instead of changing the property directly
```

or use [RectTransform.Rotate()](#recttransformrotate)

#### RectTransform.rotate
Instead of overriding the rotation, rotate() add the new rotation to the current rotation:

```python
txt.rectTransform.rotate(180) # this will add 180º to the current rotation
```

If the rotation of *txt* was 90, the new rotation would be 270.

**NOTE:** For every translation it is **very** recommended to use [RealTime.dt](#realtimedeltatime)


#### RectTransform.scale
A texts scale is expressed with a [Vector2](#vectors), and it can be changed using:

```python
txt.RectTransform.scale = Vector2(100, 100)
```
or:
```python
txt.RectTransform.setScale(Vector(100, 100)) # it is recommended to use this function instead of changing the property directly
```
### RealTime
RealTime is a functionality of Pygamemig that handles everything needed to have a constant framerate and constant speeds across different devices and framerates. [Window.Update()](#windowupdate) will wait the correspondent time to begin the next frame. By default, Pygamemig runs at 60 fps, but can be changed like so:

```python
RealTime.setDT(1/30) # this will run at 30 fps (1 / framerate)
```

This is a very useful tool to have an object move at the same speed with any device at any framerate. To adjust the speed to the framerate, use [RealTime.deltaTime](#realtimedeltatime).

#### RealTime.deltaTime
This is value represents the time between each frame in seconds. To adjust [Transform.translate()](#transformtranslate), [Transform.rotate()](#transformrotate), [RectTransform.translate()](#recttransformtranslate), and [RectTransform.rotate()](#recttransformrotate), all that is needed is to multiply by RealTime.deltaTime:

```python
obj.transform.translate(Vector2(100, 100) * RealTime.deltaTime)
txt.rectTransform.rotate(90 * RealTime.deltaTime)
```

### Inputs
Input handles all the keystrokes the window receives. For now, Pygamemig only receives if a key is pressed or not, and can't tell if a key has just been pressed or released that frame. To check if a key is being pressed, use [Input.GetKey()](#inputgetkey)

#### Input.GetKey
Will return True or False whether a key is being pressed or not:

```python
Input.GetKey(K_w) # returns true if the 'w' key is being pressed. If it isn't, it returns false
```

Pygamemig uses [Pygame's keys](http://cs.roanoke.edu/Fall2013/CPSC120A/pygame-1.9.1-docs-html/ref/key.html).

### Colours
**NOTE:** Any function that contains *color* can be written as *colour* and viceversa.

Colours are defined by their red, green, and blue value, from 0 to 255:

```python
# Colour/Color(red, green, blue)
col1 = Colour(255, 0, 0) # red
col2 = Color(0, 255, 0) # green
col3 = Colour(0, 0, 255) # blue
```

#### fromHex
Converts a hexadecimal colour to a Pygame colour:

```python
col = Colour.fromHex("#ff00aa")
```

### Mathf
Mathf stands for Math Functions, and it's a set of useful operation one might need.

#### Deg2Rad
Converts from degrees to radians:

```python
180 * Mathf.Deg2Rad # returns pi (180º to radians)
```

#### Rad2Deg
Converts from radians to degrees:

```python
3 * Mathf.Rad2Deg # returns 3 radians to degrees
```

#### Clamp
Clamps a value between two numbers. If the value is smaller than the minimum value, it will return the minimum value; if the value is greater than the maximum value, it will return the maximum value; and if the value is between the maximum and minimum values, it will return the given value:

```python
val = 50
a = Mathf.Clamp(val, 10, 100) # 50
b = Mathf.Clamp(val, 100, 200) # 100
c = Mathf.Clamp(val, 10, 30) # 30
```