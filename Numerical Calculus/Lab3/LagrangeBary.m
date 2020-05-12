% nodes = [1930 1940 1950 1960 1970 1980];
% values = [123203 131669 150697 179323 203212 226505];
% interpolation = 1955
% extrapolation = 1995

function Lx = LagrangeBary(nodes, values, x)
    % nodes: x1 ... xn
    % values: f(x1) ... f(x2)
    A = CoeffBary(nodes);
    Lx = sum(A.*values./(x-nodes)) / sum(A./(x-nodes)) * 1000;
endfunction

function A = CoeffBary(nodes)
    A = zeros(size(nodes));
    for i = 1:length(nodes)
        A(i) = 1 / prod(nodes(i)-nodes(nodes!=nodes(i)));
    endfor
endfunction
