CS 499: Software Security, Spring 2018

PROF: Alex Groce (github or my web page at https://www.cefns.nau.edu/~adg326/ will give the scoop on me, Google Scholar can tell you most of what I "do")

OFFICE HOURS:  Wed 12:15pm, SICCS 208

Class discussion via slack, assignments submitted via email drop posted in slack

3 assignments + 1 in-class test (20% of grade each)

LIVING SYLLABUS:

- Intro to Software Security (READ ANDERSON)
  - Security is about CIA
      - Confidentiality
      - Integrity
      - Availability
    - (of information)
  - Security is often about BUGS
  - A bug + a motive = probability of trigger being low no longer helps
- Protocols, key/encryption as black box basics
  - Needham-Schroeder Public Key weakness
  - Protocol fuzzing
- Static analysis
  - Basics: dead code, crying wolf, prioritizing warnings, pointers are hard
  - Chess and McGraw overview
  - Comparing Python tools (picky configurable pylint vs. friendly pyflakes)
  - Uno:  uninitialized variables, null pointers, out-of-bounds access
    - Basic dataflow
    - Automata composition to find def-use
  - Building a simple static analysis tool
    - Parse
    - Build annotated CFG
    - Walk the annotated CFG
    
    - Reporting warnings more succinctly
    - Limiting depth to which loops are unwound
    
    - Taint analysis
      - Simple version of SQL injection
    - Side channels

- Dynamic analysis
  - Intro to afl-fuzz
  - Intro to TSTL (library testing)

  - Grammar-based fuzzing and target selection criteria
    - Solidity compiler example (fuzz in a way nobody has fuzzed
    before)
	- Pick targets of actual value, for white hat or black hat purposes!

  - Practical fuzzing combined with "manual static analysis"

  - Building exploits

  - Kinds of dynamic analysis (stuff to check for!) esp. useful in security
    - "Crashes" (obviously)
    - Memory safety more generally:  bad access without crash
    - Taint
    - Determinism
    - Nondeterminism
    - Race conditions

  - SQL injection attacks
    - Dynamic analysis paper, concolic testing, specialized queries,
  working backwards from a failure 
