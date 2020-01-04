import os
import json

from airport import Airport

class Airplane():
    def __init__(self, name):
        self.name = name
        self.location = None

    def change_location(self, new_location):
        self.location = new_location

class Flight(Airplane):
    def __init__(self, name, airportA, airportB, departureTime, duration):
        super().__init__(name, airportA)
        self.destination = airportB
        self.departure = departureTime
        self.duration = duration