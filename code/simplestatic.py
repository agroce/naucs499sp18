import littlelanguage as ll

P = ll.parse(
"""
   {
    int x;
    int y;
    y := 4;
    x := y*(3+y);
    print x;
    if (x > 20) {
       print 10000;
    } else {
       print 20000;
    };
    if (x > 40) {
       print 30000;
    } else {
       print 40000;
    };
    while (x > 0) {
       int z;
       z := 3;
       print x;
       x := x - 1;
       if (x < 100) {
          y := 3;
       } else {
          y := 4;
       };
    };
   }
""")

K = 2

warnings = {}

def getWarnings():
    return warnings

def printWarnings():
    allWarnings = warnings.iteritems()
    sortedWarnings = sorted(allWarnings, key = lambda w:w[0][1])
    for (mn, path) in sortedWarnings:
        print "*"*50
        (msg, node) = mn
        print msg, " IN ", node, ":", path    

def WARNING(msg, node, path):
    if (msg, node) in warnings:
        if len(path) < len(warnings[(msg,node)]):
            warnings[(msg,node)] = path
    else:
        warnings[(msg,node)] = path        

def findDeclIssues(cfg, node, decls, useds, path):
    (name, data, succ) = cfg[node]
    decld = []
    used = []
    if data != None:
        if "use" in data:
            used = data["use"]
            for u in used:
                if u not in decls:
                    WARNING(u + " used w/o decl", node, path)
        if "def" in data:
            defd = data["def"]
            for d in defd:
                if d not in decls:
                    WARNING(d + " defd w/o decl", node, path)
        if "decl" in data:
            decld = data["decl"]
            for d in decld:
                if d in decls:
                    WARNING(d + " decld TWICE", node, path)                
    for s in succ:
        sf = filter(lambda p: p == s, path)
        if len(sf) < K:
            findDeclIssues(cfg, s, decls + decld, useds + used, path + [s])
            
    if len(succ) == 0:
        for d in decls:
            if d not in useds:
                WARNING(d + " decld but never used", node, path)

def checkDecls(cfg):
    findDeclIssues(cfg,"<init>",[],[],["<init>"])

def findBadUseDef(cfg, node, defs, path):
    (name, data, succ) = cfg[node]
    defd = []
    if data != None:
        if "use" in data:
            used = data["use"]
            for u in used:
                if u not in defs:
                    WARNING(u + " used w/o def", node, path)
        if "def" in data:
            defd = data["def"]
    for s in succ:
        sf = filter(lambda p: p == s, path)
        if len(sf) < K:        
            findBadUseDef(cfg, s, defs + defd, path + [s])

def checkUseDef(cfg):
    findBadUseDef(cfg,"<init>",[],["<init>"])

cfg = ll.CFG(P)
for node in sorted(cfg.keys()):
    (name, data, succ) = cfg[node]
    print node,":",name,data
    for s in succ:
        print "  --> ",s

checkUseDef(cfg)
checkDecls(cfg)

if len(getWarnings()) == 0:
    ll.run(P,{})
else:
    print "STATIC ANALYSIS WARNINGS: DO NOT EXECUTE!"
    printWarnings()
        

