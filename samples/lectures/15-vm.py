text = '''
              Jin-Soo Kim
   (jinsoo.kim@snu.ac.kr)
     Systems Software &
       Architecture Lab.
Seoul National University   Virtual Memory
                Fall 2022



                            Chap. 5.7 – 5.8, 5.13, 5.16 – 5.17
   ▪ Example
       • What happens if two users simultaneously run this program?
                                             #include <stdio.h>

                                             int n = 0;

                                             int main ()
                                             {
                                                 n++;
                                                 printf (“&n = %p, n = %d\n”, &n, n);
                                             }

                                             % ./a.out
                                             &n = 0x0804a024, n = 1
                                             % ./a.out
                                             &n = 0x0804a024, n = 1
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)        2
   ▪ Used in “simple” systems like embedded microcontrollers
       • Cars, elevators, digital cameras, etc.
                                                                                                      Main memory
                                                                                                      0:
                                                                                                      1:
                                                                                   Physical address   2:
                                                                                         (PA)         3:
                                                                   CPU                                4:
                                                                                          4
                                                                                                      5:
                                                                                                      6:
                                                                                                      7:
                                                                                                      8:




                                                                                                           ...
                                                                                                  M-1:


                                                                                              Data word


4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                    3
   ▪ Used in all modern servers, laptops, and smartphones
   ▪ One of the great ideas in computer science
                                                                                                                  Main memory
                                                                                                                  0:
                                      CPU Chip                                                                    1:
                                                                                                                  2:
                                                                   Virtual address           Physical address
                                                                        (VA)                       (PA)
                                                                                                                  3:
                                                 CPU                                 MMU                          4:
                                                                          4100                      4             5:
                                                                                                                  6:
                                                                                                                  7:
                                                                                                                  8:




                                                                                                                       ...
                                                                                                                M-1:


                                                                                       Data word

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                4
   ▪ Process’ abstract view of memory                                               0
                                                                                                  unused

       • OS provides illusion of private address                                            read-only segment
                                                                                           (.init, .text, .rodata)
         space to each process
       • Contains all of the memory state of                                               read/write segment
                                                                                               (.data, .bss)
         the process
                                                                                             run-time heap
                                                                                          (managed by malloc)
   ▪ Static area: allocated on exec()                                                                                  brk

       • Code & Data
                                                                                                                       stack
   ▪ Dynamic area: allocated at runtime                                                         user stack
                                                                                                                       pointer
                                                                                           (created at runtime)
       • Can grow or shrink                                                                                          memory
       • Heap & Stack                                                                     kernel virtual memory
                                                                                         (code, data, heap, stack)
                                                                                                                     invisible to
                                                                                                                     user code
                                                                                   N-1

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                    5
   ▪ Use main memory as a “cache” for secondary (disk) storage
       • Managed jointly by CPU hardware and the operating system

   ▪ Programs share main memory
       •     Each gets a private virtual address space holding its frequently used code and data
       •     Use virtual addresses for memory references
       •     Virtual address space is protected from other processes
       •     Lazy allocation: physical memory is dynamically allocated or released on demand

   ▪ CPU and OS translate virtual addresses to physical addresses
       • VM “block” is called a page
       • VM translation “miss” is called a page fault
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                   6
   ▪ Fixed-size pages (e.g., 4KB)




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   7
   ▪ Stores placement information
       • Array of page table entries (PTEs), indexed by virtual page number
       • Page table register in CPU points to page table in physical memory


   ▪ If page is present in memory
       • PTE stores the physical page number
       • Plus other status bits (protection, referenced, dirty, …)


   ▪ If page is not present
       • PTE can refer to location in swap space on disk

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   8
                                                                                           Virtual address
                                                                                           n-1                            p p-1                           0
                                    Page table
                               base register (PTBR)                                          Virtual page number (VPN)       Virtual page offset (VPO)
                                 (satp in RISC-V)


                                                                                   Page table
                                                                                   Valid     Physical page number (PPN)
                                Physical page table
                                address for the current
                                process



                                       Valid bit = 0:
                                Page not in memory
                                                                                                          Valid bit = 1
                                        (page fault)


                                                                                           m-1                            p p-1                           0
                                                                                             Physical page number (PPN)      Physical page offset (PPO)
                                                                                           Physical address
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                                              9
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   10
                                                     Level 1                         Level 2     Virtual
                                                   page table                      page tables   memory
                                                                                                               0
                                                                                                    VP 0

                                                                                      PTE 0          ...
                                                          PTE 0
                                                                                       ...        VP 1023          2K allocated VM pages
                                                          PTE 1                                                    for code and data
                                                                                    PTE 1023      VP 1024
                                                     PTE 2 (null)
                                                                                                     ...
                                                     PTE 3 (null)
                                                                                                  VP 2047
                                                     PTE 4 (null)                     PTE 0
                                                     PTE 5 (null)                      ...
                                                     PTE 6 (null)                   PTE 1023
                                                     PTE 7 (null)                                   Gap            6K unallocated VM pages

                                                          PTE 8
                                                                                    1023 null
                                                       (1K - 9)                       PTEs
                                                      null PTEs                     PTE 1023       1023
                                                                                                 unallocated       1023 unallocated pages
                                                                                                   pages
     32 bit addresses, 4KB pages, 4-byte PTEs                                                     VP 9215          1 allocated VM page
                                                                                                                   for the stack




                                                                                                     ...
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                             11
                                                   9                               9                   9                 9               12         Virtual
                                               VPN 1                         VPN 2                   VPN 3         VPN 4                VPO
                                                                                                                                                    address

                                                  L1 PT                     L2 PT                 L3 PT                  L4 PT
                                               Page global               Page upper            Page middle               Page
                                     40         directory              40 directory          40 directory         40     table
                   CR3                /                                  /                       /                 /
                  Physical
                  address                                                                                                                          Offset into
                  of L1 PT                                                                                                                    /12 physical and
                                                    L1 PTE                         L2 PTE              L3 PTE           L4 PTE                    virtual page
                                                                                                                                   Physical
                                                                                                                                    address
                                                   512 GB                       1 GB                    2 MB             4 KB       of page
                                                   region                      region                  region           region
                                                  per entry                   per entry               per entry        per entry

                                                                                                                   40
                                                                                                                    /

                                                                                            40                                          12          Physical
                                                                                            PPN                                        PPO
                                                                                                                                                    address
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                                                 12
   ▪ Address translation would appear to require extra memory references
       • One to access the PTE
       • Then the actual memory access


   ▪ But access to page tables has good locality
       • Use a fast cache of PTEs within the CPU
       • Called a Translation Look-aside Buffer (TLB)
       • Typical: 16 – 512 PTEs, 0.5 – 1 cycle for hit, 10 – 100 cycles for miss,
                  0.01% – 1% miss rate
       • Misses could be handled by hardware or software


4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)    13
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   14
   ▪ A TLB hit eliminates a memory access

                                                   CPU Chip
                                                                                                 TLB
                                                                                         2             PTE
                                                                                        VPN             3

                                                                                    1
                                                                                   VA                        PA
                                                            CPU                              MMU
                                                                                                             4    Cache/
                                                                                                                  Memory




                                                                                        Data
                                                                                             5


4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                           15
   ▪ A TLB miss incurs an additional memory access (the PTE)
       • Fortunately, TLB misses are rare. Why?

                                                  CPU Chip
                                                                                               TLB
                                                                                                      4
                                                                                         2           PTE
                                                                                        VPN

                                                                                    1                 3
                                                                                   VA                PTEA
                                                           CPU                               MMU
                                                                                                            Cache/
                                                                                                     PA     Memory
                                                                                                      5


                                                                                        Data
                                                                                         6

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                     16
   ▪ Use faulting virtual address to find PTE
   ▪ Locate page on disk
   ▪ Choose page to replace
       • If dirty, write to disk first
   ▪ Read page into memory and update page table
   ▪ Make process runnable again
       • Restart from faulting instruction




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   17
   ▪ On page fault, the page must be fetched from disk
       • Takes millions of clock cycles
       • Handled by OS code


   ▪ Try to minimize page fault rate
       • Fully associative placement
       • Smart replacement algorithms




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   18
   ▪ Physically addressed cache
       • Allows multiple processes to have blocks in cache
       • Allows multiple processes to share pages
       • Address translation is on the critical path

                                                                                      TLB hit            PA                          PA   Memory
                                                    VA                                                          Cache
                                                                    TLB                                                      Cache
                                                                                                                              miss
                                                                                                 Page         Cache
                                                                                   TLB miss
                                             page fault                                         tables         hit
                                          protection fault

                                                                                    PTE
                                           Data                                                                       Data

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                                   19
                          Processor package
                                Core x4
                                                                               Instruction                   MMU
                                            Registers
                                                                                  fetch                 (addr translation)

                                         L1 d-cache                            L1 i-cache        L1 d-TLB                L1 i-TLB
                                        32 KB, 8-way                          32 KB, 8-way   64 entries, 4-way      128 entries, 4-way

                                                         L2 unified cache                                 L2 unified TLB
                                                          256 KB, 8-way                                 512 entries, 4-way
                                                                                                                                         To other
                                                                                                            QuickPath interconnect       cores
                                                                                                            4 links @ 25.6 GB/s each     To I/O
                                                                                                                                         bridge
                                                      L3 unified cache                              DDR3 Memory controller
                                                       8 MB, 16-way                                  3 x 64 bit @ 10.66 GB/s
                                                    (shared by all cores)                       32 GB/s total (shared by all cores)



                                                                                                          Main memory
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                                    20
Memory Hierarchy Principles
   ▪ Common principles apply at all levels of the memory hierarchy
       • Based on notions of caching


   ▪ At each level in the hierarchy
       •     Block placement
       •     Finding a block
       •     Replacement on a miss
       •     Write policy




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   22
   ▪ Determined by associativity
       • Direct mapped (1-way associative) – one choice for placement
       • n-way set associative – n choices within a set
       • Fully associative – any location


   ▪ Higher associativity reduces miss rate
       • Increases complexity, cost, and access time




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   23
                                              Associativity                                Location method       Tag comparisons
                                Direct mapped                                      Index                     1
                                n-way set associative                              Set index, then search    n
                                                                                   entries within the set
                                Fully associative                                  Search all entries        #entries
                                                                                   Full lookup table         0


   ▪ Hardware caches
       • Reduce comparisons to reduce cost
   ▪ Virtual memory
       • Full table lookup makes full associativity feasible
       • Benefit in reduced miss rate
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                   24
   ▪ Choice of entry to replace on a miss
       • Least recently used (LRU)
           – Complex and costly hardware for high associativity
       • Random
           – Close to LRU, easier to implement


   ▪ Virtual memory
       • LRU approximation with hardware support




4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   25
   ▪ Write-through
       • Update both upper and lower levels
       • Simplifies replacement, but may require write buffer

   ▪ Write-back
       • Update upper level only
       • Update lower level when block is replaced
       • Need to keep more state

   ▪ Virtual memory
       • Only write-back is feasible, given disk write latency

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   26
                                                                                                                Negative
                                    Design change                                   Effect on miss rate
                                                                                                           performance effect
                                                                                   Decrease capacity      May increase access
                         Increase cache size
                                                                                   misses                 time
                                                                                   Decrease conflict      May increase access
                         Increase associativity
                                                                                   misses                 time

                                                                                                          Increases miss
                                                                                                          penalty. For very large
                                                                                   Decrease compulsory
                         Increase block size                                                              block size, may
                                                                                   misses
                                                                                                          increase miss rate due
                                                                                                          to pollution.
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)                                                    27
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   28
4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   29
   ▪ Fast memories are small, large memories are slow
       • We really want fast, large memories 
       • Caching gives this illusion ☺

   ▪ Principle of locality
       • Programs use a small part of their memory space frequently

   ▪ Memory hierarchy
       • L1 cache  L2 cache  …  DRAM memory  disk

   ▪ Memory system design is critical for multiprocessors

4190.308: Computer Architecture | Fall 2022 | Jin-Soo Kim (jinsoo.kim@snu.ac.kr)   30

'''