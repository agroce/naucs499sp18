from lark import Lark

i = -1

parser = Lark(r"""
    var: WORD
    int: SIGNED_NUMBER

    expr: "(" expr ")"
          | int
          | var
          | add
          | sub
          | mul
          | div
          | lt
          | gt
          | eq

    add: expr "+" expr
    sub: expr "-" expr
    mul: expr "*" expr
    div: expr "/" expr

    lt: expr "<" expr
    gt: expr ">" expr
    eq: expr "=" expr

    decl: "int" var
    assign: var ":=" expr
    cond: "if" expr block "else" block
    loop: "while" expr block
    print: "print" expr

    comment: "//" stmt

    stmt: decl ";"
          | assign ";"
          | cond ";"
          | loop ";"
          | print ";"
          | comment

    block: "{" stmt+ "}"

    program: block

    %import common.SIGNED_NUMBER
    %import common.WORD
    %import common.WS
    %ignore WS

    """, start='program')

def eval(expr, store):
    if expr.data == "expr":
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
            print ev          

def CFG(parsed):
    theCFG = {}
    theCFG["<init>"] = ("<init>", None, [])
    return buildCFG(parsed, theCFG, "<init>")[1]

def newNodeGen():
    i = 0
    while True:
        yield "S" + str(i).zfill(4)
        i += 1
        
nodeGen = newNodeGen()

def newNode():
    return next(nodeGen)
        
def used(expr):
    if expr.data == "expr":
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
    else:
        assert False,"Unexpected item in expression!"    

def buildCFG(parsed, cfg, parent):
    if parsed.data == "program":
        (exit, cfg) = buildCFG(parsed.children[0], cfg, parent)
        cfg["<exit>"] = ("<exit>",None,[])
        (_,_,esuccs) = cfg[exit]
        esuccs.append("<exit>")
        return ("<exit>",cfg)
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
            cfg[name] = ("assign",{"def":[v],"use":eused},[])
            return (name, cfg)
        elif stype == "cond":
            e = s.children[0]
            b1 = s.children[1]
            b2 = s.children[2]
            eused = used(e)
            cfg[name] = ("cond",{"use":eused},[])            
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
            cfg[name] = ("loop",{"use":eused},[])            
            (exit, cfg) = buildCFG(b, cfg, name)
            (_, _, esucc) = cfg[exit]
            esucc.append(name)
            return (name, cfg)
        elif stype == "print":
            e = s.children[0]
            eused = used(e)
            cfg[name] = ("print",{"use":eused},[])
            return (name, cfg)            
