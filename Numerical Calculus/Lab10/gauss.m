function x = gauss(A,b)
  A = [A, b];
  n = length(b);
  for k=1:n-1
    [max_val, max_pos] = max(abs(A(k:n,k)));
    max_pos = max_pos + k - 1;
    if max_val > 0 && max_pos > k
      A([k, max_pos], k:end) = A([max_pos, k], k:end);
    elseif max_val == 0
      disp('No unique solution');
    endif
    for i=k+1:n
      A(i,k:end) = A(i,k:end) - A(k,k:end)*(A(i,k)/A(k,k));
    endfor
  endfor
  x = backward_substitution(A(:,1:n), A(:,n+1));
endfunction