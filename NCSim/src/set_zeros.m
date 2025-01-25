function m2 = setZeros(m1, m2)
% This function sets the values in m2 to 0 if the corresponding
% cell in m1 is 0.
%
% Inputs:
%   m1: a matrix of any size
%   m2: a matrix of the same size as m1
%
% Output:
%   m2: the updated matrix with 0s in the same positions as m1

% Get the size of the matrix
[m, n] = size(m1);

% Loop through each cell in the matrix
for i = 1:m
    for j = 1:n
        % Check if the current cell in m1 is 0
        if m1(i,j) == 0
            % If it is, set the corresponding cell in m2 to 0 as well
            m2(i,j) = 0;
        end
    end
end
end
