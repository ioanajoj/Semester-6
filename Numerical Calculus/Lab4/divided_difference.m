function table=divided_difference(nodes, values)
% nodes: x1, ..., xn
% values: f(x1), ..., f(xn)
% table: divided differences
n = length(nodes);table=NaN(n);
table(:,1)=values';
for j=2:n
    for i=1:n-j+1
        table(i,j) = (table(i+1, j-1) - table(i, j-1))/(nodes(i+j-1)-nodes(i));
    endfor
endfor
endfunction
