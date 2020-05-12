nodes=[0 3 5 8 13];
values=[0 225 383 623 993];
der_values=[75 77 80 74 72];
clf;
t=linspace(0,13,1000);
[distance,speed]=Hermite_interp(nodes,values,der_values,t);
plot(distance,speed)
xlabel("distance");ylabel("speed")
xticks(0:100:1000);yticks(40:10:120);
grid on;