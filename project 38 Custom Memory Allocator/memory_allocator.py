class MemoryBlock:
    def __init__(self, start, size, is_free=True):
        self.start = start
        self.size = size
        self.is_free = is_free

class MemoryAllocator:
    def __init__(self, total_size):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]
    
    def malloc(self, size, strategy='first-fit'):
        if strategy == 'first-fit':
            block = self._first_fit(size)
        elif strategy == 'best-fit':
            block = self._best_fit(size)
        else:
            return None
        
        if block:
            if block.size > size:
                new_block = MemoryBlock(block.start + size, block.size - size)
                self.blocks.insert(self.blocks.index(block) + 1, new_block)
                block.size = size
            block.is_free = False
            return block.start
        return None
    
    def _first_fit(self, size):
        for block in self.blocks:
            if block.is_free and block.size >= size:
                return block
        return None
    
    def _best_fit(self, size):
        best = None
        for block in self.blocks:
            if block.is_free and block.size >= size:
                if not best or block.size < best.size:
                    best = block
        return best
    
    def free(self, address):
        for block in self.blocks:
            if block.start == address and not block.is_free:
                block.is_free = True
                self._merge_blocks()
                return True
        return False
    
    def _merge_blocks(self):
        i = 0
        while i < len(self.blocks) - 1:
            if self.blocks[i].is_free and self.blocks[i + 1].is_free:
                self.blocks[i].size += self.blocks[i + 1].size
                self.blocks.pop(i + 1)
            else:
                i += 1
    
    def display(self):
        print("\n" + "="*60)
        print("MEMORY STATE")
        print("="*60)
        for block in self.blocks:
            status = "FREE" if block.is_free else "ALLOCATED"
            print(f"[{block.start:4d} - {block.start + block.size - 1:4d}] Size: {block.size:4d} | {status}")
        print("="*60)
        free_mem = sum(b.size for b in self.blocks if b.is_free)
        used_mem = self.total_size - free_mem
        print(f"Total: {self.total_size} | Used: {used_mem} | Free: {free_mem}")
        print("="*60 + "\n")

# Demo
if __name__ == "__main__":
    print("\n🧠 CUSTOM MEMORY ALLOCATOR SIMULATION\n")
    
    allocator = MemoryAllocator(1024)
    print("Initialized memory: 1024 bytes")
    allocator.display()
    
    print("→ Allocating 200 bytes (First-Fit)")
    addr1 = allocator.malloc(200, 'first-fit')
    print(f"  Allocated at address: {addr1}")
    allocator.display()
    
    print("→ Allocating 150 bytes (Best-Fit)")
    addr2 = allocator.malloc(150, 'best-fit')
    print(f"  Allocated at address: {addr2}")
    allocator.display()
    
    print("→ Allocating 300 bytes (First-Fit)")
    addr3 = allocator.malloc(300, 'first-fit')
    print(f"  Allocated at address: {addr3}")
    allocator.display()
    
    print(f"→ Freeing memory at address {addr1}")
    allocator.free(addr1)
    allocator.display()
    
    print(f"→ Freeing memory at address {addr2}")
    allocator.free(addr2)
    print("  (Adjacent blocks merged)")
    allocator.display()
    
    print("→ Allocating 400 bytes (Best-Fit)")
    addr4 = allocator.malloc(400, 'best-fit')
    print(f"  Allocated at address: {addr4}")
    allocator.display()
    
    print("✅ Simulation Complete\n")
