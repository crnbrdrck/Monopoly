class Prop:

    def __init__(self, name, price):
        self.__name = name
        self.__price = price
        self.__owner = None

    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price

    def getRent(self):
        rent = self.__price * .12
        return rent

    def getOwner(self):
        return self.__owner

    def setOwner(self, owner):
        self.__owner = owner

    def setUnOwned(self):
        self.__owner = None

    def isOwned(self, owner):
        return self.__owner is not None
