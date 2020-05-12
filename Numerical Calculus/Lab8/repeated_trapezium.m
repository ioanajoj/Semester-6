function area=repeated_trapezium(f,a,b,n)
  h=(b-a)/n; x=a+h:h:b-h;
  area=h/2*(f(a)+2*sum(f(x))+f(b));
endfunction