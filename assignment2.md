Your task:


- find a dynamic analysis tool of interest

- find a target program or library of interest

Post to the #assignment2claims channel in slack a tuple of the form:


(

- NAU login - e.g. adg326 for me,
- GitHub repo or other location of open source project, including version
- Tool you used

)

Only one person can analyze a particular program of library with a particular tool, so if you want a popular choice, you need to stake it early!

Unlike last time, this assignment is not strictly limited to the
actual code you analyze, in that if you cannot find a real bug in the
program, you should introduce a (non-trivial, does not occur on all
inputs) bug to the code!  If you find a real bug, you can skip this
part.

An alternative to this is to use an older version of a program with a
known bug, and show how to find that bug.

For the assignment, send to our secret class email drop an email with subject 499 ASSIGNMENT 2 and attach a zip file with name yourNAUlogin.assign2.zip (e.g. adg326.assign2.zip for me) with:

- text file README.txt with the same info as the tuple above, plus a
  final item, what source file you modified (if any)
- if you modified the program to introduce a bug, a diff (diff.txt) of
  the affected source file
- generated tests / input files for the program analyzed, your writeup
  should identify any test(s) exposing a real or introduced-by-you bug
- a two to three page pdf writeup of your understanding of the results, what's interesting, any real bugs found, etc.

Bonus points for:

- the bug found/introduced being a real security flaw, vs. just a
  plain ol' bug
- using multiple tools and comparing results
- connecting results to technical ideas from dynamic analysis (you can
  see it never covered the buggy code, because of this coverage tool
  output, etc.)

DUE DATE IS APRIL 10TH
