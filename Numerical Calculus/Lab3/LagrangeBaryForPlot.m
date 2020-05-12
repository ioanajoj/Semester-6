% nodes = [1930 1940 1950 1960 1970 1980];
% values = [123203 131669 150697 179323 203212 226505];
% interpolation = 1955
% extrapolation = 1995

function Lx = LagrangeBaryForPlot(nodes, values, x)
    % nodes: x1 ... xn
    % values: f(x1) ... f(x2)
    A = CoeffBary(nodes);
    Lx = x;
    for j = 1:length(x)
        x_pos_node = find(nodes==x(j));
        if x_pos_node
            Lx(j) = values(x_pos_node);
        else
            Lx(j) = sum(A.*values./(x(j)-nodes)) / sum(A./(x(j)-nodes)) * 1000;
        endif
    endfor
endfunction

function A = CoeffBary(nodes)
    A = zeros(size(nodes));
    for i = 1:length(nodes)
        A(i) = 1 / prod(nodes(i)-nodes(nodes!=nodes(i)));
    endfor
endfunction