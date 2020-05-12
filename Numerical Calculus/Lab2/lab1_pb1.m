function lab1_pb1
    clf; axis square;
    l1 = @(x) x;
    subplot(2,2,1), fplot(l1, [0, 1]); title('Legendre poly l1');
    l2 = @(x) 3/2*x^2 - 1/2;
    subplot(2,2,2), fplot(l2, [0, 1]); title('Legendre poly l2');
    l3 = @(x) 5/2*x^3 - 3/2*x;
    subplot(2,2,3), fplot(l3, [0, 1]); title('Legendre poly l3');
    l4 = @(x) 35/8*x^4 - 15/4*x^2 + 3/8; 
    subplot(2,2,4), fplot(l4, [0, 1]); title('Legendre poly l4');
end