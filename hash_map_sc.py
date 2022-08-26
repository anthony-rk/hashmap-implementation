# Name: Anthony Kowalski
# OSU Email: kowalsan@oregonstate.edu
# Course: CS261 - Data Structures - 401
# Assignment: 6 - Hash Map
# Due Date: August 9th, 2022
# Description: This file contains the code for a HashMap class that utilizes a separate chaining methodology.


from a6_include import (DynamicArray, LinkedList, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key value pair in the hash map. If the key exists, it will update the value. Otherwise it will add
        the key value pair to the underlying data structrue
        """
        # Calculate the hash value
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        list_head = self._buckets[index]

        # Add the key/value pair to a linked list that does not already contain it
        if list_head.length() == 0 or list_head.contains(key) is None:
            list_head.insert(key, value)
            self._size += 1
        else:
            # Update the value
            node = list_head.contains(key)
            node.value = value

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        sum = 0
        # Iterate over each index, sum up the number of None items
        index = 0
        while index < self.get_capacity():
            list_head = self._buckets[index]
            if list_head.length() == 0:
                sum += 1
            index += 1
        return sum

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        Load factor = total number of elements stored in the table / number of buckets
        𝝺 = n / m
        """
        index = 0
        # sum the lengths of each linked list in the dynamic array
        num_elements = 0
        while index < self._buckets.length():
            num_elements += self._buckets[index].length()
            index += 1

        num_buckets = self._buckets.length()
        return num_elements / num_buckets

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        index = 0
        while index < self._buckets.length():
            for node in self._buckets[index]:
                if self._buckets[index].remove(node.key) is True:
                    self._size -= 1
            index += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the capacity of the internal hash table. All existing key/value pairs will be copied over into their new
        hash map location.
        If the new capacity is not a prime number, the next closest prime will be found and used.
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        new_hash_da = DynamicArray()
        for i in range(0, new_capacity):
            new_hash_da.append(LinkedList())

        index = 0
        while index < self._buckets.length():
            for node in self._buckets[index]:
                # Calculate the hash value
                hash_value = self._hash_function(node.key)
                new_index = hash_value % new_capacity

                new_hash_da[new_index].insert(node.key, node.value)
                # new_hash_da.set_at_index(index, SLNode(node.key, node.value))
            index += 1

        self._buckets = new_hash_da
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        # Find the hash value index, then search for the key
        # Calculate the hash value
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        for node in self._buckets[index]:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        if self.get(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        if self.contains_key(key) is False:
            return

        # Find and remove the item
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # for node in self._buckets[index]:
        self._buckets[index].remove(key)

        # decrement the size
        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key / value pair
        stored in the hash map.
        """
        out_da = DynamicArray()

        index = 0
        while index < self._buckets.length():
            for node in self._buckets[index]:
                temp_tuple = (node.key, node.value)
                out_da.append(temp_tuple)
            index += 1

        return out_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function takes in a dynamic array, and returns a tuple, where the first item is a dynamic array of the mode
    item(s), and the second item is the frequency.
    It is implemented in O(n) runtime
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    largest_frequency = 0
    items_da = DynamicArray()

    # Iterate through the dynamic array, we can use the frequency as the key, aka 1: "apple" if there was
    # only 1 apple occurence.
    index = 0
    while index < da.length():
        if map.contains_key(da[index]) is False:
            curr_frequency = 1
            map.put(da[index], curr_frequency)
        else:
            # update the frequency as it already exists in the hashmap
            curr_frequency = map.get(da[index])
            curr_frequency += 1
            # if curr_frequency >= largest_frequency:
            #     largest_frequency = curr_frequency
            map.put(da[index], curr_frequency)

        # Remove all other values, add new value ot the items_da
        if curr_frequency == largest_frequency:
            items_da.append(da[index])
        if curr_frequency > largest_frequency:
            largest_frequency = curr_frequency
            while items_da.length() > 0:
                items_da.pop()

            items_da.append(da[index])

        index += 1

    print(map)
    return (items_da, largest_frequency)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
