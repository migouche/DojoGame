import inspect
from typing import Union
from dojogame.graphics.window import Window
from dojogame.maths.realtime import RealTime
from dojogame.inputs.inputs import Input
from pygame.constants import RESIZABLE
from pygame import init, mixer, quit, error

_window_args = (800, 600)
_window_kwargs = {"title": "Dojo Game", "flags": RESIZABLE, "vsync": False}
_config_called = False


class DojoGame:
    def __init__(self):
        self._window = None

    def run(self):
        global _config_called, _window_args, _window_kwargs
        frame = inspect.currentframe().f_back
        while frame.f_code.co_filename.startswith('<frozen'):
            frame = frame.f_back
        try:
            frame.f_locals['config']()
        except KeyError:
            pass
        _config_called = True

        init()
        RealTime.init()
        Input.update()

        self._window = Window(*_window_args, **_window_kwargs)

        try:
            frame.f_locals['start']()
        except KeyError:
            pass

        try:
            while self._window.running:
                frame.f_locals['update']()
                self._window.update()
                try:
                    frame.f_locals['late_update']()
                except KeyError:
                    pass
                self._window.late_update()

                # if Input.get_key_down(K_q):
                # self.window.quit()
        except KeyError:
            raise Exception("Main loop must be inside an update function")
        except error as e:
            if self.window.running:
                raise e
        except Exception as e:
            quit()
            raise e

    def quit(self):
        self._window.quit()

    def exit(self):
        self._window.quit()

    @property
    def window(self) -> Window:
        if not _config_called or self._window is None:
            raise Exception("Game's window not created yet")
        return self._window

    @staticmethod
    def config_window(width: int = 0, height: int = 0, title: str = "Game Window",
                      icon: str = None, flags: Union[list[int], int] = 0,
                      depth: int = 0, display: int = 0, vsync: bool = False):
        global _window_args, _window_kwargs, _config_called
        if _config_called:
            raise Exception("This function can only be called inside the config function")
        _window_args = (width, height)
        _window_kwargs = {"title": title, "icon": icon, "flags": flags,
                          "depth": depth, "display": display, "vsync": vsync}

    @staticmethod
    def config_mixer(frequency: int = 44100, size: int = -16, channels: int = 2, buffer: int = 512,
                     devicename: str = None, allowedchanges: [int] = None):
        if _config_called:
            raise Exception("This function can only be called inside the config function")
        changes = 0
        for change in allowedchanges:
            changes |= change
        mixer.pre_init(frequency, size, channels, buffer, devicename, changes)
        pass
