from numpy import *
import pylab as p
#import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3
u=r_[0:2*pi:100j]
v=r_[0:pi:100j]
x=10*outer(cos(u),sin(v))
y=10*outer(sin(u),sin(v))

x=u
y=v
z=sin(u)+cos(v)

print "X","-----------------"
print len(x)
print x[0]
print x

print "Y","-----------------"
print len(y)
print y[0]
print y

print "Z","-----------------"
print len(z)
print z[0]
print z

fig=p.figure()
ax = p3.Axes3D(fig)
ax.plot_wireframe(x,y,z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
p.show()
