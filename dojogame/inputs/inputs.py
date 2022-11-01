# inputs.py

import pygame
from pygame.constants import MOUSEBUTTONUP, MOUSEBUTTONDOWN
from dojogame.maths.vectors import Vector2
from dojogame.data import arrays


class Input:
    @staticmethod
    def get_key(key) -> bool:
        return arrays.keys[key]

    @staticmethod
    def get_key_down(key) -> bool:
        return (not arrays.oldKeys[key]) and arrays.keys[key]

    @staticmethod
    def get_key_up(key) -> bool:
        return arrays.oldKeys[key] and not arrays.keys[key]

    @staticmethod
    def get_event(event, attribute: str = "", value=None) -> bool:
        b = False
        for ev in arrays.events:
            if ev.type == event:
                if attribute == "":
                    b = True
                else:
                    if getattr(ev, attribute) == value:
                        b = True
        return b

    @staticmethod
    def get_event_property(event, prop: str):
        for ev in arrays.events:
            if ev.type == event:
                return getattr(ev, prop)
        raise Exception(f"Event '{event}' doesn't exist. Maybe doesn't happen every frame?")

    # Mouse
    @staticmethod
    def get_mouse_button_down(button) -> bool:
        return Input.get_event(MOUSEBUTTONDOWN, "button", button)

    @staticmethod
    def get_mouse_button_up(button) -> bool:
        return Input.get_event(MOUSEBUTTONUP, "button", button)

    @staticmethod
    def get_mouse_position() -> Vector2:
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])

    @staticmethod
    def update():
        arrays.oldKeys = arrays.keys
        arrays.keys = pygame.key.get_pressed()
        arrays.events = pygame.event.get()
