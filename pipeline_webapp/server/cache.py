from collections import defaultdict, OrderedDict
import random


def dec_to_bin(n: int) -> str:
    return bin(n)[2:].zfill(32)


class Cache:
    def __init__(
        self,
        words_exponent: int = 0,
        blocks_exponent: int = 0,
        associativity_exponent: int = 0,
        replacement_policy: int = 0,
        hit_time: int = 1,
        miss_penality: int = 20,
    ) -> None:
        self.words_exponent = words_exponent
        self.words = 2**words_exponent
        self.block_size = self.words * 4
        self.blocks_exponent = blocks_exponent
        self.blocks = 2**blocks_exponent
        self.cache_size = self.blocks * self.block_size
        self.associativity_exponent = associativity_exponent
        self.associativity = 2**associativity_exponent
        self.replacement_policy = replacement_policy
        self.hit_time = hit_time
        self.miss_penality = miss_penality
        self.sets = 2 ** (blocks_exponent - associativity_exponent)
        self.accesses = 0
        self.hits = 0
        self.misses = 0
        self.cold_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0
        self.memory_stalls = 0
        self.cache_accesses: defaultdict[str, bool] = defaultdict(bool)
        self.miss_classification_table = [defaultdict(bool) for i in range(self.sets)]
        self.prev_address = ("", "", "")
        self.prev_victim = ("", "", "")
        self.cache = [OrderedDict() for i in range(self.sets)]

    def __split(self, address: str) -> tuple[str, str, str]:
        tag = address[
            : 30
            - self.blocks_exponent
            + self.associativity_exponent
            - self.words_exponent
        ]
        index = address[
            30
            - self.blocks_exponent
            + self.associativity_exponent
            - self.words_exponent : 30
            - self.words_exponent
        ]
        block_offset = address[30 - self.words_exponent :]
        return tag, index, block_offset

    def access(self, address: str, main_memory: dict[int, str]) -> None:
        tag, index, block_offset = self.prev_address = self.__split(address)
        num_index = int(index, 2) if index else 0

        self.accesses += 1
        if self.replacement_policy == 0:
            if tag in self.cache[num_index]:
                self.hits += 1
                self.memory_stalls += self.hit_time - 1
                self.cache[num_index].move_to_end(tag)
                for key in self.cache[num_index][tag]:
                    self.cache[num_index][tag][key] = (
                        main_memory[key]
                        if key in main_memory
                        else self.cache[num_index][tag][key]
                    )
            else:
                self.misses += 1
                self.memory_stalls += self.miss_penality + self.hit_time - 1

                if self.cache_accesses[tag + index]:
                    if self.sets == 1:
                        self.capacity_misses += 1
                    elif self.miss_classification_table[num_index][tag + index]:
                        self.conflict_misses += 1
                    else:
                        self.capacity_misses += 1
                else:
                    self.cold_misses += 1

                if len(self.cache[num_index]) == self.associativity:
                    _, value = self.cache[num_index].popitem(last=False)
                    self.prev_victim = self.__split(dec_to_bin(next(iter(value))))
                    self.miss_classification_table[
                        int(self.prev_victim[1], 2) if self.prev_victim[1] else 0
                    ][self.prev_victim[0] + self.prev_victim[1]] = True
                self.cache[num_index][tag]: OrderedDict[int, str] = OrderedDict()
                num_address = int(tag + index + "0" * len(block_offset), 2)
                for i in range(self.words):
                    self.cache[num_index][tag][num_address + 4 * i] = (
                        main_memory[num_address + 4 * i]
                        if num_address + 4 * i in main_memory
                        else "00000000"
                    )

        elif self.replacement_policy == 1:
            if tag in self.cache[num_index]:
                self.hits += 1
                self.memory_stalls += self.hit_time - 1
                for key in self.cache[num_index][tag]:
                    self.cache[num_index][tag][key] = (
                        main_memory[key]
                        if key in main_memory
                        else self.cache[num_index][tag][key]
                    )
            else:
                self.misses += 1
                self.memory_stalls += self.miss_penality + self.hit_time - 1

                if self.cache_accesses[tag + index]:
                    if self.sets == 1:
                        self.capacity_misses += 1
                    elif self.miss_classification_table[num_index][tag + index]:
                        self.conflict_misses += 1
                    else:
                        self.capacity_misses += 1
                else:
                    self.cold_misses += 1

                if len(self.cache[num_index]) == self.associativity:
                    _, value = self.cache[num_index].popitem(last=False)
                    self.prev_victim = self.__split(dec_to_bin(next(iter(value))))
                    self.miss_classification_table[
                        int(self.prev_victim[1], 2) if self.prev_victim[1] else 0
                    ][self.prev_victim[0] + self.prev_victim[1]] = True
                self.cache[num_index][tag]: OrderedDict[int, str] = OrderedDict()
                num_address = int(tag + index + "0" * len(block_offset), 2)
                for i in range(self.words):
                    self.cache[num_index][tag][num_address + 4 * i] = (
                        main_memory[num_address + 4 * i]
                        if num_address + 4 * i in main_memory
                        else "00000000"
                    )

        elif self.replacement_policy == 2:
            if tag in self.cache[num_index]:
                self.hits += 1
                self.memory_stalls += self.hit_time - 1
                for key in self.cache[num_index][tag]:
                    self.cache[num_index][tag][key] = (
                        main_memory[key]
                        if key in main_memory
                        else self.cache[num_index][tag][key]
                    )
            else:
                self.misses += 1
                self.memory_stalls += self.miss_penality + self.hit_time - 1

                if self.cache_accesses[tag + index]:
                    if self.sets == 1:
                        self.capacity_misses += 1
                    elif self.miss_classification_table[num_index][tag + index]:
                        self.conflict_misses += 1
                    else:
                        self.capacity_misses += 1
                else:
                    self.cold_misses += 1

                if len(self.cache[num_index]) == self.associativity:
                    victim_tag = random.choice(list(self.cache[num_index]))
                    victim_value = self.cache[num_index][victim_tag]
                    del self.cache[num_index][victim_tag]
                    self.prev_victim = self.__split(
                        dec_to_bin(next(iter(victim_value)))
                    )
                    self.miss_classification_table[
                        int(self.prev_victim[1], 2) if self.prev_victim[1] else 0
                    ][self.prev_victim[0] + self.prev_victim[1]] = True
                self.cache[num_index][tag]: OrderedDict[int, str] = OrderedDict()
                num_address = int(tag + index + "0" * len(block_offset), 2)
                for i in range(self.words):
                    self.cache[num_index][tag][num_address + 4 * i] = (
                        main_memory[num_address + 4 * i]
                        if num_address + 4 * i in main_memory
                        else "00000000"
                    )

        self.cache_accesses[tag + index] = True
