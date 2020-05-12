
%nodes=[0 3 5 8 13];
%values=[0 225 383 623 993];
%der_values=[75 77 80 74 72];

%H is the Hermite polynomial
%x=points where we compute H
%Pn=(x-z1)...(x-zn), D[Pn]=der of Pn, P0=1,D[p0]=0
%Pn+1=Pn(x-zn+1),D[Pn+1]=D[Pn(x-zn+1)]=D[Pn](x-zn+1)+Pn
%degree(H) <= #double_nodes-1

function [Hx,der_Hx]=Hermite_interp(nodes,values,der_values,x)
  table=div_diff_double(nodes,values,der_values);
  coefs=table(1,:); %only take first line
  double_nodes=repelem(nodes, 2);
  Hx=x; der_Hx=x; %for same dimension
  for i=1:length(x)
    Hx(i)=coefs(1);
    P=1;
    der_Hx(i)=0;
    der_P=0;
    for k=2:length(coefs)
      der_P=der_P*(x(i)-double_nodes(k-1))+P;
      P=P*(x(i)-double_nodes(k-1));
      Hx(i)=Hx(i)+coefs(k)*P;
      der_Hx(i)=der_Hx(i)+coefs(k)*der_P;
    endfor
  endfor
endfunction
