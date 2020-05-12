function lab1_pb2_b(n)
    clf; axis square; hold on;
    t0 = @(x) ones(1, length(x)); fplot(t0, [-1, 1]);
    t1 = @(x) x; fplot(t1, [-1, 1]);
    for i = 2:n
        tnrec = @(x) 2*x.*t1(x)-t0(x);
        fplot(tnrec, [-1, 1]);
        t0 = t1;
        t1 = tnrec;
    end
end