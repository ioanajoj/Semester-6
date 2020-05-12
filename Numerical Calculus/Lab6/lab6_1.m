clf;

nodes=[0 pi/2 pi 3*pi/2 2*pi];
values=sin(nodes);

disp("The value of sin(x) at x=pi/4 is:"), disp(sin(pi/4))

cubic_nat_spline=spline(nodes,values,pi/4);
disp("The value of the cubic natural spline at x=pi/4 is"), disp(cubic_nat_spline)

cubic_clamped_spline=spline(nodes,[0 values 0],pi/4);
disp("The value of the cubic clamped spline at x=pi/4 is"), disp(cubic_clamped_spline)

%sine function
f=@(x) sin(x);
fplot(f,[0 2*pi],'r')
hold on;

%nat spline
xx=linspace(0,2*pi,1000);
cubic_nat_spline=spline(nodes,values,xx);
plot(xx, cubic_nat_spline, 'b')

%clamped
xx=linspace(0,2*pi,1000);
cubic_nat_spline=spline(nodes,[0 values 0],xx);
plot(xx, cubic_nat_spline, 'g')

plot(nodes, values, 'o');
grid on;