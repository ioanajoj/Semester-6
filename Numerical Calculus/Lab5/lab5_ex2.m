function err = lab5_ex2
  nodes=[1 2];
  f=[0 0.6931];
  der_f=[1 0.5];
  f_val = log(1.5);
  [H,~]=Hermite_interp(nodes,f,der_f,[1.5]);
  err=abs(H-f_val);
endfunction