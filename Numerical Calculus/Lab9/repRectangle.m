function area = repRectangle(f,a,b,n)
    h = (b-a)/n;
    x = a+h/2:h:b-h/2;
    area = h*sum(f(x));
end