% If the input vector is [4, 5, 1, 3, 2, 6], the sorted vectortemp would be [1, 2, 3, 4, 5, 6].
% The index of the 90th percentile value using the nearest rank method is calculated as ceil(length(temp)*0.9), 
% which is 6. Therefore, the output value of NPRE would be 6, which is the 90th percentile value of the input vector.

function NPRE_Value = NPRE(input_vector)
    temp = sort(input_vector);
%    length(temp)
    NPRE_Value = temp(ceil(length(temp)*0.9));