# Testability project

In this project, we want to read bench file and create a network of gate and then inject values into input terminals and calculate gate result in each layer until we reach to output terminals.

This project has 2 phases as follows:

1. In phase one, we perform **Deductive Fault Simulation** to find s-a faults in each wire.
2. In the second phase, by the means of D**eductive Fault Simulation**, first generate F**ault Dictionary** file(in `result_files` directory) and then use fault equivalent to perform **Fault collapse** to generate fault dictionary that shows **Essential Test Vectors** (Also in the `result_files` directory).

*Note: To generate fault dictionary, we need to inject  2 <sup>n</sup> test vectors (Exhaustive manner). So the bench files (except c17.bench) has many input terminals, so we generate sample bench files in `my_bench_files` directory to perform our test.*

---

To run this project, follow these instructions:

```
pip install -r requirements.txt
python main.py
```
