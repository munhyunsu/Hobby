class InterfaceList():

    def size(self):
        raise NotImplementedError
    
    def add(self, idx, data):
        raise NotImplementedError

    def remove(self, idx):
        raise NotImplementedError

    def get(self, idx):
        raise NotImplementedError


class InterfaceSet():

    def size(self):
        raise NotImplementedError
    
    def add(self, data):
        raise NotImplementedError

    def remove(self, data):
        raise NotImplementedError

    def isin(self, data):
        raise NotImplementedError


class InterfaceStack():

    def size(self):
        raise NotImplementedError

    def push(self, data):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError


class InterfaceQueue():

    def size(self):
        raise NotImplementedError

    def enqueue(self, data):
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError
