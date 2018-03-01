from subprocess import Popen, PIPE, STDOUT
import random
import sys

target = 'cat'

RUNS = 1000
MAX_LENGTH = 1000
VALUES = [chr(i) for i in range(0,255)]

failed = False

print "="*79
print "AMERICAN FURRY PLOP, THE WORLD'S SIMPLEST FUZZER"
print "="*79

print "FUZZING",target

for i in range(0,RUNS):
    if (i%100) == 0:
        print ".",
        sys.stdout.flush()
    data = b''
    length = random.randrange(0,MAX_LENGTH)
    while len(data) < length:
        data += random.choice(VALUES)
    p = Popen([target], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
    cat_stdout = p.communicate(input=data)[0]
    if p.returncode != 0:
        print "FAILURE IN RUN #",i
        print "  RETURN CODE:", p.returncode
        failed = True
        print "  WRITING FAILED PROCESS OUTPUT TO failure.txt"
        with open('failure.txt','w') as f:
            f.write(cat_stdout)
        print "  WRITING TRIGGERING INPUT DATA TO data"
        with open('data','wb') as f:
            f.write(data)            
        break
    
print

if not failed:
    print "RAN",RUNS,"TESTS WITH NO FAILURES"
