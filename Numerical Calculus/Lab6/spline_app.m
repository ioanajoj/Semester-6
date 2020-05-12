clf;axis equal;axis([0 2 0 1]);
xticks(0:0.1:2);yticks(0:0.1:1);
grid on;hold on;
set(gca,"fontsize",15)
[x,y]=ginput(1);
X=x;Y=y;
i=1;
while ~isempty([x,y])
  plot(x,y,'*k','MarkerSize',10);
  text(x+0.01,y+0.01,num2str(i),"fontsize",15);
  [x,y]=ginput(1);
  i=i+1;
  X=[X,x];Y=[Y,y];
endwhile
nodes=linspace(0,1,length(X));
time=linspace(0,1,1000);
spline_x=spline(nodes,X,time);
spline_y=spline(nodes,Y,time);
plot(spline_x,spline_y,"LineWidth",3)
