clear variables; close all;
colors = gray(5);
path = load('jython/ts_rhc.mat');
colordef black
set(0,'DefaultFigureWindowStyle','docked')
names = fieldnames(path);
ax=[];
%for i = 1:length(names)
%  n = names{i};
  
  
  routes = {'RHC', 'SA'};
  
  for r = 1:numel(routes)
  curves = {[routes{r} '_fitness'] [routes{r} '_iterations']}
      %for c = 1:2
      fitstr = curves(1)
      iterstr = curves(2)
      figure('Name', fitstr{:}, 'NumberTitle', 'off');
      fitness = path.(fitstr{:});
      iters = path.(iterstr{:});
      plot(iters,fitness);
   %end
      
      figure('Name',routes{r},'NumberTitle','off');
      %set(gca,'position',[0.03 0.03 1 1])
      ax(end+1) = gca;
      %plot(path.RHC_fitness)
      p = path.(routes{r});
      %%
      hold on
      cols = 10;%length(path.(n));
      rows = length(fitness);
      for j = 1:rows
          %p = path.(names{i});
          xInd= (j-1)*2 +1;
          yInd = xInd+1;
          X = p(xInd,1:cols);
          Y = p(yInd,1:cols);
          scatter(X, Y) %,   plot(X, Y, '-y', 'Color', colors(2,:));
      end
      plot(X,Y,'r');
  hold off
  
  
  

end