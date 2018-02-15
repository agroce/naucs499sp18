from lark import Lark

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

    stmt: decl ";"
          | assign ";"
          | cond ";"
          | loop ";"
          | print ";"

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
            
