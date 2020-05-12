clf;hold on;
nodes=linspace(-5,5,15);

%function
f=@(x) sin(2.*x);
y=f(nodes);
fplot(f, [-5 5], 'r');

%Hermite
der_f=@(x) 2*cos(2.*x); %derivative of f
der_y=der_f(nodes); %derivative values
[H,~]=Hermite_interp(nodes,y,der_y,nodes)
plot(nodes,H, 'o');
xticks(nodes);

grid on;