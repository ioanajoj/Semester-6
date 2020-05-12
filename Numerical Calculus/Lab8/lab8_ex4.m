a=1; 
b=2;
f=@(x) x.*log(x);

i = 1;
value = -1;
while value != 636
  L = repeated_trapezium(f,a,b,i);
  value = round(L*1e3);
##  disp(value);
  i = i+1;
end
disp(L);