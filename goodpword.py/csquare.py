import sys 
import stdio 
import stddraw
from color import Color 

def main():
    r1 = int(sys.argv[1])
    g1 = int(sys.argv[2])
    b1 = int(sys.argv[3])
    c1 = Color(r1,g1,b1)
    
    r2 = int(sys.argv[4])
    g2 = int(sys.argv[5])
    b2 = int(sys.argv[6])
    c2 = Color(r1,g1,b1) 
    
    stddraw.setCanvasSize(512,256)
    stddraw.setYscale(0.25,0.75) 
    
    stddraw.setPenColor(c1)
    stddraw.filledSquare(.25,.5,.2)
    stddraw.setPenColor(c2)
    stddraw.filledSquare(.25,.5,.1) 
    
    stddraw.setPenColor(c2)
    stddraw.filledSquare(.75,.5,.2)
    stddraw.setPenColor(c1)
    stddraw.filledSquare(.75,.5,.1) 
    
    stddraw.show()
    
    if __name__ == '__main__': main()