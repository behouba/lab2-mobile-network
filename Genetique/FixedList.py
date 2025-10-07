from copy import deepcopy


class FixedList:
    def __init__(self, size=None, content=None):
        if content is None and size is None:
            raise ValueError("Size or Content need to be specified")
        elif content is not None and size is not None:
            raise ValueError("Size and Content can't both be specified")
        elif content is not None and size is None:
            self.content = deepcopy(content)
            self.__size = len(content)
        elif size is not None and content is None:
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

    def reverse(self):
        self.content.reverse()

    def copy(self):
        return deepcopy(self)
