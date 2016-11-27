clear all; close all; clc;
input_filename = 'export_w14_chx_0x513CA9F162'

num_scans = 49;


SSE_filename = strcat(input_filename,'_SSE.csv');
SSE_dist_filename = strcat(input_filename,'_SSE_dist.csv');
Area_filename = strcat(input_filename,'_area.csv');
path_filename = strcat(input_filename,'_pathdist.csv');

% Tracemap_filename = strcat(input_filename,'.output_TraceMap');
% Centroids_filename = strcat(input_filename,'.output_centroids');
% Points_filename = strcat(input_filename,'.output_points');


SSEs = csvread(SSE_filename);
SSE_dist = csvread(SSE_dist_filename);
% area = csvread(Area_filename);
paths = csvread(path_filename);
%% plot the path distances
x = 1:length(paths);
plot(x,paths)
title('Cluster Path Distance vs Time');
xlabel('Window Advancement (days)');
ylabel('Cluster Minimum Path Distance');


%% 2D Plot SSE and avg(SSE) Vs Cluster Number
figure
hold on;
x_avg = zeros(length(SSEs(:,1)),1);
y_avg = zeros(length(SSEs(:,1)),1);
for k = 2:1:length(SSEs(1,:))
   x = SSEs(:,1);
   y = SSEs(:,k);
   x_avg = x_avg + x./length(SSEs(1,:));
   y_avg = y_avg + y./length(SSEs(1,:));
   plot(x',y','color',rand(1,3));
end

title('SSE vs Clustering k');
xlabel('Number of clusters k');
ylabel('Sum of Squared Errors');

figure 
plot(x_avg,y_avg)
title('Average SSE vs Clustering k');
xlabel('Number of clusters k');
ylabel('Sum of Squared Errors');
%% 2D Plot SSE dist vs cluster number 
figure
hold on;
xd_avg = zeros(length(SSE_dist(:,1)),1);
yd_avg = zeros(length(SSE_dist(:,1)),1);
for k = 2:1:length(SSE_dist(1,:))
   x = SSE_dist(:,1);
   y = SSE_dist(:,k);
   xd_avg = xd_avg + x./length(SSE_dist(1,:));
   yd_avg = yd_avg + y./length(SSE_dist(1,:));
   plot(x',y','color',rand(1,3));
end
title('SSE Curvature vs Clustering k');
xlabel('Number of clusters k');
ylabel('Sum of Squared Errors Curvature Radius');

figure 
plot(xd_avg,yd_avg);
title('Average SSE Curvature vs Clustering k');
xlabel('Number of clusters k');
ylabel('Sum of Squared Errors Curvature Radius');

%% 2D delta_area
figure;
x = 1:1:length(area);
plot(x,area);
title('2D Area vs Time');
ylabel('Area (arbitrary units)');
xlabel('Time (window shift)');



%% 2D Plot Scatters
clear all; close all; clc;
input_filename = 'export_w14_c4_c12'

num_scans = 49;
figure;

for o = 1:num_scans
    c_file = strcat(input_filename,'_c',num2str(o),'.csv');
    p_file = strcat(input_filename,'_w',num2str(o),'.csv');
    c_file
    p_file
    centroids = csvread(c_file);
    points = csvread(p_file);
	drawnow
    cla
    hold on
    scatter(centroids(:,1),centroids(:,2),'ro','filled');
    scatter(points(:,1),points(:,2),'b+');
    h = fill(centroids(:,1),centroids(:,2),'b');
%     set(h,'facealpha',.5);
    title(strcat('Window ',num2str(o)));
    xlabel('Distance Traveled (km)');
    ylabel('Minutes Asleep');
    legend('Centroids','Data Points');
    axis([0, 21, 0, 800]);
    hold off;
    frame = getframe(1);
    im{o} = frame2im(frame);

end


filename = 'export_2D.gif';
for x = 1:num_scans
    [A,map] = rgb2ind(im{x},256);
    if x == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',1);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',1);
    end
end