import os

class BankAccount():
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.type = "normal"
        self.balance = 0

    def getName(self):
        return self.name

    def getNumber(self):
        return self.number

    def getType(self):
        return self.type

    def getBalance(self):
        return self.balance

    def setName(self, name):
        self.name = name
    
    def setNumber(self, Number):
        self.Number = number

    def setType(self, stype):
        self.type = stype

    def setBalance(self, balance):
        self.balance = balance

    def printUser(self):
        pass