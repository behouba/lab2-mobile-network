class FixedList:
    def __init__(self, size):
        self.content = []
        self.__size = size

    def append(self, value):
        if len(self.content) >= self.__size:
            self.content.pop(0)

        self.content.append(value)

    def __getitem__(self, item):
        return self.content[item]

    def __setitem__(self, key, value):
        self.content[key] = value

    def __repr__(self):
        return self.content.__repr__()

    def __len__(self):
        return self.__size
