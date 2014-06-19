from numpy import loadtxt, where
from pylab import scatter, show, legend, xlabel, ylabel
 
#load the dataset
data = [1,2,3,2,3,12,45,23,24,4,2,34,2,34,23,3,42]
 
X = data[:, 0:2]
y = data[:, 2]
 
pos = where(y == 1)
neg = where(y == 0)
scatter(X[pos, 0], X[pos, 1], marker='o', c='b')
scatter(X[neg, 0], X[neg, 1], marker='x', c='r')
xlabel('Exam 1 score')
ylabel('Exam 2 score')
legend(['Not Admitted', 'Admitted'])
show()