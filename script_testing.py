from plxscripting.easy import *
s_i, g_i = new_server('localhost', 10000, password='%#U%LyiaH^@i23Mv')

s_i.new()
g_i.gotostructures()

# Alternative 1
# Adds a line section with a length of 1 to a polycurve
polycurve_g = g_i.polycurve(4, 5)

segment_g = polycurve_g.add() 
print(segment_g)