x = [ 1 2 3 4 5];
y = [ 22 23 25 30 28];

points=linspace(1,5,100);
Lx = Newton_interpolation(x,y,points);
Lx_single=Newton_interpolation(x,y,2.5);
disp("2,5 pounds of fertilizer="),disp(Lx_single),disp("pounds of potatos");

clf;hold on;grid on;
plot(x,y,'b');
plot(points,Lx,'r');
plot(2.5,Lx_single,'o');
