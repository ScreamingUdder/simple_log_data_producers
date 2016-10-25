import abc


class Device:
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


class SampleTemperature(Device):
    def __init__(self):
        self.name = 'temp_1'
        self.temperature = 350  # kelvin
        self.ambient_temperature = 293  # kelvin

    def update(self, timestep):
        self.temperature -= 0.1 * (self.temperature - self.ambient_temperature)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.temperature
