# Computer Architecture Lab 1
## Ομάδα 13
### Νένος Δημήτρης 9012 dimineno@ece.auth.gr

#### Ερώτημα 1

Στο 1ο ερώτημα εκτέλεσα ένα απλό πρόγραμμα το οποίο εμφανίζει στην έξοδο του συστήματος (stdout) την έκφραση **Hello World!**.
Η εκτέλεση του προγράμματος γίνεται με την εντολή

`$ build/ARM/gem5.opt -d Lab_1/hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"` 

, δεδομένου ότι βρισκόμαι στο _gem5 directory_. Η εντολή αυτή λεέι ότι θα κάνω build με τον simulator _gem5.opt_ με **guest architecture ARM**, στην συνέχεια χρησιμοποιώ το flag **-d** για να ανακατευθύνω το **output** του προγράμματος στο directory results/hello_result. Στην συνέχεια, δίνουμε το script το οποίο θέλω να τρέξω (_starter_se.py_) . Τέλος, δίνω δύο **cmdargs** στο script, το ένα είναι ο τύπος cpu που θέλω να χρησιμοποιήσω (minor CPU) και το άλλο είναι το εκτελέσιμο binary αρχείο που θέλω να τρέξει το script (hello).


```ruby
    parser = argparse.ArgumentParser(epilog=__doc__)
```

όπου η κλάση _argparce_ δημιουργεί το αντικείμενο _ArgumentParser_ το οποίο κρατάει τις εισόδους του script και τα δίνει στο αντικείμενο _parser_. Στην συνέχεια εκτελούνται οι παρακάτω εντολές,

```ruby
   parser.add_argument("commands_to_run", metavar="command(s)", nargs='*',
                        help="Command(s) to run")
    parser.add_argument("--cpu", type=str, choices=list(cpu_types.keys()),
                        default="atomic",
                        help="CPU model to use")
    parser.add_argument("--cpu-freq", type=str, default="4GHz")
    parser.add_argument("--num-cores", type=int, default=1,
                        help="Number of CPU cores")
    parser.add_argument("--mem-type", default="DDR3_1600_8x8",
                        choices=ObjectList.mem_list.get_names(),
                        help = "type of memory to use")
    parser.add_argument("--mem-channels", type=int, default=2,
                        help = "number of memory channels")
    parser.add_argument("--mem-ranks", type=int, default=None,
                        help = "number of memory ranks per channel")
    parser.add_argument("--mem-size", action="store", type=str,
                        default="2GB",
                        help="Specify the physical memory size")

```

Η διαδικασία ανάθεσης των cmdargs στις μεταβλητές του script γίνεται με την μέθοδο _add_argument()_ η οποία αναθέτει το binary εκτελέσιμο _hello_ και το cpu type _minor_. Βλέπω επίσης, ότι τα υπόλοιπα χαρακτηρηστικά του simulator όπως _CPU Frequency_, _Number of Cores_, _Memory_Type_ κλπ εφόσον δεν δίνονται σαν cmdargs παίρνουν τις _default_ τιμές τους. Πιο συγκεκριμένα, η default συχνότητα ρολογιού είναι **4GHz**, ο αριθμός των πυρήνων του επεξεργαστή είναι **1**, ενώ ο τύπος RAM είναι **DDR3_1600_8X8** με 2 κανάλια (δηλ. **dual port**) και μέγεθος **2GB**. Όσον αφορά τον τύπο της CPU βλέπω ότι αναθέτετε ο τύπος _minor_ μέσω των παρακάτω εντολών

```ruby
    cpu_types = {
    "atomic" : ( AtomicSimpleCPU, None, None, None, None),
    "minor" : (MinorCPU,
               devices.L1I, devices.L1D,
               devices.WalkCache,
               devices.L2),
    "hpi" : ( HPI.HPI,
              HPI.HPI_ICache, HPI.HPI_DCache,
              HPI.HPI_WalkCache,
              HPI.HPI_L2)
}
```


Στην συνέχεια εκτελείτε η εντολή

```ruby
    args = parser.parse_args()
```

η οποία ελέγχει τα cmdargs και μετατρέπει το κάθε argument σε σωστό τύπο μεταβλητής. Στην συνέχεια, εκτελείτε η εντολή

```ruby
   root = Root(full_system = False) 
```

η οποία δηλώνει το _Excecution Mode_ του _gem5_ ως **System-Call Emulation (SE)**, δηλαδή ορίζει ότι ο gem5 δεν τρέχει ένα πλήρες λειτουργικό σύστημα, παρά μόνο το πρόγραμμα που του δίνει ο χρήστης, οπότε κάνει emulate όλα τα system calls τα οποία θα προκύψουν με ένα απλό σύστημα το οποίο αποτελείτε μόνο απο την CPU και την μνήμη. Αν είχαμε δώσει σαν όρισμα στην μέθοδο _Root_ ως _full_system = True_, τότε θα έλεγα στον gem5 ότι θα κάνει emulate ένα πλήρες λειτουργικό σύστημα, δηλαδή θα ήταν σε _Excecution Mode_ **Full-System (FS)**. Στην συνέχεια, τρέχει η εντολή

```ruby
    root.system = create(args)
```

η οποία καλεί την μέθοδο _create_ η οποία με την σειρά της καλεί την **SimpleSystem()** η οποία αρχικοποιεί κάποιες παραμέτρους του συστήματος όπως το μέγεθος της γραμμής της cache αλλά, την τάση και την συχνότητα λειτουργίας του συστήματος καθώς και την τάση των Caches όπως φαίνονται παρακάτω:

```ruby
    # Use a fixed cache line size of 64 bytes
    cache_line_size = 64
```
```ruby
    # Create a voltage and clock domain for system components
    self.voltage_domain = VoltageDomain(voltage="3.3V")
    self.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=self.voltage_domain)
```

```ruby
    # Add CPUs to the system. A cluster of CPUs typically have
    # private L1 caches and a shared L2 cache.
    self.cpu_cluster = devices.CpuCluster(self, args.num_cores, args.cpu_freq, "1.2V", *cpu_types[args.cpu])
```

```ruby
    if self.cpu_cluster.memoryMode() == "timing":
    self.cpu_cluster.addL1()
    self.cpu_cluster.addL2(self.cpu_cluster.clk_domain)
    self.cpu_cluster.connectMemSide(self.membus)
```

Ακόμη, η μέθοδος _create_ καλεί και την μέθοδο **get_processes()** η οποία παίρνει τα cmdargs και τα μεταφράζει ώς μια λίστα από processes. Τέλος, καλούνται οι μέθοδοι **m5.instansiate()** και **m5.simulate()** οι οποίες θεμελιώνουν την ιεραρχία της C++ και ξεκινούν την προσομοίωση αντίστοιχα.

### Συνοπτικά

|               | System Info   |
| ------------- | ------------- |
| Voltage       | 3.3V          |
| Frequency     | 1GHz          |

|               | CPU Info      |
| ------------- | ------------- |
| Num. of Cores | 1             |
| Frequency     | 4GHz          |
| Type          | Minor         |
| Voltage       | 1.2V          |
| Mode          | Timing        |

|               | RAM Info      |
| ------------- | ------------- |
| Memory        | 2GB           |
| Channels      | 2             |
| Type          | DDR3_1600_8x8 | 

Τέλος μπορώ να αλλάξώ τη συχνότητα του συστήματος δίνοντας το παρακάτω cmdargs στο script:

```ruby
    --sys-clock= value
```
#### Ερώτημα 2
|  stats.txt    |            meaning                |
| ------------- | --------------------------------- |
| sim_seconds   | Number of seconds simulated       |
| sim_insts     | Number of instructions simulated  |
| host_inst_rate| imulator instruction rate (inst/s)| 

#### Ερώτημα 3
#### A.
Εκτός από το αρχείο εξόδου stats.txt που παράγεται στο τέλος της εξομοίωσης, ο gem5 παράγει
και τα αρχεία config.ini και config.json. Τα αρχεία αυτά παρέχουν πληροφορίες για το σύστημα
που εξομοιώνει ο gem5
Έστω πως το σύστημα έχει ποινή αστοχίας (miss penalty) L1 = 6 cycles και ποινή αστοχίας
(miss penalty) L2 = 50 cycles και 1 cycle cache hit/instruction execution.
Μπαίνοντας στο αρχείο stats.txt βρίσκω τα misses στα **L1 Instruction Cache**,**L1 Data Cache**,	**L2 Cache**
έχω αντίστοιχα 


```ruby
system.cpu_cluster.cpus.icache.overall_misses::.cpu_cluster.cpus.inst          332                       # number of overall misses
system.cpu_cluster.cpus.dcache.overall_misses::.cpu_cluster.cpus.data          179                       # number of overall misses
system.cpu_cluster.l2.overall_misses::total                                    479                       # number of overall misses

```
Επίσης τις συνολικές εντολές που έτρεξαν τις παίρνω από :
```ruby
sim_insts                                        5028                       # Number of instructions simulated
```
Άρα κάντοντας την πράξη το CPI= ((332+179)*6 + 479*50)/5028=5.37

#### Ερώτημα 4
Ο emulator gem5 χρησιμοποιεί διάφορα μοντέλα CPU, κάποια in-οrder και κάποια out-of-order. Τα in-order μοντέλα που χρησιμοποιεί είναι τα **Simple CPU** και **Minor CPU** models.

Το μοντέλο Simple CPU έχει ανανεωθεί πρόσφατα και έχει χωριστεί σε 3 κλάσεις, **BaseSimpleCPU**, **AtomicSimpleCPU** και **TimingSimpleCPU**. 
Το BaseSimpleCPU μοντέλω εξυπηρετεί διάφορους σκοπούς όπως την εκτέλεση συναρτήσεων οι οποίες κάνουν έλεγχω για τυχόν interrupts, κάνει τα fetch requests και αναλαμβάνει και κάποιες post-excecute διεργασίες. Η κλάση BaseSimpleCPU δεν μπορεί να χρησιμοποιηθεί μόνη της καθώς χρειάζεται να κληθούν και μια από τις κλάσεις AtomicSimpleCPU ή TimingSimpleCPU οι οποίες κληρονομούν την κλάση BaseSimpleCPU. Όπως λέει και ο τίτλος το μοντέλο **AtomicSimpleCPU** χρησιμοποιεί _Atomic Memory Access_ όπου είναι μια αρκετά γρήγορη και απλουστευμένη μέθοδος memory accessing, η οποία χρησιμοποιείται για fast forwarding και warming up των caches. Τo μοντέλο Atomic Simple CPU εκτελεί όλα τα operations για ένα instruction μέσα σε 1 κυκλο ρολογιού. Η κλάση AtomicSimpleCPU λοιπόν δημιουργεί ports μεταξύ μνήμης και επεξεργαστή. Η κλάση TimingSimpleCPU έχει ακριβώς την ίδια λειτουργία με την κλάση AtomicSimpleCPU (δηλαδή την διασύνδεση CPU-Cache) με μόνη διαφορά ότι χρησιμοποιεί _timing memory access_. Δηλαδή, μια μέθοδο προσπέλασης μνήμης η οποία είναι αρκετά λεπτομερής και κάνει stall τα cache accesses και περιμένει ACK (Acknowledgment) πρωτού συνεχίσει.

Το μοντέλο **MinorCPU** αποτελεί ένα ευέλικτο μοντέλο in-order CPU που αναπτύχθηκε αρχικά για να υποστηρίζει το Arm ISA, ενώ υποστηρίζει και άλλα ISAs. Το MinorCPU έχει fixed four-stage in-order execution pipeline, ενώ διαθέτει ρυθμιζόμενες δομές δεδομένων και συμπεριφορά εκτέλεσης. Επομένως μπορεί να ρυθμιστεί σε επίπεδο μικρο-αρχιτεκτονικής για να μοντελοποιήσει συγκεκριμένο επεξεργαστή. Το four-stage pipeline περιλαμβάνει fetching lines, decomposition into macro-ops, decomposition of macro-ops into micro-ops και execute.

#### A. 
Για το ερώτημα αυτό αναπτύχθηκε ένα απλό πρόγραμμα σε C που απλά τυπώνει τους αριθμούς από το 0 μέχρι και το δέκα. 


```ruby
#include<stdio.h>

int main()
{int i;
for (i=0; i<=10; i++){
printf("%d \n", i);
}
return 0;
}
```

Για να κάνω compile το αρχείο .c σε εκτελέσιμο που προσδιορίζεται για ARM ISA έπρεπε να τρέξω την παρακάτω εντολή,

```ruby
arm-linux-gnueabihf-gcc --static .Lab_1/script/program.c -o .Lab_1/script/programCompiled
```

Αρχικά τρέχω το πρόγραμμα χρησιμοποιώντας ως CPU την MinorCPU με την παρακάτω εντολή :

```ruby
./build/ARM/gem5.opt -d Lab_1/CPUMinor configs/example/se.py --cpu-type=MinorCPU --caches -c ./script/programCompiled
 
```
Κάποια βασικά αποτελέσματα του simulation φαίνονται παρακάτω:



```ruby
final_tick                                   41177000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                  83500                       # Simulator instruction rate (inst/s)
host_mem_usage                                 667384                       # Number of bytes of host memory used
host_op_rate                                    97732                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.19                       # Real time elapsed on the host
host_tick_rate                              214139312                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       16037                       # Number of instructions simulated
sim_ops                                         18789                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000041                       # Number of seconds simulated
sim_ticks                                    41177000                       # Number of ticks simulated
system.cpu.committedInsts                       16037                       # Number of instructions committed
system.cpu.committedOps                         18789                       # Number of ops (including micro ops) committed
system.cpu.cpi                               5.135250                       # CPI: cycles per instruction
system.cpu.discardedOps                          2174                       # Number of ops (including micro ops) which were discarded before commit
system.cpu.idleCycles                           54668                       # Total number of cycles that the object has spent stopped
system.cpu.ipc                               0.194732                       # IPC: instructions per cycle
system.cpu.numCycles                            82354                       # number of cpu cycles simulated
```
Στη συνέχεια τρέχω την ίδια εντολή αλλά αυτή την φορά για **TimingSimpleCPU** :



```ruby
./build/ARM/gem5.opt -d Lab_1/TimingSimpleCPU configs/example/se.py --cpu-type=TimingSimpleCPU --caches -c ./script/programCompiled

```
Κάποια βασικά αποτελέσματα του simulation φαίνονται παρακάτω

```ruby
final_tick                                   50559000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                 312753                       # Simulator instruction rate (inst/s)
host_mem_usage                                 665596                       # Number of bytes of host memory used
host_op_rate                                   363823                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.05                       # Real time elapsed on the host
host_tick_rate                              989408811                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       15938                       # Number of instructions simulated
sim_ops                                         18583                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000051                       # Number of seconds simulated
sim_ticks                                    50559000                       # Number of ticks simulated
system.cpu.Branches                              3258                       # Number of branches fetched
system.cpu.committedInsts                       15938                       # Number of instructions committed
system.cpu.committedOps                         18583                       # Number of ops (including micro ops) committed
system.cpu.idle_fraction                     0.000000                       # Percentage of idle cycles
system.cpu.not_idle_fraction                 1.000000                       # Percentage of non-idle cycles
system.cpu.numCycles                           101118                       # number of cpu cycles simulated
```

Άν συγκρίνουμε τα αποτελέσματα των δυο μοντέλων ο συνολικός αριθμός των κύκλων ρολογιού του κάθε simulation, δεδομένου ότι και τα δυο μοντέλα έτρεξαν στην ίδια συχνότητα, βλέπουμε ότι το μοντέλο TiminigSimpleCPU εκτελείτε σε 101118 κύκλους μηχανής, ενώ το μοντέλο MinorCPU εκτελείτε σε 82354,, δηλαδή εκτελείτε πιο γρήγορα. Το παραπάνω αποτέλεσμα είναι λογικό καθώς το μοντέλο MinorCPU χρησιμοποιεί τεχνικές pipelinining. Η υλοποίηση όμως μιας τέτοιας μοντελοποίησης, όπως αυτή του pipelining είναι απαιτητική για το σύστημα  και αυτό επαληθεύεται απο την σύγκριση των host_seconts, καθώς βλέπουμε ότι το μοντέλο MinorCPU χρειάστηκε 0.19 sec για να τρέξει στο host machine, ενω το μοντέλο TimingSimpleCPU χρειάστηκε 0.05sec.


### B.
Πρώτα κάνουμε προσομείωση με συχνότητα 500MHz για τους δυο μοντέλα CPU
MinorCPU:
```ruby
./build/ARM/gem5.opt -d Lab_1/CPUMinor500MHz configs/example/se.py --cpu-type=MinorCPU --cpu-clock="500MHz" --caches -c ./script/programCompiled
```
Κάποια βασικά αποτελέσματα του simulation φαίνονται παρακάτω

```ruby
inal_tick                                   78486000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                 120469                       # Simulator instruction rate (inst/s)
host_mem_usage                                 667384                       # Number of bytes of host memory used
host_op_rate                                   141009                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.13                       # Real time elapsed on the host
host_tick_rate                              588925102                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       16037                       # Number of instructions simulated
sim_ops                                         18789                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000078                       # Number of seconds simulated
sim_ticks                                    78486000                       # Number of ticks simulated
system.cpu.committedInsts                       16037                       # Number of instructions committed
system.cpu.committedOps                         18789                       # Number of ops (including micro ops) committed
system.cpu.cpi                               2.447029                       # CPI: cycles per instruction
system.cpu.discardedOps                          2159                       # Number of ops (including micro ops) which were discarded before commit
system.cpu.idleCycles                           11982                       # Total number of cycles that the object has spent stopped
system.cpu.ipc                               0.408659                       # IPC: instructions per cycle
system.cpu.numCycles                            39243                       # number of cpu cycles simulated
```

Για το TimingSimple μοντέλο τρέχω:

```ruby
./build/ARM/gem5.opt -d Lab_1/TimingSimpleCPU_500MHz configs/example/se.py --cpu-type=TimingSimpleCPU --cpu-clock="500MHz" --caches -c ./script/programCompiled
```

Κάποια βασικά αποτελέσματα του simulation φαίνονται παρακάτω:
```ruby
final_tick                                  124958000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                 306055                       # Simulator instruction rate (inst/s)
host_mem_usage                                 665340                       # Number of bytes of host memory used
host_op_rate                                   355800                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.05                       # Real time elapsed on the host
host_tick_rate                             2390850961                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       15938                       # Number of instructions simulated
sim_ops                                         18583                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000125                       # Number of seconds simulated
sim_ticks                                   124958000                       # Number of ticks simulated
system.cpu.Branches                              3258                       # Number of branches fetched
system.cpu.committedInsts                       15938                       # Number of instructions committed
system.cpu.committedOps                         18583                       # Number of ops (including micro ops) committed
system.cpu.idle_fraction                     0.000000                       # Percentage of idle cycles
system.cpu.not_idle_fraction                 1.000000                       # Percentage of non-idle cycles
system.cpu.numCycles                            62479                       # number of cpu cycles simulated
system.cpu.numWorkItemsCompleted                    0                       # number of work items this cpu completed
system.cpu.numWorkItemsStarted                      0                       # number of work items this cpu started
system.cpu.num_busy_cycles               62478.999500                       # Number of busy cycles
```

Αυτό που παρατηρώ είναι ότι, όπως είναι λογικό άλλωστε με την μείωση της συχνότητας της CPU, αυξήθηκε ο συνολικός χρόνος εκτέλεσης του κάθε μοντέλου ξεχωριστά. Αυτό, όμως που αξίζει να σημειωθεί είναι ότι η μείωση της συχνότητας της CPU είχε πολύ μεγαλύτερο impact στο μοντέλο TimingSimpleCPU, εν αντιθέση με το μοντέλο MinorCPU,λόγω της τεχνικής pipeline που χρησιμοποιεί το μοντέλο MinorCPU.



Τέλος θα αλλάξω την τεχνολογία της μνήμης μας από DDR3_1600_8x8 (που είναι η default τιμή) σε DDR3_2133_8x8 και θα εξετάσω τα αποτελέσματα. Πάλι, παραθέτονται οι εντολές που έτρεξαν στο τερματικό και τα αντίστοιχα στατιστικά του εκάστοτε simulation για τα διαφορετικά μοντέλα CPU.

MinorCPU:
```ruby
./build/ARM/gem5.opt -d Lab_1/MinorCPU_mem_DDR3_2133_8x8 configs/example/se.py --cpu-type=MinorCPU --mem-type=DDR3_2133_8x8 --caches -c ./script/programCompiled
```

```ruby
final_tick                                   39528000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                 125621                       # Simulator instruction rate (inst/s)
host_mem_usage                                 667388                       # Number of bytes of host memory used
host_op_rate                                   146979                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.13                       # Real time elapsed on the host
host_tick_rate                              309151463                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       16037                       # Number of instructions simulated
sim_ops                                         18789                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000040                       # Number of seconds simulated
sim_ticks                                    39528000                       # Number of ticks simulated
system.cpu.committedInsts                       16037                       # Number of instructions committed
system.cpu.committedOps                         18789                       # Number of ops (including micro ops) committed
system.cpu.cpi                               4.929600                       # CPI: cycles per instruction
system.cpu.discardedOps                          2173                       # Number of ops (including micro ops) which were discarded before commit
system.cpu.idleCycles                           51362                       # Total number of cycles that the object has spent stopped
system.cpu.ipc                               0.202856                       # IPC: instructions per cycle
system.cpu.numCycles                            79056                       # number of cpu cycles simulated
```

TimingSimpleCPU

```ruby
./build/ARM/gem5.opt -d Lab_1/TimingSimpleCPU_mem_DDR3_2133_8x8 configs/example/se.py --cpu-type=TimingSimpleCPU  --mem-type=DDR3_2133_8x8 --caches -c ./script/programCompiled
```


```ruby
final_tick                                   49715000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                                 364095                       # Simulator instruction rate (inst/s)
host_mem_usage                                 665336                       # Number of bytes of host memory used
host_op_rate                                   423381                       # Simulator op (including micro ops) rate (op/s)
host_seconds                                     0.04                       # Real time elapsed on the host
host_tick_rate                             1132070385                       # Simulator tick rate (ticks/s)
sim_freq                                 1000000000000                       # Frequency of simulated ticks
sim_insts                                       15938                       # Number of instructions simulated
sim_ops                                         18583                       # Number of ops (including micro ops) simulated
sim_seconds                                  0.000050                       # Number of seconds simulated
sim_ticks                                    49715000                       # Number of ticks simulated
system.cpu.Branches                              3258                       # Number of branches fetched
system.cpu.committedInsts                       15938                       # Number of instructions committed
system.cpu.committedOps                         18583                       # Number of ops (including micro ops) committed
system.cpu.idle_fraction                     0.000000                       # Percentage of idle cycles
system.cpu.not_idle_fraction                 1.000000                       # Percentage of non-idle cycles
system.cpu.numCycles                            99430                       # number of cpu cycles simulated

```
Παρατηρώ ότι μειώθηκαν οι χρόνοι εκτέλεσης από την αρχική μας περίπτωση. Αυτό είναι λογικό αφού αρχικά είχαμε DDR3_1600_8x8 : (1.6 x 8 x 8 / 8 = 12.8 GBps) και τώρα DDR3_2133_8x8 : (2.133 x 8 x 8 / 8 = 17.0 GBps).


### Κριτική Εργασίας

Αρχικά, όσον αφορά την εγκατάσταση του simulator gem5, αντιμετώπισα πρόβλημα κατα τη διάρκεια του build του gem5,λόγω διαφορετικής έκδοσης ubuntu συγκριτικά με την προτεινόμενη, επείτα όμως από επικοινωνία με τους διδάσκοντες λύθηκε εύκολα το πρόβλημα. Αναφορικά με το πρακτικό κομμάτι της εργασίας και τα προγράμματα που έπρεπε να τρέξω, θεωρώ ότι ήταν αρκετά ενδιαφέρον καθώς μπορέσαμε να δώ στην πράξη πράγματα. Το πιο σημαντικό ήταν η ασχολία με την εργασία με βοήθησε όχι μονο να καταλάβω καλύτερα τις έννοιες του μαθήματος που μέχρι τώρα τις είχα δει μόνο σε θεωρητικό επίπεδο,αλλά μου δόθηκε και η δυνατότητα να ασχοληθώ με το git και τη
γλώσσα Μarkdown που μέχρι τώρα δεν τα είχα χρησιμοποιήσει.
