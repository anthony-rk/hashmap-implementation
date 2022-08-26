# Name: Anthony Kowalski
# OSU Email: kowalsan@oregonstate.edu
# Course: CS261 - Data Structures - 401
# Assignment: 6 - Hash Map
# Due Date: August 9th, 2022
# Description: This file contains code for a HashMap class, which is implemented using Open Addressing with Quadratic
# Probing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Adds an item to the hashmap (or updates if it already exists). This method will resize the array if the
        load facter is >= 0.50.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.50:
            old_capacity = self.get_capacity()
            new_capacity = old_capacity * 2
            self.resize_table(new_capacity)

        # Calculate the hash value
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # Insert the entry if the first index to find is empty
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return
        else:
            if self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
            else:
                # Probe for the next open spot
                j = 0
                placed = False
                initial = index
                while placed is False:
                    if self._buckets[index] is None:
                        self._buckets[index] = HashEntry(key, value)
                        self._size += 1
                        placed = True
                        return
                    elif self._buckets[index].is_tombstone is True:
                        self._buckets[index] = HashEntry(key, value)
                        self._size += 1
                        placed = True
                        return
                    # Update the value if it already exists
                    elif self._buckets[index].key == key:
                        self._buckets[index].value = value
                        placed = True
                        return
                    else:
                        j += 1
                    index = (initial + (j ** 2)) % self._capacity

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        Load factor = total number of elements stored in the table / number of buckets
        𝝺 = n / m
        """
        return self._size / self._buckets.length()

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets (including tombstones) in the hash table.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the capacity of the internal hash table. All existing key/value pairs will be copied over into their new
        hash map location.
        If the new capacity is not a prime number, the next closest prime will be found and used.
        """
        if new_capacity < 1 or new_capacity < self._size:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Make a new HashMap
        new_hash = HashMap(new_capacity, self._hash_function)

        item_index = 0
        # iterate through the old values, putting them in the new_hash HashMap
        while item_index < self._buckets.length():
            # If the load factor gets too large, resize the table to double the capacity
            if new_hash.get_size() / new_hash.get_capacity() >= 0.50:
                new_hash.resize_table(new_hash.get_capacity() * 2)

            curr_item = self._buckets[item_index]

            # Only need to copy non-none, non-tombstone values over
            if curr_item is not None:
                if curr_item.is_tombstone is False:
                    new_hash.put(curr_item.key, curr_item.value)

            item_index += 1

        # Update the HashMap's internally data
        self._buckets = new_hash._buckets
        self._capacity = new_hash.get_capacity()
        self._size = new_hash.get_size()

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        # Calculate the hash value
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        if self._buckets[index] is None:
            return None

        j = 1
        found = False
        initial = index
        while found is False:
            if self._buckets[index] is None:
                return None
            if self._buckets[index].is_tombstone is False:
                if self._buckets[index].key == key:
                    return self._buckets[index].value
            index = (initial + (j ** 2)) % self._capacity
            j += 1

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

        # Quadratic probe until we find the value
        j = 0
        found = False
        initial = index
        while found is False:
            if self._buckets[index].key == key:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                found = True
            else:
                j += 1
            index = (initial + (j ** 2)) % self._capacity


    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        index = 0
        while index < self._buckets.length():
            if self._buckets[index] is not None:
                self._size -= 1
            self._buckets[index] = None
            index += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key / value pair
        stored in the hash map.
        """
        out_da = DynamicArray()

        index = 0
        while index < self._buckets.length():
            curr_item = self._buckets[index]

            if curr_item is not None:
                if curr_item.is_tombstone is False:
                    temp_tuple = (curr_item.key, curr_item.value)
                    out_da.append(temp_tuple)
            index += 1
        return out_da


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
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
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
    #
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
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
