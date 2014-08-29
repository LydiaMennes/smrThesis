

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
            text(maps(ii(i), 1, m) + 0.006 * width, maps(ii(i), 2, m), words{ii(i)});
        end
        axis off
        set(gcf, 'Position', [1 + 3 * m -150 + 3 * m 1280 705]);
        drawnow
    end