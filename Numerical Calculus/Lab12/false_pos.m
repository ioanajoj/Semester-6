function [c,i]=false_pos(a,b,f,err)
  for i=1:100
    c = (a*f(b) - b*f(a))/(f(b)-f(a));
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