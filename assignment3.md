Your task:

- find a REAL SECURITY-RELEVANT BUG of interest, discovered using
  either dynamic or static analysis, and describe both the bug and how
  it was found

- write up a 3 page (12 point font, 1 inch margins, single spaced)
  description of the bug.  Relevant graphics (memory layout, screens
  showing the failure in action, etc. are most welcome.  Try to tie
  the bug and its discovery to ideas of dynamic and static analysis in
  class, and explain the security implications:  how does the bug
  affect C I and/or A?  How critical do you think this bug was?  Can
  you find out how long the bug was present in deployed systems before
  being detected and corrected?

You will look for a bug detected by static or dynamic analysis
depending on the md5 hash of your login.  For me, this is:

```
> echo "adg326" | md5
e39b71a749392be89e61ae12fea9543a
```

The final 0-9 digit is a 3, which is odd, so I would write about
static analysis.  If you are even, write about dynamic analysis.

For the assignment turnin, again, send to our secret class email drop an email with
subject 499 ASSIGNMENT 3 and attach a PDF (I will no longer take Word
doc, folks!) file with your 3 page
writeup.  The writeup must include at least:

1.  Your name and NAU ID, of course
2.  A URL to the report on the detection of the bug
3.  A discussion of the bug-detection methods and static or dynamic
    analysis tools used

DUE DATE IS APRIL 24TH
