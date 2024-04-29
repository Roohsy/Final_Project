from collections import deque

_debug_mode = 0

def debug_print(str):
    if _debug_mode == 1:
        print(str)

class obj:
    def __init__(self, k, v):
        self._k = k
        self._v = v

    def __str__(self) -> str:
        return f"obj(_k: {self._k}, _v: {self._v})"

class FIFO:
    def __init__(self, cache_size):
        self._hash_table = {}
        
        # fifo queue
        self.main_fifo = deque()
        self._cache_size = cache_size

        # stats
        self.miss_num = 0
        self.exe_num = 0
    
    def evict(self):
        while len(self.main_fifo) > self._cache_size:
            cur_evict = self.main_fifo.popleft()
            debug_print(f'k={cur_evict._k} is evicted from the fifo')
            del self._hash_table[cur_evict._k]

    def put(self, k, v):
        self.exe_num += 1
        if k in self._hash_table:
            debug_print(f'k={k} is in the fifo and now it is updated the v')
            tmp_obj = self._hash_table[k]
            tmp_obj._v = v
        else:
            debug_print(f'k={k} is a new object and now it is added to the fifo')
            self.miss_num += 1
            cur_obj = obj(k, v)
            self._hash_table[k] = cur_obj
            self.main_fifo.append(cur_obj)
        if len(self.main_fifo) > self._cache_size:
            self.evict()

    def print_queue(self):
        cur_queue = self.main_fifo
        print("=========================================")
        if len(cur_queue) == 0:
            print('this queue is empty')
        for ele in cur_queue:
            print(ele)

    def get(self, k):
        self.exe_num += 1
        if k not in self._hash_table:
            debug_print(f'k={k} is not in cache, return None')
            self.miss_num += 1
            return None
        tmp_obj = self._hash_table[k]
        debug_print(f'k={k} is in the fifo, return {tmp_obj._v}')
        return tmp_obj._v
    
    def get_miss_ratio(self):
        return self.miss_num / self.exe_num

def is_put_instruction(instruction):
    return instruction.startswith('put')

def is_get_instruction(instruction):
    return instruction.startswith('get')

def execute_fifo(cache, file='./instructions.txt'):
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            if is_get_instruction(line):
                cache.get(line.split()[1])
            if is_put_instruction(line):
                cache.put(line.split()[1], line.split()[2])
    
if __name__ == "__main__":
    _debug_mode = 1
    fifo = FIFO(5)
    execute_fifo(fifo, './toy_test.txt')
    fifo.print_queue()
    print('miss ratio = ', fifo.get_miss_ratio())