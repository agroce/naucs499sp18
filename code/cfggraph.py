from graphviz import Digraph

def makeGraph(cfg,file):
    dot = Digraph()
    for s in cfg:
        info = ""
        if cfg[s][1] != None:
            info = ":" + s + ":"+repr(cfg[s][1])
        else:
            info = ":" + s + ":{}"
        dot.node(s,cfg[s][0] + info,shape='box')
    for s in cfg:
        for s2 in cfg[s][2]:
            dot.edge(s,s2)
    dot.render(file,view=True)
