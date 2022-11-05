import pygame.mixer


class Sound:
    def __init__(self, data: str | pygame.mixer.Sound):
        if isinstance(data, str):
            self._sound = pygame.mixer.Sound(data)
        else:
            self._sound = data

    def play(self, loops=0, max_time=0, fade_ms=0):
        return Channel(self._sound.play(loops, max_time, fade_ms))

    def stop(self):
        self._sound.stop()

    def fadeout(self, time):
        self._sound.fadeout(time)

    @property
    def volume(self) -> float:
        return self._sound.get_volume()

    @volume.setter
    def volume(self, value):
        """:param value: 0.0 - 1.0
        If value < 0.0, the volume will not be changed
        If value > 1.0, the volume will be set to 1.0
        """
        self._sound.set_volume(value)

    @property
    def num_channels(self) -> int:
        return self._sound.get_num_channels()

    @property
    def length(self) -> float:
        """
        :return: The length of the sound in seconds
        """
        return self._sound.get_length()

    @property
    def raw(self) -> bytes:
        return self._sound.get_raw()


class Channel:
    def __init__(self, data: int | pygame.mixer.Channel):
        if isinstance(data, int):
            self._channel = pygame.mixer.Channel(data)
        else:
            self._channel = data

    def play(self, sound: Sound, loops=0, max_time=0, fade_ms=0):
        self._channel.play(sound, loops, max_time, fade_ms)

    def pause(self):
        self._channel.pause()

    def stop(self):
        self._channel.stop()

    def unpause(self):
        self._channel.unpause()

    def fadeout(self, time):
        self._channel.fadeout(time)

    @property
    def volume(self) -> float:
        return self._channel.get_volume()

    @volume.setter
    def volume(self, value):
        """:param value: 0.0 - 1.0
        If value < 0.0, the volume will not be changed
        If value > 1.0, the volume will be set to 1.0
        """
        self._channel.set_volume(value)

    def set_stereo_volume(self, left, right):
        self._channel.set_volume(left, right)

    def get_busy(self) -> bool:
        return self._channel.get_busy()

    def get_sound(self) -> Sound:
        return Sound(self._channel.get_sound())

    def queue(self, sound: Sound):
        self._channel.queue(sound)

    def get_queue(self) -> Sound:
        return Sound(self._channel.get_queue())

    def get_end_event(self) -> int:
        return self._channel.get_endevent()

