# hashmap-implementation

This project implements a hash map using 2 different implementions, using [chaining](hash_map_sc.py) and [open addressing](hash_map_oa.py).

The chaining implementation uses linked lists to resolve collisions, whereas the open addressing implementation finds the next open index in the underlying data structure (dynamic array) and both resize once the hashmap becomes >= a table load threshold in order to maintain optimimal time complexity when doing operations on the hashmap. 
