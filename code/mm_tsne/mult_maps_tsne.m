function [Y, importance] = mult_maps_tsne(P, no_maps, no_dims, max_iter)
%MULT_MAPS_TSNE Runs multiple maps t-SNE to construct multiple embeddings
%
%   [Y, importance] = mult_maps_tsne(P, no_maps, no_dims, max_iter)
%
% Uses multiple maps t-Stochastic Neighborhood Embedding (t-SNE) on the 
% similarity matrix P to construct no_maps complementary data representations 
% of dimensionality no_dims. The matrix P should be a symmetric, non-negative,
% zero-diagonal matrix that sums up to one. Ideally, the matrix P should
% contain intransitive similarities (otherwise, regular t-SNE can be used
% without problems). Note that if no_maps is set to 1, this function
% reduces to normal t-SNE.
%
% The function returns the low-dimensional maps in the matrix Y, and the 
% corresponding importance weights in importance.
%
%
% (C) Laurens van der Maaten
% Delft University of Technology, 2011


    if ~exist('no_maps', 'var') || isempty(no_maps)
        no_maps = 5;
    end    
    if ~exist('no_dims', 'var') || isempty(no_dims)
        no_dims = 2;
    end
    if ~exist('max_iter', 'var') || isempty(max_iter)
        max_iter = 1000;
    end
    
    % Check inputs
    eps = 1e-7;
    assert(no_maps == round(no_maps), 'Number of maps should be integer.');
    assert(no_maps >= 1, 'Number of maps should be positive.');
    assert(no_dims == round(no_dims), 'Number of dimensions should be integer.');
    assert(no_dims >= 1, 'Number of dimensions should be positive.');
    if no_maps == 1, warning('Note that when using a single map, multiple maps t-SNE reduces to standard t-SNE.'); end
    assert(all(P(:) >= 0), 'Similarity matrix P should be non-negative.');
    assert(abs(sum(P(:)) - 1) < eps, 'Similarity matrix P should sum up to one.');
    assert(sum(sum(abs(P - P'))) < eps, 'Similarity matrix P should be symmetric.');
    
    % Initialize some variables
    n = size(P, 1);                                     % number of instances and dimensionality
    momentum = 0.5;                                     % initial momentum
    final_momentum = 0.8;                               % value to which momentum is changed
    mom_switch_iter = 250;                              % iteration at which momentum is change
    epsilonY = 250;                                     % learning rate for changes in Y
    epsilonW = 100;                                     % learning rate for changes in W
    
    % Lie about the P-values
    P = P .* 4;
    
    % Initialize a random solution
    if numel(no_maps) == 1
        Y = randn(n, no_dims, no_maps) * 0.001;
    else
        Y = no_maps;
        [n, no_dims, no_maps] = size(Y);
    end
    y_incs = zeros(n, no_dims, no_maps);
    weights = repmat(1 / no_maps, [n no_maps]);
    
     % Pre-allocate some memory
    num = zeros(n, n, no_maps);
    QQ  = zeros(n, n, no_maps);
    dCdP = zeros(n, no_maps);
    dCdD = zeros(n, n, no_maps);
    dCdY = zeros(n, no_dims, no_maps);
    
    % Run the iterations
    for iter=1:max_iter
        
        % Compute the mixture proportions from the mixture weights
        proportions = exp(-weights);
        proportions = bsxfun(@rdivide, proportions, sum(proportions, 2));

        % Compute pairwise affinities per map
        for m=1:no_maps
            sum_Y = sum(Y(:,:,m) .^ 2, 2);
            tmp = 1 ./ (1 + bsxfun(@plus, sum_Y, bsxfun(@plus, sum_Y', -2 * Y(:,:,m) * Y(:,:,m)')));
            tmp(1:n+1:end) = 0;
            num(:,:,m) = tmp;
        end

        % Compute pairwise affinities under the mixture model
        QZ = repmat(eps, [n n]);
        for m=1:no_maps
            QQ(:,:,m) = (proportions(:,m) * proportions(:,m)') .* num(:,:,m);
            QZ = QZ + QQ(:,:,m);
        end
        Z = sum(QZ(:));        
        Q = QZ ./ Z;
        
        % Compute derivative of cost function w.r.t. mixture proportions
        PQ = Q - P;
        tmp = (1 ./ QZ) .* PQ;
        for m=1:no_maps
            dCdP(:,m) = sum(bsxfun(@times, proportions(:,m), num(:,:,m) .* tmp), 1)';
        end
        dCdP = 2 * dCdP;

        % Compute derivative of cost function w.r.t. mixture weights
        dCdW = proportions .* bsxfun(@minus, sum(dCdP .* proportions, 2), dCdP);

        % Compute derivative of cost function w.r.t. pairwise distances
        for m=1:no_maps
            dCdD(:,:,m) = (QQ(:,:,m) ./ QZ) .* -PQ .* num(:,:,m);
        end

        % Compute derivative of cost function w.r.t. the maps
        for m=1:no_maps
            for i=1:n
                dCdY(i,:,m) = sum(bsxfun(@times, dCdD(i,:,m)' + dCdD(:,i,m), bsxfun(@minus, Y(i,:,m), Y(:,:,m))), 1);
            end
        end
        
        % Update the solution
        y_incs = momentum * y_incs - epsilonY * dCdY;
        Y = Y + y_incs;
        Y = bsxfun(@minus, Y, mean(Y, 1));
        weights = weights - epsilonW * dCdW;
        
        % Update the momentum if necessary
        if iter == mom_switch_iter
            momentum = final_momentum;
        end
        if iter == 50
            P = P ./ 4;
        end
        
        % Compute the value of the cost function
        if ~rem(iter, 25)            
            C = sum(P(:) .* log(max(P(:), realmin) ./ max(Q(:), realmin)));
            disp(['Iteration ' num2str(iter) ': error is ' num2str(C)]);
        end
    end
    importance = proportions;
    
    