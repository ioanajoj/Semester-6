function [c,i]=bisection(a,b,f,err)
  for i=1:100
    c = (a + b) / 2;
    if abs(f(c)) < err || abs(b-a) < err || abs(b-a) / abs(b) < err
      break
    endif
    if f(a) * f(c) < 0
      b = c;
    else
      a = c;
    endif
  endfor
endfunction
