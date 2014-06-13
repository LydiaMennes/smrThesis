function [U,S,V] = fsvd(A, k, i, usePowerMethod)
% FSVD Fast Singular Value Decomposition 
% 
%   [U,S,V] = FSVD(A,k,i,usePowerMethod) computes the truncated singular
%   value decomposition of the input matrix A upto rank k using i levels of
%   Krylov method as given in [1], p. 3.
% 
%   If usePowerMethod is given as true, then only exponent i is used (i.e.
%   as power method). See [2] p.9, Randomized PCA algorithm for details.
% 
%   [1] Halko, N., Martinsson, P. G., Shkolnisky, Y., & Tygert, M. (2010).
%   An algorithm for the principal component analysis of large data sets.
%   Arxiv preprint arXiv:1007.5510, 0526. Retrieved April 1, 2011, from
%   http://arxiv.org/abs/1007.5510. 
%   
%   [2] Halko, N., Martinsson, P. G., & Tropp, J. A. (2009). Finding
%   structure with randomness: Probabilistic algorithms for constructing
%   approximate matrix decompositions. Arxiv preprint arXiv:0909.4061.
%   Retrieved April 1, 2011, from http://arxiv.org/abs/0909.4061.
% 
%   See also SVD.
% 
%   Copyright 2011 Ismail Ari, http://ismailari.com.

    if nargin < 3
        i = 1;
    end

    % Take (conjugate) transpose if necessary. It makes H smaller thus
    % leading the computations to be faster
%    if size(A,1) < size(A,2)
%        A = A';
%        isTransposed = true;
%    else
%        isTransposed = false;
%    end
    isTransposed = false;

    n = size(A,2);
    l = k + 2;

    % Form a real n×l matrix G whose entries are iid Gaussian r.v.s of zero
    % mean and unit variance
%    G = randn(n,l);
    G = [-0.44, 1.67, -1.26, -2.43;0.56, 0.63,1.16,0.68;0.69,0.09,0.45,0.65;-0.14,-1.51,0.81,1.81;-0.47,0.19,-0.51,-0.84]


    if nargin >= 4 && usePowerMethod
        % Use only the given exponent
        H = A*G;
        for j = 2:i+1
            H = A * (A'*H);
        end
    else
        % Compute the m×l matrices H^{(0)}, ..., H^{(i)}
        % Note that this is done implicitly in each iteration below.
        H = cell(1,i+1);
        H{1} = A*G;
        for j = 2:i+1
            H{j} = A * (A'*H{j-1});
        end

        % Form the m×((i+1)l) matrix H
        H = cell2mat(H)
    end

    % Using the pivoted QR-decomposiion, form a real m×((i+1)l) matrix Q
    % whose columns are orthonormal, s.t. there exists a real
    % ((i+1)l)×((i+1)l) matrix R for which H = QR.  
    % XXX: Buradaki column pivoting ile yapilmayan hali.
    [Q,~] = qr(H,0);
    disp('q, n, d')
    (i+1)*l
    size(A,1)
    size(A,2)
    disp('size Q')
    size(Q)

    % Compute the n×((i+1)l) product matrix T = A^T Q
    T = A'*Q;
    disp("size T")
    size(T)

    % Form an SVD of T
    [Vt, St, W] = svd(T,'econ');

    % Compute the m×((i+1)l) product matrix
    Ut = Q*W;

    % Retrieve the leftmost m×k block U of Ut, the leftmost n×k block V of
    % Vt, and the leftmost uppermost k×k block S of St. The product U S V^T
    % then approxiamtes A. 

    if isTransposed
        V = Ut(:,1:k);
        U = Vt(:,1:k);     
    else
        U = Ut(:,1:k);
        V = Vt(:,1:k);
    end
    S = St(1:k,1:k);
end