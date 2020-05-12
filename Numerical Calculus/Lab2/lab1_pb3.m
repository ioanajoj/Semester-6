function lab1_pb3(n)
    clf; axis square; hold on;
    expo = @(x) exp(x);
    fplot(expo, [-1,3], 'k');
    Tn = @(x) ones(1, length(x));
    for k = 1:n
        Tn = @(x) Tn(x)+1/factorial(k)*x.^k;
        fplot(Tn, [-1, 3]); 
    end
    legend()
end