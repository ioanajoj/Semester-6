## A=diag(3*ones(10,1)) + diag(-ones(9,1),-1) + diag(-ones(9,1),1)
## b=[2,ones(1,8),2]'
## [x,iter] = gauss_seidel_2(A,b,1e-16)

function [x,iter]=gauss_seidel_2(A, b, err)
  M = tril(A);
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
