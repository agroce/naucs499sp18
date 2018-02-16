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

def WARNING(b, msg):
    print msg

def findDeclIssues(cfg, node, decls, useds, path):
    (name, data, succ) = cfg[node]
    decld = []
    used = []
    if data != None:
        if "use" in data:
            used = data["use"]
            for u in used:
                if u not in decls:
                    WARNING (False, u+" used w/o decl in " + name + ": " + repr(path))
        if "def" in data:
            defd = data["def"]
            for d in defd:
                if d not in decls:
                    WARNING (False, d+" defd w/o decl in " + name + ": " + repr(path))
        if "decl" in data:
            decld = data["decl"]
            for d in decld:
                if d in decls:
                    WARNING (False, d+" decld TWICE in " + name + ": " + repr(path))                
    for s in succ:
        sf = filter(lambda p: p == s, path)
        if len(sf) < K:
            findDeclIssues(cfg, s, decls + decld, useds + used, path + [s])
            
    if len(succ) == 0:
        for d in decls:
            if d not in useds:
                WARNING (False, d+" decld but never used in " + name + ": " + repr(path))

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
                    WARNING (False, u+" used w/o def in " + name + ": " + repr(path))
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

ll.run(P,{})
        

