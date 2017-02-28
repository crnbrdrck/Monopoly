class Player:

    _CURRENT_ID = 0

    def __init__(self, name):
        self.setUsername()
        self.setBank()
        self.setGo()
        self.setInJail()
        self.setGetOutOfJailFreeCard()
        self._id = Player._CURRENT_ID
        self.__jailCount = 0
        Player._CURRENT_ID += 1
        self.__ownedProperties = []

    def setUsername(self, name):
        self.__name = name

    def getUsername(self):
        return self.__name

    def setBank(self):
        self.__bankBal = 500

    def updateBank(self, value):
        self.__bankBal += value

    def getBankBal(self):
        return self.__bankBal

    def setGo(self):
        self.__pos = 0

    def movePosition(self, newPos):
        self.__pos += newPos

    def getPos(self):
        return self.__pos

    def setInJail(self):
        self.__inJail = False

    def updateJailCount(self):
        self.__jailCount += 1

    def resetJailCount(self):
        self.__jailCount == 0


    def getJailCount(self):
        return self.__jailCount

    def gotToJail(self):
        self.__inJail = True

    def getOutOfJail(self):
        self.__inJail = False

    def setGetOutOfJailFreeCard(self):
        self.__inJailCard = False

    def getJailCard(self):
        self.__jailCard = True

    def useJailCard(self):
        self.__jailCard = False
        self.__inJail = False

    def hasJailCard(self):
        if self.__jailCard == True:
            return True
        else:
            return False

    def addOwnProp(self, prop):
        self.__ownedProperties.append(prop)

    def ownedProperties(self):
        return self.__ownedProperties

    def sellProp(self, prop):
        self.__ownedProperties.remove(prop)

    def __hash__(self):
        return self._id

    def __eq__(self, obj):
        return isinstance(Player, obj) and self._id == obj.getId()
