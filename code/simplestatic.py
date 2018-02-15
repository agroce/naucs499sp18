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
    while (x > 1) {
       print x;
       x := x - 1;
    };
   }
""")

ll.run(P,{})


