nodes = linspace(0, 6, 13);
f=@(x) exp(sin(x));
values=f(nodes);

X = linspace(0, 6, 100);
Y = Newton_interpolation(nodes, values, X);
clf;hold on;grid on;

fplot(f,[0,6],'r');
plot(nodes,values,'o');
plot(X,Y,'b');
