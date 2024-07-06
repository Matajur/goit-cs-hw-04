# Tier 2. Module 1: Computer Systems and Their Fundamentals

## Topic 7 - Basics of multi-threaded programming
## Topic 8 - Basics of multiprocess programming
## Homework

### Technical description

Develop a program that processes and analyzes text files in parallel to search for defined keywords. Create two versions of the program: one using the `threading` module for multithreaded programming, and the other using the `multiprocessing` module for multiprocess programming.

### Instruction

1. Implementation of a multithreaded approach to file processing (using `threading`):

* Split the list of files between different threads.
* Each thread must search its own set of files for the given keywords.
* Collect and output search results from all streams.

2. Implementation of a multiprocess approach to file processing (using `multiprocessing`):

* Split the list of files between different processes.
* Each process must process its own portion of the files, looking for keywords.
* Use a data exchange mechanism (for example, via `Queue`) to collect and display search results.

### Acceptance criteria

- Implemented multi-threaded and multi-process approaches to file processing.
- Effective distribution of files between threads/processes is ensured.
- The code measures and outputs the execution time for each of the versions.
- Correct handling of errors and exceptions is ensured, especially when working with the file system.
- Both versions of the program return a dictionary where the key is the search word and the value is a list of file paths where the word is found.
