import sys 
import stdio 
from charge import Charge 

x = float(sys.argv[1])
y = float(sys.argv[2])
c1 = Charge(0.16,0.54,23.67)
c2 = Charge(0.34,0.73,45.38) 

v1= c1.potentialAt(x,y)
v2 = c2.potentialAt(x,y) 
stdio.writef('potential at (%.2f,%.2f) due to\n',x,y) 
stdio.writeln(' ' + str(c1)+'and')
stdio.writeln(' '+str(c2))
stdio.writef('is %.2e\n',v1+v2)