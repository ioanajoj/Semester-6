n1 = 4; n2 = 10; x = 0.5;
a = 0; b = x;
f = @(t) exp(-t.^2);
L1 = repeated_simpson(f,a,b,n1)
L2 = repeated_simpson(f,a,b,n2)
err_f1 = 2 / sqrt(pi) * L1
err_f2 = 2 / sqrt(pi) * L2
