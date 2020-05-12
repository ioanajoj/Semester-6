function lab1_pb2_a(n)
    clf; axis square; hold on;
    tn = @(n) @(t) cos(n .* acos(t));
    for i = 1:n
        fplot(tn(i), [-1, 1]);
    end
end