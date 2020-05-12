function lab1_pb2_b_2(n)
    clf; axis square; hold on;
    t0 = @(x) ones(1, length(x)); fplot(t0, [-1, 1]);
    t1 = @(x) x; fplot(t1, [-1, 1]);
    tnrec = @(t0, t1) @(x) 2*x.*t1(x)-t0(x);
    for i = 2:n
        fplot(tnrec(t0, t1), [-1, 1]);
        t0 = t1;
        t1 = tnrec;
    end
end