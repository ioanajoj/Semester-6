##x = [81 100 121 144];
##y = sqrt(x);
y = [9 10 11 12]
f = [y'];

X = 115;
m = length(x);
result = -1;
for i=1:m
  for j=1:i-1
    deter = det([f(j,j) x(j)-X; f(i,j) x(i)-X]);
    f(i,j+1) = deter / (x(i)-x(j));
  endfor;
  if i>1 && abs(f(i,i) - f(i-1,i-1)) < 10e-3
    result = f(i,i);
    break;
  endif
endfor;

disp(result);