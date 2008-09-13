###
#   Copied from the pygame wiki cookbook
#   http://www.pygame.org/wiki/TextWrapping?parent=CookBook
#
#   This snippet of code will convert a string of text into a list containing 
#the lines it would break down into, for a certain font and width.
#

def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
                a=a+1
                n=text.rsplit(None, a)[0]
                if stext == n:
                        cut += 1
                        stext= n[:-cut]
                else:
                        stext = n
                l=font.size(stext)[0]
                real=len(stext)               
                done=0                        
        return real, done, stext             
    
def wrapline(text, font, maxwidth): 
        done=0                      
        wrapped=[]                  
                               
        while not done:             
                nl, done, stext=truncline(text, font, maxwidth) 
                wrapped.append(stext.strip())                  
                text=text[nl:]                                 
        return wrapped
