% nodes = [1930 1940 1950 1960 1970 1980];
% values = [123203 131669 150697 179323 203212 226505];
% interpolation = 1955
% extrapolation = 1995

function L = LagrangeBary(nodes, values, X)
    % nodes: x1 ... xn
    % values: f(x1) ... f(x2)
    w=CoeffBary(nodes);
    L=X;
    for j=1:length(X)
      x_pos_node=find(nodes==X(j));
      if x_pos_node
        L(j)=values(x_pos_node);
      else
        L(j)=sum(w.*values./(X(j)-nodes))/...
              sum(w./(X(j)-nodes));
      endif
    endfor
endfunction

function A = CoeffBary(nodes)
    A = zeros(size(nodes));
    for i = 1:length(nodes)
        A(i) = 1 / prod(nodes(i)-nodes(nodes!=nodes(i)));
    endfor
endfunction
