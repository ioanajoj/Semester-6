temperature=[0 10 20 30 40 60 80 100];
pressure=[0.0061 0.0123 0.0234 0.0424 0.0738 0.1992 0.4736 1.0133];
T=45;

degree_1=1;
coefs_lsq_1=polyfit(temperature,pressure,degree_1);
poly_lsq_1=@(x) polyval(coefs_lsq_1,x);
value_1=polyval(coefs_lsq_1,T);
error_1=norm(poly_lsq_1(pressure) - temperature);
disp("Value for T=45 for polynomial of degree"), disp(degree_1), 
  disp(value_1), disp(error_1);

degree_2=3;
coefs_lsq_2=polyfit(temperature,pressure,degree_2);
poly_lsq_2=@(x) polyval(coefs_lsq_2,x);
value_2=polyval(coefs_lsq_2,T);
error_2=norm(poly_lsq_2(pressure) - temperature);
disp("Value for T=45 for polynomial of degree"), disp(degree_2), 
  disp(value_2), disp(error_2);

clf;hold on;axis([-5 105 -0.5 2]);grid on;
plot(temperature,pressure,'o');
plot(T,value_1,'-*','MarkerSize',10,'MarkerEdgeColor','blue');
plot(T,value_2,'-*','MarkerSize',10,'MarkerEdgeColor','red');
fplot(poly_lsq_1,[0,100],'-b');
fplot(poly_lsq_2,[0,100],'-r');
xlabel("temperature");
ylabel("pressure");
