# Modeling and Predicting Behavior
## Objective
The purpose of this program is to analyze biometric data to recognize deviant changes in behavior and predict future behavior output.
This program was designed and developed for BIOE 553, Systems Biology and Neuroengineering, for the purpose of diagnosing neural state.
## Background
Current diagnostic tools for neurodegeneration are highly invasive, time consuming, and economically unfeasible.  While accurate, they are limited in long duration high frequency time point sampling for patient health monitoring and prognosis of neural state progression.  For these reasons, an alternative strategy for disease state evaluation is desperately needed for long term patient monitoring and subsequent proper treatment of disease progression outcomes.

Prior research has demonstrated neurodegeneration influences behavioral routines, albeit at various degrees dependent on disease state.  Basic routines, including and not limited to computer use, physical activity, and sleep patterns, have been implicated in neurodegenerative disease pathogenesis.  Under the premise that behavior impacts neural state, and that neural state influences behavior, we have developed an algorithmic approach for monitoring and identifying significant behavioral change over long time periods.  With the emergent popularity of activity trackers, such as Apple health, Google fit, and Fitbit trackers, our approach allows for dissection and interpretation of physiological and behavioral data to achieve diagnosis of neural state.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/IO.png" alt="alt text" height="300">
<p>
<b>Figure 1:</b> Controlled behavioral input is characterized by non-uniform behavioral output.  Nonetheless, there will be some metrics of behavior that are influenced by disease state.  For the top two cases, there will be some stimuli by which both diseased and normal patients respond similarly; however other stimuli can result in abnormal behavior.

Using various clustering and machine learning algorithms, this approach analyzes local and global histories of behavior and their emergent patterns to predict behavioral output changes as a recursive function of prior behavioral output history.  In particular, this method implements K-means clustering with a fast Fourier transform extrapolation to estimate future behavior output trajectories based on training parameters set by behavioral output.  Additionally, this method is not limited by dimensionality of a dataset, although for data visualization may not be possible for dimensions greater than 3.

## Fundamental Assumptions
Because behavioral output is highly variable at small time scales, in order to evaluate long term behavior we implement the following assumptions:
* Behavioral routines are cyclical
* Continuous small alterations in behavior integrated over time should alter behavioral clusters over time
* Insidious changes in behavior can be characterized by slow gradual change over time. Large fluctuations in change are less likely to predict neurodegeneration, a process that typically takes years before disease state realization.

## K-means Sliding Window
In order to obtain time-scale data, the global history of patient data is partitioned via a sliding window of size S.  To generate each timepoint, the window advances foward I days per iteration and the local history contained within the window is subject to K-means clustering.  The cluster centroids are then accepted as a representation of the average behavior observed over that window.  Because of  the sliding window, subsequent data will be added and removed in a first in, first out manner, resulting in an overlap of S-I days between consecutive windows (Figure 2,3).

<img src="https://raw.githubusercontent.com/gsun1729/Optimized-Kmeans/master/images/local_scan.png" alt="alt text" height="300" >
<p>
<b>Figure 2:</b> Scanning methodology of the sliding window.  With each iteration, the window moves fowards by I days.  Data in each window is then used to predict behavioral output for the next P days (red line).
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/process.png" alt="alt text" height="400" >
<p>
<b>Figure 3:</b> Data processing methodology.  
<p>

To optimize for the number of clusters, we utilized the elbow method, in which each window is clustered into 0 through k clusters.  The difference in sum of squared errors(SSE) is evaluated for each clustering.  This permits percentage of variance to be explained as a function of the number of clusters.  Because the optimal number of clusters should be where addition or reduction of the number of clusters does not yield better modeling of the data, the number of clusters selected is at the point where the marginal gain of adding more clusters drops.  This "elbow" is calculated via drawing a line from the SSE for 0 to k clusters, where k at maximum is the nubmer of points in the dataset.  The maximum orthogonal distance from each point (k,SSE) to the line will yield the point where addition of more clusters does not result in a better model.  This maximum distance is then correlated to its corresponding point to yield the optimal number of clusters, k<sub>O</sub> (Figure 4,5).  

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/elbow.png" alt="alt text" height="300" >
<p>
<b>Figure 4:</b> The optimal number of clusters is determined by the point where addition or subtraction of more clusters does not yield a better model fit, which is represented on the graph where the "elbow bend" occurs.  This point is determined by drawing a line (red) connecting the first and last SSE vs k data point and evaluating where the maximum orthogonal distance (green) from each point to the line occurs.  This iteration was run with categories 4 and 12 with a window of size 14.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4,12/export_avgSSEdist_k.png" alt="alt text" height="300">
<p>
<b>Figure 5:</b> The site at which the maximum orthogonal distance occurs is marked by the highest peak in this plot.  This iteration was run with categories 4 and 12 with a window of size 14.

The optimal number of clusters (k<sub>O</sub>) were then used to cluster each window.  Because  k<sub>O</sub> varies window to window, comparison between windows is achieved by evaluating the minimum path distance between the cluster centroids, and for two dimensional cases, the area encapsulated by the centroids.  On the first iteration, centroid locations are selected using the Forgy method; and adjusted accordingly.  With each advancement of the window, the previous window's centroids are fed as initial centroids into the next K-means iteration to allow for continuity of centroid migration.  If the optimal number of clusters is less than the number of existing centroids, centroids will be randomly selected for removal.  Likewise, if the optimal number of clusters is greater, additional centroids will be selected from the existing dataset via the Forgy method.

## Operation
This program runs primarily off of fitbit data.  This can be obtained by downloading a .csv file of fitbit data [here](http://fitbit-export.azurewebsites.net/).  A sample input datafile has been included in the directory [here](https://github.com/gsun1729/Optimized-Kmeans/blob/master/sample_data.csv)

To initialize the program, the user must supply the following inputs:
* Input data filename
* Window Size
* Output Filename (optional)
* Maximum number of iterations (for the number of iterations to run Kmeans, optional)

Syntax for running the program with the listed arguments is as follows:


python kmeans.py - i input_filename -w window_size -m max_iterations -o output_filename


Once running the user specifies the number of dimensions to analyze and the categories for analysis, which are listed below:

0. dateTime
1. activities-calories
2. activities-caloriesBMR
3. activities-steps
4. activities-distance
5. activities-floors
6. activities-elevation
7. activities-minutesSedentary
8. activities-minutesLightlyActive
9. activities-minutesFairlyActive
10. activities-minutesVeryActive
11. sleep-timeInBed
12. sleep-minutesAsleep
13. sleep-awakeningsCount
14. sleep-minutesAwake
15. sleep-minutesToFallAsleep
16. sleep-minutesAfterWakeup

## Data Analysis
For this part, window size was set to 14 days.  This is based on the assumption that it takes two weeks for any behaviors to cement within a user's routine.  Window size however can be adjusted according to need--note larger windows will mean that the influence of new queued data will have a lesser influence on centroid migration, and too small of a window will result in large influence on centroid migration.
### 2-Dimensional Datasets
The following data was generated using categories 4 and 12 (activities-distance, and sleep-minutesAsleep).
As observed in Figure 6, variation in cluster centroids varies significantly with each movement of the window, and centroid number differs with each advancement.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4%2C12/export_2D.gif" alt="alt text" height="450" >
<p>
<b>Figure 6:</b> Centroid migration and area calculation with each advancement of scanning window.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4%2C12/export_SSE_k.png" alt="alt text" height="450" >
<p>
<b>Figure 7:</b> SSE calculation for k optimization highlights the variability of optimal k with each window

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4%2C12/export_SSEdist_k.png" alt="alt text" height="450" >
<p>
<b>Figure 8:</b> SSE maximum variation calculation for k.

Because the input dataset is of two dimensions, we can visualize the area encapuslated by the centroid verticies and minimum path distance.  Note for this case, the area encapsulated is representative of activity-distance multiplied by sleep-minutesAsleep.  A large area would indicate wider variation in the dataset.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4%2C12/export_area_time.png" alt="alt text" height="450" >
<p>
<b>Figure 9:</b> Centroid polygon area as a function of time. 

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4%2C12/export_CMPD_time.png" alt="alt text" height="450" >
<p>
<b>Figure 10:</b> Cluster centroid minimum path distance as a function of time.

While both the minimum path distance and polygon area are capable of detecting change, the area analysis is much more sensitive than the path distance method, as change in any centroid is correlated with the area being scaled up or down.  Path distance is more lenient to smaller changes, as a small centroid deviation would not necessarily impact the rest of the centroids.  In other words, a small movement of one of the centroid points would influence the area encapsulated by the entire polygon, but could slightly alter the minimum path length, as each centroid would have a radius of change in which the centroid could move without altering the minimum path length.

### 8 dimensional analysis.
Although K-means requires at most 1 dimension to work, lower dimensionality results in higher sensitivity to change.  Considering the variability of behavior, this could be a major set back to behavioral modeling and prediction in that high sensitivity at lower dimensions would result difficulty distinguishing between significant and gradual changes in behavior.

To evaluate the functionality of higher dimension analysis, we analyzed 8 dimensions of behavioral data, namely categories (3, 4, 8-10, 12-14).  Window size was set to 14 days.  One limitation of analyzing higher dimensions is that the area analysis is no longer applicable. However, it is significantly better at recognizing significant patterns in behavioral change, as illustrated in Figure 13, where the minimum centroid path distance recognizes at day 10 and 40 times when I was traveling, as well as the increased physical activity in between.

Additionally, k<sub>O</sub>  is subject to less variation without significant perturbation of the system, as shown in figures 11,12, where k<sub>O</sub> is largely conserved at 2-3 clusters.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/export_w14_c8D_SSE_k.png" alt="alt text" height="450" >
<p>
<b>Figure 11:</b> SSE vs k for k<sub>O</sub> determination.  Note the similarity of plots with each window iteration.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/export_w14_c8D_SSEdist_k.png" alt="alt text" height="450" >
<p>
<b>Figure 12:</b> SSE max distance for k<sub>O</sub> determination.  Although there are a few iterations where the maximum distance oscillates, the majority of distance plots recognize 2-3 clusters as the optimal k<sub>O</sub>.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/export_w14_c8D_pathdist.png" alt="alt text" height="450" >
<p>
<b>Figure 13:</b> Cluster Centroid Minimum path distance.  At time points 10,40 (windows), we observe the algorithm recognize a significant change in behavior due to travel, as well as maintenance of different behavior during the travel period.

## Prediction and Extrapolation
In order to predict the next D days of activity, we implement a fast fourier transform.  Under the assumption that behavioral routines are cyclic, we adjusted the number of harmonics to 14, the same length as the training window under the assumption that the highest frequency of change observable is daily and the lowest frequency of change observable is once per two weeks.  The predictive window length was set to 5 days.

Under this schema, the fourier transform was then used to predict future behavior under two different schemes, the first identical to the one illustrated in figure 2, and the second using a cumulative window in which the window elongates with each iteration (Figure 14).
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/cumulative_scan.png" alt="alt text" height="450" >
<p>
<b>Figure 14:</b> Cumulative window scanning operation.  Each prediction is now based on the entirety of prexisting data, as opposed to the shifting window method (Figure 2).

### Scrolling Window Extrapolation
Under the scrolling window extrapolation, we observe higher sensitivity to small changes in behavior as expected and larger variation in SSE.  One of the significant limitations of this method is that by sampling only the local window history to determine the extrapolation function, only behaviors exhibited in the window are accounted in the future prediction, without accounting for the previous range of behaviors (prior to the window).  This however could also be interpreted as a strength, expecially for examining short term behavior where older behavior does not influence present behavior (i.e. eating a cheesecake two months ago is not going to affect your propensity for cheesecake now).
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/scrolling_window_extrapolation.gif" alt="alt text" height="450" >
<p>
<b>Figure 15:</b> Extrapolation under the scrolling window schema.  Note how due to the sinusoidal nature of the FFT, changes in behavior are assumed to be cyclic, which may result in the algorithm consistently overpredicting a change in a period of stability.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/local_window.png" alt="alt text" height="450" >
<p>
<b>Figure 16:</b> SSE of extrapolation with actual historical result indicates that the scrolling window method is influenced by large changes beyond the change itself--the system resembles that of an under-damped system due to the heightened sensitivity induced by the smaller window.
### Cumulative Window Extrapolation
Under the cumulative window extrapolation method, we observe at the beginning of the session significant over prediction, similar to that of the scrolling window.  However, due to the cumulative effect of the additional data, the system begins more like an overdamped system as the extrapolation moves forward.  Furthermore, we observe decreased sensitivity in SSE with regards to significant changes in behavior, as illustrated in figure 18.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/cumulative_window_extrapolation.gif" alt="alt text" height="450" >
<p>
<b>Figure 17:</b> Extrapolation and prediction under the cumulative window schema.  Although the model starts out poorly in the beginning, this is largely due to lack of data.  The beginning is similar to the scrolling window, in that the window is still considered small.  For instance, the first few windows, the window size will be 5,6,7,8,...; however the scrolling window has a constant window size of 5.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/cumulative_window_SSE.png" alt="alt text" height="450" >
<p>
<b>Figure 18:</b> SSE of extrapolation with actual historical result indicates that the cumulative scrolling window method is less influenced by large changes beyond the incident itself.  Large peaks could be used to predict large deviant behaviors, while smaller inclines could be used to characterize gradual change.

### Global Extrapolation
Although FFT extrapolation works very well in modeling the data (Figure 19), one of its limitations arises from its cyclic nature.  Because it assumes that behavior can be cyclic, it cannot predict beyond half a period outside of the training data.  This is best illustrated by figure 20, in which we observe that the extrapolation assumes continuity of behavioral patterns and poorly predicts the future by reiterating the training data.  This however can be corrected by increasing the number of harmonics in the FFT extrapolation.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/global_extrapolation_w14_p3_h14.png" alt="alt text" height="450" >
<p>
<b>Figure 19:</b> Global extrapolation of historical data.
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_w14_chx_0x513CA9F162/Historical_extrapolation_d100.png" alt="alt text" height="450" >
<p>
<b>Figure 20:</b> Predicting beyond the training data length can result in assuming that the present pattern will continue.
