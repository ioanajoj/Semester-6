## A=diag(3*ones(10,1)) + diag(-ones(9,1),-1) + diag(-ones(9,1),1)
## b=[2,ones(1,8),2]'
## sor(A,b,10,1.13)

function x=sor(A, b, it, omega)
  n = length(b);
  x_old=zeros(n,1);
  x = x_old;
  for k=1:it
    for i=1:n
      x(i) = (b(i) - A(i,1:i-1)*x(1:i-1) - A(i,i+1:n)*x_old(i+1:n)) / A(i,i);
    endfor
    x = (1-omega)*x_old + omega*x;
    x_old = x;    
  endfor
endfunction