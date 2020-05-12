## find omega:
## TJ=diag(diag(A))\(diag(diag(A))-A); 
## rho=max(abs(eig(TJ))); 
## omega=2/(1+sqrt(1-rho^2))
##
## A=diag(3*ones(10,1)) + diag(-ones(9,1),-1) + diag(-ones(9,1),1)
## b=[2,ones(1,8),2]'
## [x,iter] = sor_2(A,b,1e-16, omega)

function [x,iter]=sor_2(A, b, err, omega)
  M = (diag(diag(A)) + tril(A,-1))/omega;
  N = M - A;
  c = M\b;
  T = M\N;
  x_old = zeros(size(b));
  iter = 1;
  while true
    x = c + T*x_old;
    if norm(x-x_old,inf)*norm(T,inf)/(1-norm(T,inf))<=err
      return;
    endif
    x_old = x;
    iter = iter + 1;
  endwhile
endfunction