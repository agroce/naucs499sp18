import littlelanguage as ll

P = ll.parse(
"""
   {
    int x;
    x := 4*(3+4);
    print x;
    if (x > 20) {
       print x;
    } else {
       print 2;
    };
    while (x > 1) {
       print x;
       x := x - 1;
    };
   }
""")

ll.run(P,{})


