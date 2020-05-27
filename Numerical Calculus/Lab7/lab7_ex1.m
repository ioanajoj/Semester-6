time=[1:7];
temperature=[13 15 20 14 15 13 10];

m=length(time)-1;
a=( (m+1) * sum(time.*temperature) - sum(time) * sum(temperature) ) /...
  ( (m+1) * sum(time.^2) - sum(time)^2 );
b=( sum(time.^2) * sum(temperature) - sum(time.*temperature) * sum(time) ) /...
  ( (m+1) * sum(time.^2) - sum(time)^2 );
f=@(x) a*x+b;
disp("Temperature in the room at 8:00:"), disp(f(8))
error=norm(temperature-f(time));
disp("Error:"), disp(error)

coefs_lsq=polyfit(time,temperature,1);
disp("Coeffs:"), disp(coefs_lsq);
poly_lsq=@(x) polyval(coefs_lsq,x);

% predict temperature at 8 o'clock
disp("Temperature in the room at 8:00:"), disp(poly_lsq(8))

% find the minimum value E(a,b)
error=norm(temperature-poly_lsq(time));
disp("Error:"), disp(error)

% plot points
clf;
plot(time, temperature,'o')
hold on;
fplot(poly_lsq,[0,10],'-b');
fplot(f,[0,10],'-r');