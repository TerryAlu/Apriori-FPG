IBM Quest Data Generator
========================

This project is modified from [halfvim/quest](https://github.com/halfvim/quest). 
The output format is changed and a transaction is represented in a row.
Besides, -ntrans and -nitems values won't times 1000. This will allow us to conduct experiment with smaller data size.

The transaction file is named \<fname\>.data. Each row represents a transaction, and items in a row are seperated by comma.
An item is identified by a unique integer.

```
item1,item2,item3...
item2,item3,item5...
```

Notice: Number of transactions in \<fname\>.data slightly smaller than the value of -ntrans sometimes.

Compile with *Microsoft Visual Studio* in Windows or *make* in Linux.

Usage:
```
Command Line Options:
  -ntrans number_of_transactions (default: 1000000)
  -tlen avg_items_per_transaction (default: 10)
  -nitems number_of_different_items) (default: 100000)

  -npats number_of_patterns (default: 10000)
  -patlen avg_length_of_maximal_pattern (default: 4)
  -corr correlation_between_patterns (default: 0.25)
  -conf avg_confidence_in_a_rule (default: 0.75)

  -fname <filename> (write to filename.data and filename.pat)
  -ascii (default: True)
  -randseed # (reset seed used generate to x-acts; must be negative)
  -version (to print out version info)
```

To get command-line help,
```
executable_filename lit -help
```

Examples: Generate test.data and test.pat
```
./gen lit -ntrans 100 -tlen 5 -nitems 20 -npats 5 -fname test
```


