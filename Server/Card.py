class Card:

    def __init__(self, text, is_bail, method):
        # Method must be a lambda that takes in a player object and the server
        self.__text = text
        self.__method = method
        self.__is_bail = is_bail

    def getText(self):
        return self.__text

    def isBail(self):
        return self.__is_bail

    @property
    def method(self, player, server):
        self.__method(player, server)
