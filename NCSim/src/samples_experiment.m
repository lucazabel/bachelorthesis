function [samples, npres, mres] = samples_experiment()
%
% Simulator for Decentralized Network Coordinate Algorithms (NCSim) 
%
% 
% Version 1.1.0
% Updated on Jan. 3, 2016
% 
% Copyright (C) <2011-2016> by Yang Chen, Fudan University (chenyang@fudan.edu.cn)
% 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
% THE SOFTWARE.
%

%%%%%%%%%%%%%%%%% Code %%%%%%%%%%%%%%%%% 


% raw distance matrix %
clear
compute_nc = 1;
%load('data_matrix.mat');
load('fit_energy_tp2_mW_including_receiver.mat');

% PL: 169 * 169 PlanetLa data set
% Toread: 355 * 355 PlanetLab data set (collected in Mar.-Apr. 2010, 
%   used in our ACM ReArch'10 paper 'Taming the Triangle Inequality Violations with Network Coordinate System on Real Internet',
%   http://code.google.com/p/toread/) 
% kingmatrix: 1740 * 1740 King data set (http://pdos.csail.mit.edu/p2psim/kingdata/)
%   used in many Network Coordinate papers

% DATA = PL; % PlanetLab data set (small)
% DATA = Toread; % PlanetLab data set (big)
% DATA = king_matrix; % King data set
DATA = fit_energy_tp2_mW; % energy consumption data set
%DATA = FITc; % latency data set

% parameters of NCSim
default_dimension = 2; % config your NC dimension here
max_round = 3; % config your round(s) of simulation here
re_cdf_on = 1; % display the CDF of Relative Error (RE)
vivaldi_option = 1;
K_neigh = 20;
step_size = 1;
% selecting Vivaldi branch, 
%   0 - Vivaldi (basic), original Vivaldi
%   1 - Vivaldi (height),  original Vivaldi
%   2 - Vivaldi (TIV aware), used in "Towards Network Triangle Inequality
%   Violation Aware Distributed Systems" 
%   (Proc. of ACM IMC, 2007).
ides_option = 0;
% selecting IDES branch:
%   0 - IDES (nonnegative), ensuring all predicted distances to be nonnegative, 
%   used in "Phoenix: A Weight-based Network Coordinate System Using Matrix Factorization" 
%   (IEEE Transactions on Network and Service Management, 2011, Vol. 8, Issue 4)
%   1 - IDES (SVD)
%   2 - IDES(NMF)

fprintf('\nNCSim (%d Nodes, %d Neighbors)\n', length(DATA), K_neigh);
samples = 1:step_size:K_neigh;
npres = zeros(length(samples), 1);
mres = zeros(length(samples), 1);
i = 1;
N = length(DATA);
counter = 1;
if compute_nc == 1
    for sample = samples
        % NC: Vivaldi
        % 0- basic Vivaldi, 1- Vivaldi (height), 2-Vivaldi TIV aware
        predicted_matrix = NCS_vivaldi_all(DATA, default_dimension, length(DATA), sample, vivaldi_option); 
        rerr = relative_error(predicted_matrix, DATA);        
        %npre = NPRE(rerr);
        % IDES
        %tmp = randperm(N);         
        %landmarks = tmp(1:32); % choose random L nodes as landmarks
        %hosts = tmp(32+1:N);  % the rest of them are orinary hosts
        %D_landmark = DATA(landmarks, landmarks);
        %D_host2landmark = DATA(hosts, landmarks);
        
        %[out_l, in_l, out_h, in_h] = NCS_IDES_all(D_landmark, D_host2landmark, default_dimension, ides_option);
        %predicted_matrix = out_h*in_h;
        %real_matrix = DATA(hosts, hosts);
        %rerr=relative_error(predicted_matrix, real_matrix);        
        npre = NPRE(rerr);
        mre = median(rerr);
        fprintf('Vivaldi: NPRE:%.2f, MRE:%.2f\n', npre, mre);  
        npres(i, 1) = npre;
        mres(i, 1) = mre;
        i = i+1;
        counter = counter + 1;
    end
end

figure;
lw = 2;
% Create the first line plot
plot(samples, npres, '--', 'LineWidth',lw); hold on
plot(samples, mres, '-.', 'LineWidth', lw); hold on

% Add the legend
h5 = legend('NPRE', 'MRE');
set(h5, 'FontSize', 16);

% Add the axis labels and title
xlabel('Number of Neighbors (N=84)', 'FontSize', 16);
ylabel('Error Value (mW)', 'FontSize', 16);

% Save the plot as an SVG file
% saveas(gcf, 'plots/svg/samples_exp_mW_gate_rec_height.svg', 'svg');

