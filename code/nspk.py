import random

def analyze(msg):
	if msg not in known:
		known.append(msg)
	if type(msg) == tuple:
		for c in msg:
			analyze(c)
	if type(msg) == list:
		if msg[1] in known: # need to know key to decrypt!
			analyze(msg[0])

def send(msg,who):
    log.append((who,msg))
    sent.append(msg)
    analyze(msg)

def match(msg,m):
    if (type(msg) == tuple) or (type(msg) == list):
        l = len(msg)
        if len(m) != l:
            return False
        for i in range(0,l):
            if not (match(msg[i],m[i])):
                return False
        return True
    elif msg == "*":
        return True
    return msg == m
    
def matches(msg,msgs):
    for m in msgs:
        if match(msg,m):
            return m
    return False

    
RUNS = 1000
DEPTH = 1000

A = "A"
B = "B"
I = "I"
PK = {}
PK[A] = "PKA"
PK[B] = "PKB"
PK[I] = "PKI"

NA = None
NB = None

for i in range(0,RUNS):
    print i
    sent = []
    log = []
    known = [PK[I],A,B,I]
    Astate = 0
    Bstate = 0
    for j in range(0,DEPTH):
        who = random.choice([A,B,I])
        if who == A:
            if Astate == 0:
                R = random.choice([B,I])
                NA = "N"+str(random.random())
                msg = (A,R,[(NA,A),PK[R]])
                send(msg,who)
                Astate = 1
            elif Astate == 1:
                msg = (R,A,[(NA,"*"),PK[A]])
                matched = matches(msg,sent)
                if matched != False:
                    NR = matched[2][0][1]
                    Astate = 2
            elif Astate == 2:
                msg = (A,R,[NR,PK[R]])
                send(msg,who)
                #print "A finished protocol with",R
                Astate = 0
        elif who == B:
            if Bstate == 0:
                msg = (A,B,[(NA,A),PK[B]])
                if msg in sent:
                    Bstate = 1
            elif Bstate == 1:
                NB = "N"+str(random.random())
                msg = (B,A,[(NA,NB),PK[A]])
                send(msg,who)
                Bstate = 2
            elif Bstate == 2:
                msg = (A,B,[NB,PK[B]])
                if msg in sent:
                    #print "B finished protocol with A(?)"                    
                    if (NB in known):
                        for i in range(0,len(log)):
                            print i,log[i][0],":",log[i][1]
                        assert(False)
                    Bstate = 0
        elif who == I:
            msg = "FOO"
            while msg in sent:
                first = "A"
                second = "A"
                while first == second:
                    first = random.choice([A,B,I])
                    second = random.choice([A,B,I])
                third = random.choice(known)
                fourth = random.choice(known)
                #key = PK[random.choice([A,B])]
                key = PK[second]
                msg = random.choice([(first,second,[third,key]),
                                        (first,second,[(third,fourth),key])])
            send(msg,who)
