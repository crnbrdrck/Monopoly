class Player:

    _CURRENT_ID = 0

    def __init__(self, username):
        self._username = username

        # Initialise the id using the static variable
        self._id = Player._CURRENT_ID

        Player._CURRENT_ID += 1

    def __hash__(self):
        return self._id

    def getUsername(self):
        return self._username

    def getId(self):
        return self._id