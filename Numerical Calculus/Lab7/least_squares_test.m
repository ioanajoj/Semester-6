function error=least_squares_test
  k=2;
  clf;axis equal;axis([0 5 0 3]);
  xticks(0:1:5);yticks(0:1:3);
  grid on;hold on;
  set(gca,"fontsize",15)
  [x,y]=ginput(1);
  nodes=x;values=y;
  while ~isempty([x,y])
    plot(x,y,'*k','MarkerSize',10);
    [x,y]=ginput(1);
    nodes=[nodes,x];values=[values,y];
  endwhile
  coefs_lsq=polyfit(nodes,values,k);
  poly_lsq=@(x) polyval(coefs_lsq,x);
  fplot(poly_lsq,[0,5],"LineWidth",3);
  legend("off");
  disp(values)
  disp(poly_lsq(nodes))
  error=norm(values-poly_lsq(nodes));
endfunction
