class HashTable:
    def __init__(self, size=19):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, data):
        hash_value = self.hash_function(key)

        if self.slots[hash_value] is None:
            self.slots[hash_value] = key
            self.data[hash_value] = data
        else:
            if self.slots[hash_value] == key:
                print('Hash update')
                self.data[hash_value] = data  # replace data
            else:
                next_slot = self.rehash(hash_value)
                while (self.slots[next_slot] is not None and
                       self.slots[next_slot] != key):
                    next_slot = self.rehash(next_slot)
                print('Hash collision, next_slot {0}'.format(next_slot))

                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = data
                else:
                    self.data[next_slot] = data
        print('Hash put, key {0}, data {1}, hash_value {2}'.format(key,
                                                                   data,
                                                                   hash_value))

    def rehash(self, old_hash):
        return (old_hash+1) % self.size

    def hash_function(self, key):
        return key % self.size

    def get(self, key):
        start_slot = self.hash_function(key)
        data = None
        stop = False
        found = False
        position = start_slot

        while (self.slots[position] is not None and
               not found and not stop):
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position)
                if position == start_slot:
                    stop = True
        return data

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)


class HashTableList:
    def __init__(self, size=19):
        self.size = size
        self.slots = list()
        for index in range(0, self.size):
            self.slots.append(dict())

    def put(self, key, data):
        hash_value = self.hash_function(key)

        if len(self.slots[hash_value]) == 0:
            self.slots[hash_value][key] = data
        else:
            if key in self.slots[hash_value].keys():
                print('Hash update')
                self.slots[hash_value][key] = data  # replace data
            else:
                print('Hash collision')
                self.slots[hash_value][key] = data
        print('Hash put, key {0}, data {1}, hash_value {2}'.format(key,
                                                                   data,
                                                                   hash_value))

    def hash_function(self, key):
        return key % self.size

    def get(self, key):
        hash_value = self.hash_function(key)
        return self.slots[hash_value][key]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)


def main():
    hash_table = HashTable(11)
    hash_table[54] = 'CPU'
    hash_table[26] = 'MEMORY'
    hash_table[93] = 'DISK'
    hash_table[17] = 'KEYBOARD'
    hash_table[77] = 'MOUSE'
    hash_table[31] = 'SPEAKER'
    hash_table[44] = 'MONITOR'
    hash_table[55] = 'TOUCH'
    hash_table[20] = 'LAN'
    print(hash_table.slots)
    print(hash_table.data)

    hash_table[20] = 'POWER'
    hash_table[34] = 'MIC'
    hash_table[91] = 'WLAN'
    print(hash_table.slots)
    print(hash_table.data)

    # infinity loop!
    hash_table[1024] = 'BUS'
    print(hash_table.slots)
    print(hash_table.data)


def main2():
    hash_table = HashTableList(11)
    hash_table[54] = 'CPU'
    hash_table[26] = 'MEMORY'
    hash_table[93] = 'DISK'
    hash_table[17] = 'KEYBOARD'
    hash_table[77] = 'MOUSE'
    hash_table[31] = 'SPEAKER'
    hash_table[44] = 'MONITOR'
    hash_table[55] = 'TOUCH'
    hash_table[20] = 'LAN'
    print(hash_table.slots)

    hash_table[20] = 'POWER'
    hash_table[34] = 'MIC'
    hash_table[91] = 'WLAN'
    print(hash_table.slots)

    # infinity loop!
    hash_table[1024] = 'BUS'
    print('here', hash_table[54])
    print(hash_table.slots)


if __name__ == '__main__':
    # main()
    main2()
