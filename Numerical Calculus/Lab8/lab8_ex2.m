## Example:
a = 1.4; b = 2; c = 1; d = 1.5;
f = @(x,y) log(x + 2 * y);
L = trapezium_for_double_integral(f,a,b,c,d)