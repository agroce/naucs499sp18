from lark import Lark

parser = Lark(r"""
    var: WORD
    int: SIGNED_NUMBER

    expr: "(" expr ")"
          | int
          | user
          | var
          | add
          | sub
          | mul
          | div
          | lt
          | gt
          | eq
          | sanitize

    add: expr "+" expr
    sub: expr "-" expr
    mul: expr "*" expr
    div: expr "/" expr
    user: "user!"
    sanitize: "sanitize" expr

    lt: expr "<" expr
    gt: expr ">" expr
    eq: expr "=" expr

    decl: "int" var
    assign: var ":=" expr
    cond: "if" expr block "else" block
    loop: "while" expr block
    print: "print" expr
    secure: "SECURE" expr
    skip: "skip"

    comment: "//" stmt

    stmt: decl ";"
          | assign ";"
          | cond ";"
          | loop ";"
          | print ";"
          | skip ";"
          | secure ";"
          | comment

    block: "{" stmt+ "}"

    program: block

    %import common.SIGNED_NUMBER
    %import common.WORD
    %import common.WS
    %ignore WS

    """, start='program')

def exprToStr(expr):
    if expr.data == "expr" and expr.children[0].data == "expr":
        return "(" + exprToStr(expr.children[0]) + ")"
    elif expr.data == "expr":
        return exprToStr(expr.children[0])
    elif expr.data == "sanitize":
        return "sanitize " + exprToStr(expr.children[0])    
    elif expr.data == "var":
        v = expr.children[0][0]
        return str(v)
    elif expr.data == "int":
        return str(int(expr.children[0]))
    elif expr.data == "add":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " + " + ev2
    elif expr.data == "sub":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " - " + ev2
    elif expr.data == "mul":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " * " + ev2
    elif expr.data == "div":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " / " + ev2
    elif expr.data == "lt":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " < " + ev2
    elif expr.data == "gt":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " > " + ev2
    elif expr.data == "eq":
        ev1 = exprToStr(expr.children[0])
        ev2 = exprToStr(expr.children[1])
        return ev1 + " == " + ev2
    elif expr.data == "user":
        return "user!"
    else:
        assert False,"Unexpected item in expression!"

def eval(expr, store):
    if expr.data == "expr":
        return eval(expr.children[0], store)
    if expr.data == "sanitize":
        return eval(expr.children[0], store)     
    elif expr.data == "var":
        v = expr.children[0][0]
        if v not in store:
            assert False,v+" is not in the store!"
        ev = store[v]
        if ev == None:
            assert False,v+" not initialized!"
        return store[v]
    elif expr.data == "int":
        return int(expr.children[0])
    elif expr.data == "add":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 + ev2
    elif expr.data == "sub":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 - ev2        
    elif expr.data == "mul":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 * ev2
    elif expr.data == "div":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 / ev2
    elif expr.data == "lt":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 < ev2
    elif expr.data == "gt":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 > ev2
    elif expr.data == "eq":
        ev1 = eval(expr.children[0], store)
        ev2 = eval(expr.children[1], store)
        return ev1 == ev2
    elif expr.data == "user":
        return 3
    else:
        assert False,"Unexpected item in expression!"

def parse(program):
    return parser.parse(program)

def run(parsed, store):
    if parsed.data == "program":
        run(parsed.children[0], store)
    elif parsed.data == "block":
        for s in parsed.children:
            run(s, store)
    elif parsed.data == "stmt":
        s = parsed.children[0]
        stype = s.data
        if stype == "decl":
            v = (s.children[0].children[0])[0]
            assert v not in store
            store[v] = None
        elif stype == "assign":
            v = (s.children[0].children[0])[0]
            assert v in store
            e = s.children[1]
            ev = eval(e, store)
            store[v] = ev
        elif stype == "cond":
            e = s.children[0]
            ev = eval(e, store)
            if ev:
                run(s.children[1], store)
            else:
                run(s.children[2], store)
        elif stype == "loop":
            e = s.children[0]
            ev = eval(e, store)
            if ev:
                run(s.children[1], store)
                run(parsed, store)
        elif stype == "print":
            e = s.children[0]
            ev = eval(e, store)
            print(ev)
        elif stype == "secure":
            e = s.children[0]
            ev = eval(e, store)
            print("I AM DOING A VERY IMPORTANT SECURITY THING WITH",ev)

def CFG(parsed):
    theCFG = {}
    theCFG["<init>"] = ("<init>", None, [])
    return buildCFG(parsed, theCFG, "<init>")[1]

def newNodeGen():
    i = 0
    while True:
        yield "S" + str(i).zfill(8)
        i += 1
        
nodeGen = newNodeGen()

def newNode():
    return next(nodeGen)
        
def used(expr):
    if expr.data == "expr":
        return used(expr.children[0])
    if expr.data == "sanitize":
        return used(expr.children[0])    
    elif expr.data == "var":
        v = expr.children[0][0]
        return [v]
    elif expr.data == "int":
        return []
    elif expr.data in ["add","mul","sub","div","lt","gt","eq"]:
        ev1 = used(expr.children[0])
        ev2 = used(expr.children[1])
        return ev1 + ev2
    elif expr.data == "user":
        return ["user!"]
    else:
        assert False,"Unexpected item in expression!"

def sanitized(expr):
    if expr.data == "expr":
        return sanitized(expr.children[0])
    if expr.data == "sanitize":
        return used(expr.children[0])        
    elif expr.data == "var":
        v = expr.children[0][0]
        return []
    elif expr.data == "int":
        return []
    elif expr.data in ["add","mul","sub","div","lt","gt","eq"]:
        ev1 = sanitized(expr.children[0])
        ev2 = sanitized(expr.children[1])
        return ev1 + ev2
    elif expr.data == "user":
        return []
    else:
        assert False,"Unexpected item in expression!"          

def buildCFG(parsed, cfg, parent):
    if parsed.data == "program":
        (exit, cfg) = buildCFG(parsed.children[0], cfg, parent)
        ename = newNode() + " (exit)"
        cfg[ename] = ("<exit>",None,[])
        (_,_,esuccs) = cfg[exit]
        esuccs.append(ename)
        return (ename, cfg)
    elif parsed.data == "block":
        for s in parsed.children:
            (exit, cfg) = buildCFG(s, cfg, parent)
            parent = exit
        return (parent, cfg)
    elif parsed.data == "stmt":
        s = parsed.children[0]
        stype = s.data
        name = newNode()
        (_,_,psucc) = cfg[parent]
        psucc.append(name)
        if stype == "comment":
            cfg[name] = ("comment",None,[])
            return (name, cfg)        
        if stype == "decl":
            v = (s.children[0].children[0])[0]
            cfg[name] = ("decl",{"decl":[v]},[])
            return (name, cfg)
        elif stype == "assign":
            v = (s.children[0].children[0])[0]
            e = s.children[1]
            eused = used(e)
            esanitized = sanitized(e)
            cfg[name] = ("assign",{"def":[v],"use":eused,
                                   "san":esanitized,
                                   "val":exprToStr(e)},[])
            return (name, cfg)
        elif stype == "cond":
            e = s.children[0]
            b1 = s.children[1]
            b2 = s.children[2]
            eused = used(e)
            cfg[name] = ("cond",{"cond":exprToStr(e),"use":eused},[])            
            (exit1, cfg) = buildCFG(b1, cfg, name)
            (exit2, cfg) = buildCFG(b2, cfg, name)
            mname = newNode()
            cfg[exit1][2].append(mname)
            cfg[exit2][2].append(mname)
            msucc = []
            cfg[mname] = ("merge",None,[])
            return (mname, cfg)
        elif stype == "loop":
            e = s.children[0]
            b = s.children[1]
            eused = used(e)            
            cfg[name] = ("loop",{"cond":exprToStr(e),"use":eused},[])            
            (exit, cfg) = buildCFG(b, cfg, name)
            (_, _, esucc) = cfg[exit]
            esucc.append(name)
            return (name, cfg)
        elif stype == "print":
            e = s.children[0]
            eused = used(e)
            cfg[name] = ("print",{"use":eused},[])
            return (name, cfg)
        elif stype == "secure":
            e = s.children[0]
            eused = used(e)
            esanitized = sanitized(e)
            cfg[name] = ("secure",{"use":eused,"san":esanitized},[])
            return (name, cfg)          
        elif stype == "skip":
            cfg[name] = ("skip",{},[])
            return (name, cfg)
