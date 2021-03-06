import abc
import math


class Device:
    """The base class for devices"""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.name = 'unnamed device'

    @abc.abstractmethod
    def update(self, timestep):
        """Update the state of the device"""
        return

    def get_name(self):
        """Get the name of the device"""
        return self.name

    @abc.abstractmethod
    def get_value(self):
        """Get the current state of the device"""
        return 1

    @abc.abstractmethod
    def get_time(self):
        """Get the current time"""
        return 1


class SampleTemperature(Device):
    """A thermometer device, unfortunately it looks like a pid controller has broken somewhere..."""

    def __init__(self):
        self.name = 'temp_1'
        self.temperature = 350  # kelvin
        self.ambient_temperature = 293  # kelvin
        self.time = 0

    def update(self, timestep):
        self.time += timestep
        self.temperature -= 0.1 * (self.temperature - self.ambient_temperature)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.temperature

    def get_time(self):
        return self.time


class Oscillator(Device):
    """An oscillator device, a vital component of any neutron source instrument!"""

    def __init__(self):
        self.name = 'osc_1'
        self.time = 0
        self.x = 0
        self.A = 1
        self.w = 0.1

    def update(self, timestep):
        self.time += timestep
        self.x = self.A * math.sin(self.w * self.time)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.x

    def get_time(self):
        return self.time
