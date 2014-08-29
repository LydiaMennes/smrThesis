%NIPS_DEMO Demonstration of multiple maps t-SNE on NIPS vol. 1-20 data
%
%   nips_demo
%
% Demonstrated the use of multiple maps t-SNE on the NIPS vol. 1-20 data.
%
%
% (C) Laurens van der Maaten
% Delft University of Technology, 2011


    clear all
    close all

    % Load data
    disp('Loading and pre-processing data...');
    load 'nips_1-22.mat'

    % Prepare co-authorship matrix
    no_authors = length(authors);
    P = zeros(no_authors, no_authors);
    for i=1:size(documents, 1)
        doc_authors = find(documents(i,:));
        if ~isempty(doc_authors)
            ind = combn(doc_authors, 2);
            P(sub2ind(size(P), ind(:,1), ind(:,2))) = P(sub2ind(size(P), ind(:,1), ind(:,2))) + 1;
        end
    end
    
    % Remove authors with only one paper
    no_papers = full(sum(documents, 1));
    rem_ind = find(no_papers < 2);
    P(rem_ind,:) = [];
    P(:,rem_ind) = [];
    no_papers(rem_ind) = [];
    authors(rem_ind) = [];
    
    % Remove authors without cooperations
    authors_without_coop = find(sum((P ~= 0), 2) == 1);
    P(authors_without_coop,:) = [];
    P(:,authors_without_coop) = [];
    no_papers(authors_without_coop) = [];
    authors(authors_without_coop) = [];
    
    % Normalize P-matrix
    P(1:size(P, 1) + 1:end) = 0;
    unnorm_P = P;
    P = bsxfun(@rdivide, P, sum(P, 2));
    P = P + P';
    P = P ./ sum(P(:));    
    
    % Run multiple maps t-SNE
    no_maps = 5;
    no_dims = 2;
    max_iter = 500;
    disp(['Running multiple maps t-SNE to construct ' num2str(no_maps) ' maps of ' num2str(length(authors)) ' authors...']);
    disp('This may take up to 15 minutes to compute!');    
    [maps, weights] = mult_maps_tsne(P, no_maps, no_dims, max_iter);
    
    % Compute font sizes according to importance
    font_sizes = 6 + round(log10(no_papers) * 6);
    
    % Draw maps
    disp(['Drawing maps after ' num2str(max_iter) ' iterations... please note that 2,000 iterations were used to produce the results in the paper!']);
    for i=1:no_maps
        
        % Plot dots of authors with sufficient importance weight
        figure(i);
        ind = find(weights(:,i) > .05);
        width = max(maps(ind, 1, i)) - min(maps(ind, 1, i));
        scatter(maps(ind, 1, i), maps(ind, 2, i), 20 * weights(ind, i));
        axis off
        
        % Plot names of authors with sufficient importance weight
        cur_authors = authors(ind);
        for ii=1:length(cur_authors)
            author = cur_authors{ii}(1:find(cur_authors{ii} == '_', 1, 'first') - 1);
            h = text(maps(ind(ii), 1, i) + .004 * width, maps(ind(ii), 2, i), author);
            set(h, 'FontSize', font_sizes(ind(ii)));
        end
        drawnow
    end
    