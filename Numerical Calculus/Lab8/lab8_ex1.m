a=0;b=1;n=4;
f=@(x)2./(1+x.^2);
clf; hold on; grid on; 

area_trapezium = repeated_trapezium(f,a,b,n)
x = linspace(0, 1, 100);
plot(x,f(x),'b','LineWidth',3);ylim([0,4]);
fill([x b a],[f(x) 0 0],'b','FaceAlpha',0.25);

## Trapezium 
plot([a, b], [f(a) f(b)],'r','LineWidth',2);
fill([0 1 1 0], [f([0 1]) 0 0] , 'r', 'FaceAlpha', 0.25);

## Simpson
nodes=[a (a+b)/2 b];
x=linspace(a,b,1000);
simple_simpson=sum(LagrangeBary(nodes,f(nodes),x))/1000
area_simpson = repeated_simpson(f,a,b,n)
