def runit(text):
    for i in range(0,len(text)):
        try:
            if text[i] == 'a':
                if text[i-1] == 'z':
                    if text[i-2] == 'z':
                        if text[i-3] == 'i':
                            if text[i-4] == 'p':                        
                                raise ValueError
        except IndexError:
            pass
    return 0
        
