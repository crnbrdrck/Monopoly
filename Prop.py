class Prop:
    _CURRENT_ID = 0

    def __init__ (self, name, price):
        self.__name = name
        self.__price = price
        self.__owner = None
        self._id = Player._CURRENT_ID
        Player._CURRENT_ID += 1

    def getOwner(self):
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
        self.__owner = None:

    def isOwned(self, owner):
        if self.__owner != None:
            return True
        else:
            return False
