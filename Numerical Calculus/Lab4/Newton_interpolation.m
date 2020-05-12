function Lx=Newton_interpolation(nodes, values, x)
  % x the point(s) where we compute L
  % L  is the Lagrange polynomial
  table=divided_difference(nodes, values); 
  Lx=x;
  for i=1:length(x)
    prods=[1 cumprod(x(i)-nodes(1:end-1))];
    Lx(i)=table(1,:)*prods';
  endfor
endfunction
