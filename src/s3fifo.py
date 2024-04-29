from collections import deque

_debug_mode = 0

def debug_print(str):
    if _debug_mode == 1:
        print(str)

class obj:
    def __init__(self, k, v):
        self._k = k
        self._v = v
        self._cnt = 0

    def __str__(self) -> str:
        return f"obj(_k: {self._k}, _v: {self._v}, _cnt: {self._cnt})"

class S3_FIFO:
    def __init__(self, cache_size, small_ratio):
        # default setting
        self._limitation = 1
        self._hash_table = {}

        # parameters
        self._cache_size = cache_size
        self._small_cache_size = cache_size * small_ratio
        self._main_cache_size = cache_size - self._small_cache_size
        
        # 3 fifo queues
        self.main_fifo = deque()
        self.ghost_fifo = deque()
        self.small_fifo = deque()

        # stats
        self.miss_num = 0
        self.exe_num = 0

    def evict_small_fifo(self):
        while len(self.small_fifo) > self._small_cache_size:
            tmp_obj = self.small_fifo.popleft()
            k = tmp_obj._k
            if tmp_obj._cnt >= self._limitation:
                # push it to the main fifo
                debug_print(f'k={k} is pushed into the main fifo')
                tmp_obj._cnt = 0
                self.main_fifo.append(tmp_obj)
                if len(self.main_fifo) > self._main_cache_size:
                    self.evict_main_fifo()
            else:
                # push it to the ghost fifo
                debug_print(f'k={k} is pushed into the ghost fifo')
                tmp_obj._cnt = None
                tmp_obj._v = None
                self.ghost_fifo.append(tmp_obj)
                # clear the ghost fifo if it is full
                while len(self.ghost_fifo) > self._main_cache_size:
                    debug_print(f'k={k} is evicted from the ghost fifo')
                    cur_evict = self.ghost_fifo.popleft()
                    if cur_evict._k is not None:
                        del self._hash_table[cur_evict._k]

    def evict_main_fifo(self):
        while len(self.main_fifo) > self._main_cache_size:
            tmp_obj = self.main_fifo.popleft()
            k = tmp_obj._k
            if tmp_obj._cnt >= 1:
                debug_print(f'k={k} is reinsert to the main fifo')
                tmp_obj._cnt -= 1
                self.main_fifo.append(tmp_obj)
            else:
                debug_print(f'k={k} is evicted from the main fifo')
                del self._hash_table[tmp_obj._k]

    def put(self, k, v):
        self.exe_num += 1
        if k in self._hash_table:
            # if it's in the ghost
            # delete from ghost and add it to the main
            tmp_obj = self._hash_table[k]
            if tmp_obj._cnt is None:
                debug_print(f'k={k} is in the ghost fifo and now it is added to the main fifo')
                self.miss_num += 1
                tmp_obj._k = None
                cur_obj = obj(k, v)
                self.main_fifo.append(cur_obj)
                self._hash_table[k] = cur_obj
            else:
                debug_print(f'k={k} is in the small/main fifo and now it is updated the v')
                tmp_obj._v = v
                tmp_obj._cnt = min(tmp_obj._cnt + 1, 3)
        else:
            debug_print(f'k={k} is a new object and now it is added to the small fifo')
            self.miss_num += 1
            cur_obj = obj(k, v)
            self._hash_table[k] = cur_obj
            self.small_fifo.append(cur_obj)
        
        if len(self.small_fifo) > self._small_cache_size:
            self.evict_small_fifo()
        
        if len(self.main_fifo) > self._main_cache_size:
            self.evict_main_fifo()

    def get(self, k):
        self.exe_num += 1
        if k not in self._hash_table:
            self.miss_num += 1
            debug_print(f'k={k} is not in cache, return None')
            return None
        tmp_obj = self._hash_table[k]
        if tmp_obj._cnt is None:
            self.miss_num += 1
            debug_print(f'k={k} is in ghost fifo, return None')
            return None
        tmp_obj._cnt = min(tmp_obj._cnt + 1, 3)
        debug_print(f'k={k} is in small/main fifo, return {tmp_obj._v}')
        return tmp_obj._v
    
    def print_queue(self, queuename):
        cur_queue = []
        if queuename == 'main':
            cur_queue = self.main_fifo
        elif queuename == 'ghost':
            cur_queue = self.ghost_fifo
        elif queuename == 'small':
            cur_queue = self.small_fifo
        print("==================" + queuename + "===============")
        if len(cur_queue) == 0:
            print('this queue is empty')
        for ele in cur_queue:
            print(ele)
    
    def print_queues(self):
        self.print_queue('main')
        self.print_queue('ghost')
        self.print_queue('small')

    def get_miss_ratio(self):
        return self.miss_num / self.exe_num

def is_put_instruction(instruction):
    return instruction.startswith('put')

def is_get_instruction(instruction):
    return instruction.startswith('get')    
    
def execute_s3_fifo(cache, file='./instructions.txt'):
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            if is_get_instruction(line):
                cache.get(line.split()[1])
            if is_put_instruction(line):
                cache.put(line.split()[1], line.split()[2])
        
if __name__ == "__main__":
    _debug_mode = 1
    s3 = S3_FIFO(5, 0.4)
    execute_s3_fifo(s3, './toy_test.txt')
    s3.print_queues()
    print('miss ratio = ', s3.get_miss_ratio())