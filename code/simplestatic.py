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

parsed = parser.parse("{int x; x := 4*(3+4);}")
print parsed
print parsed.data
for s in parsed.children:
    print s.data

