## Example
a = 0; b = 2 * pi; n1 = 3; n2 = 4; r = 110; p = 75;
f = @(x)[1 - (p/r).^2 .* sin(x)].^(1/2);
r = 110; p = 75;

L = repeated_trapezium(f, a, b, n2);
H = 60 * r / (r^2 - p^2) * L
L = repeated_trapezium(f, a, b, n1);
H = 60 * r / (r^2 - p^2) * L
