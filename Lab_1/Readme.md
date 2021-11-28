# Computer Architecture Lab 1
## Ομάδα 13
### Νένος Δημήτρης 9012 dimineno@ece.auth.gr

#### Ερώτημα 1

Στο 1ο ερώτημα εκτελέσαμε ένα απλό πρόγραμμα το οποίο εμφανίζει στην έξοδο του συστήματος (stdout) την έκφραση **Hello World!**.
Η εκτέλεση του προγράμματος γίνετα με την εντολή

`$ build/ARM/gem5.opt -d results/hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"` 

, δεδομένου ότι βρισκόμαστε στο _gem5 directory_. Η εντολή αυτή λεέι ότι θα κάνουμε build με τον simulator _gem5.opt_ με **guest architecture ARM**, στην συνέχεια χρησιμοποιόυμε το flag **-d** για να ανακατευθύνουμε το **output** του προγράμματος στο directory results/hello_result. Στην συνέχεια, δίνουμε το script το οποίο θέλουμε να τρέξουμε (_starter_se.py_) . Τέλος, δίνουμε δύο **cmdargs** στο script, το ένα είναι ο τύπος cpu που θέλουμε να χρησιμοποιήσουμε (minor CPU) και το άλλο είναι το εκτελέσιμο binary αρχείο που θέλουμε να τρέξει το script (hello).


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

Η διαδικασία ανάθεσης των cmdargs στις μεταβλητές του script γίνεται με την μέθοδο _add_argument()_ η οποία αναθέτει το binary εκτελέσιμο _hello_ και το cpu type _minor_. Βλέπουμε επίσης, ότι τα υπόλοιπα χαρακτηρηστικά του simulator όπως _CPU Frequency_, _Number of Cores_, _Memory_Type_ κλπ εφόσον δεν δίνονται σαν cmdargs παίρνουν τις _default_ τιμές τους. Πιο συγκεκριμένα, η default συχνότητα ρολογιού είναι **4GHz**, ο αριθμός των πυρήνων του επεξεργαστή είναι **1**, ενώ ο τύπος RAM είναι **DDR3_1600_8X8** με 2 κανάλια (δηλ. **dual port**) και μέγεθος **2GB**. Όσον αφορά τον τύπο της CPU βλέπουμε ότι αναθέτετε ο τύπος _minor_ μέσω των παρακάτω εντολών

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

η οποία δηλώνει το _Excecution Mode_ του _gem5_ ως **System-Call Emulation (SE)**, δηλαδή ορίζει ότι ο gem5 δεν τρέχει ένα πλήρες λειτουργικό σύστημα, παρά μόνο το πρόγραμμα που του δίνει ο χρήστης, οπότε κάνει emulate όλα τα system calls τα οποία θα προκύψουν με ένα απλό σύστημα το οποίο αποτελείτε μόνο απο την CPU και την μνήμη. Αν είχαμε δώσει σαν όρισμα στην μέθοδο _Root_ ως _full_system = True_, τότε θα λέγαμε στον gem5 ότι θα κάνει emulate ένα πλήρες λειτουργικό σύστημα, δηλαδή θα ήταν σε _Excecution Mode_ **Full-System (FS)**. Στην συνέχεια, τρέχει η εντολή

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

Τέλος μπορούμε να αλλάξουμε τη συχνότητα του συστήματος δίνοντας το παρακάτω cmdargs στο script:

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
Μπαίνοντας στο αρχείο stats.txt μπορούμε να βρούμε τα misses στα **L1 Instruction Cache**,**L1 Data Cache**,	**L2 Cache**
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
