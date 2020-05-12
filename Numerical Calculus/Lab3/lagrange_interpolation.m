function lmf = lagrange_interpolation(X)
    %x = [1930,1940,1950,1960,1970,1980];
    %f = [123203,131669,150697,179323,203212,226505];
    x = [100, 121, 144];
    f = [10, 11, 12];
    a = lab3_ai(x);
    lmf = [];
    for val=1:length(X)
        upper = 0;
        lower = 0;
        for i=1:length(x)
            upper = upper + a(i) * f(i) / (X(val) - x(i));
            lower = lower + a(i) / (X(val) - x(i));
        endfor
        lmf = [lmf, upper / lower];
    endfor
endfunction
    