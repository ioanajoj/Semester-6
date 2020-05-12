a = 0; b = pi; n1 = 10; n2 = 30;
f = @(x) 1 ./ (4 + sin(20 .* x));
L1 = repeated_simpson(f, a, b, n1)
L2 = repeated_simpson(f, a, b, n2)
