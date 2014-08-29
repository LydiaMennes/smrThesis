
    % Load and pre-process the word association data
    load 'association1000.mat'                   % experiment on small word association data set
%     load 'association5000.mat'                  % experiment on large word association data set
    if size(P, 1) == 5000
        warning('Running on the full word association data set requires a lot of RAM!');
    else
        disp('Please note that 5,000 words were used for the experiments in the paper!');
    end
    P = bsxfun(@rdivide, P, sum(P, 2));
    P = P + P';
    P = max(P ./ sum(P(:)), eps);
    n = size(P, 1);
    
    % Run the leave-out multiple-maps t-SNE model
    no_dims = 2;
    if size(P, 1) == 1000
        no_maps = 8;
    else
        no_maps = 25;
    end
    max_iter = 500;
    disp(['Running multiple maps t-SNE to construct ' num2str(no_maps) ' maps of ' num2str(size(P, 1)) ' words...']);
    if size(P, 1) == 5000
        disp('This may take up to 24 hours to compute!');
    else
        disp('This may take up to 15 minutes to compute!');
    end
    [maps, weights] = mult_maps_tsne(P, no_maps, no_dims, max_iter);
    
    % Shows the maps
    if size(P, 1) == 5000
        disp(['Drawing maps after ' num2str(max_iter) ' iterations... please note that 2,000 iterations were used to produce the results in the paper!']);
    end
    for m=1:size(maps, 3)
        
        % Remove points with small importance weight
        figure(m);
        if size(maps, 3) > 1
            ii = find(weights(:,m) > .05);
        else
            ii = 1:size(maps, 1);
        end
        
        % Make scatterplot
        scatter(maps(ii, 1, m), maps(ii, 2, m), weights(ii, m) * 40); axis off
        XLim = get(gca, 'XLim');
        width = XLim(2) - XLim(1);
            
        % Place the text labels
        for i=1:length(ii)			
			xc = maps(ii(i), 1, m) + 0.006 * width;
			yc = maps(ii(i), 2, m);
			if ischar(xc) || ischar(yc)
				disp('problem')
				disp(xc)
				disp(yc)
			end
			if isnan(xc) || isnan(yc)
				disp('nan found')
			end
			if ~isa(xc, 'double') || ~isa(yc, 'double')
				disp('definitely problem input')
			end
            text(xc, yc, words{ii(i)});
        end
        axis off
        set(gcf, 'Position', [1 + 3 * m -150 + 3 * m 1280 705]);
        drawnow
    end       