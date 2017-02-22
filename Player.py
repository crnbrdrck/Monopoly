class Player:

    _CURRENT_ID = 0

    def __init__(self, username):
        self._username = username

        # Initialise the id using the static variable
        self._id = Player._CURRENT_ID
        Player._CURRENT_ID += 1

    """
        Special Methods
    """

    # To allow Player objects to be used as keys in a dict
    def __hash__(self):
        return self._id

    def __eq__(self, obj):
        return isinstance(Player, obj) and self._id == obj.getId()

    def getUsername(self):
        return self._username

    def getId(self):
        return self._id
