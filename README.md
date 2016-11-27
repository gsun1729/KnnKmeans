# Modeling and Predicting Behavior
## Objective
The purpose of this program is to analyze biometric data to recognize deviant changes in behavior and predict future behavior output.
This program was designed and developed for BIOE 553, Systems Biology and Neuroengineering, for the purpose of diagnosing neural state.
## Background
Current diagnostic tools for neurodegeneration are highly invasive, time consuming, and economically unfeasible.  While accurate, they are limited in long duration high frequency time point sampling for patient health monitoring and prognosis of neural state progression.  For these reasons, an alternative strategy for disease state evaluation is desperately needed for long term patient monitoring and subsequent proper treatment of disease progression outcomes.

Prior research has demonstrated neurodegeneration influences behavioral routines, albeit at various degrees dependent on disease state.  Basic routines, including and not limited to computer use, physical activity, and sleep patterns, have been implicated in neurodegenerative disease pathogenesis.  Under the premise that behavior impacts neural state, and that neural state influences behavior, we have developed an algorithmic approach for monitoring and identifying significant behavioral change over long time periods.  With the emergent popularity of activity trackers, such as Apple health, Google fit, and Fitbit trackers, our approach allows for dissection and interpretation of physiological and behavioral data to achieve diagnosis of neural state.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/IO.png" alt="alt text">
<p>
<b>Figure 1:</b> Controlled behavioral input is characterized by non-uniform behavioral output.  Nonetheless, there will be some metrics of behavior that are influenced by disease state.  For the top two cases, there will be some stimuli by which both diseased and normal patients respond similarly; however other stimuli can result in abnormal behavior.

Using various clustering and machine learning algorithms, this approach analyzes local and global histories of behavior and their emergent patterns to predict behavioral output changes as a recursive function of prior behavioral output history.  In particular, this method implements K-means clustering with a fast Fourier transform extrapolation to estimate future behavior output trajectories based on training parameters set by behavioral output.  Additionally, this method is not limited by dimensionality of a dataset, although for data visualization may not be possible for dimensions greater than 3.

## Fundamental Assumptions
Because behavioral output is highly variable at small time scales, in order to evaluate long term behavior we implement the following assumptions:
* Behavioral routines are cyclical
* Continuous small alterations in behavior integrated over time should alter behavioral clusters over time
* Insidious changes in behavior can be characterized by slow gradual change over time. Large fluctuations in change are less likely to predict neurodegeneration, a process that typically takes years before disease state realization.

# K-means Sliding Window
In order to obtain time-scale data, the global history of patient data is partitioned via a sliding window of size S.  To generate each timepoint, the window advances foward I days per iteration and the local history contained within the window is subject to K-means clustering.  The cluster centroids are then accepted as a representation of the average behavior observed over that window.  Because of  the sliding window, subsequent data will be added and removed in a first in, first out manner, resulting in an overlap of S-I days between consecutive windows (Figure 2,3).

![alt Local Window Scan](https://raw.githubusercontent.com/gsun1729/Optimized-Kmeans/master/images/local_scan.png)
<p>
<b>Figure 2:</b> Scanning methodology of the sliding window.  With each iteration, the window moves fowards by I days.  Data in each window is then used to predict behavioral output for the next P days (red line).
<p>
<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/process.png" alt="alt text" height="200" >
<p>
<b>Figure 3:</b> Data processing methodology.  
<p>

To optimize for the number of clusters, we utilized the elbow method, in which each window is clustered into 0 through k clusters.  The difference in sum of squared errors(SSE) is evaluated for each clustering.  This permits percentage of variance to be explained as a function of the number of clusters.  Because the optimal number of clusters should be where addition or reduction of the number of clusters does not yield better modeling of the data, the number of clusters selected is at the point where the marginal gain of adding more clusters drops.  This "elbow" is calculated via drawing a line from the SSE for 0 to k clusters, where k at maximum is the nubmer of points in the dataset.  The maximum orthogonal distance from each point (k,SSE) to the line will yield the point where addition of more clusters does not result in a better model.  This maximum distance is then correlated to its corresponding point to yield the optimal number of clusters, k<sub>O</sub> (Figure 4,5).  

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/elbow.png" alt="alt text" height="200" >
<p>
<b>Figure 4:</b> The optimal number of clusters is determined by the point where addition or subtraction of more clusters does not yield a better model fit, which is represented on the graph where the "elbow bend" occurs.  This point is determined by drawing a line (red) connecting the first and last SSE vs k data point and evaluating where the maximum orthogonal distance (green) from each point to the line occurs.  This iteration was run with categories 4 and 12 with a window of size 14.

<img src="https://github.com/gsun1729/Optimized-Kmeans/blob/master/images/export_2D_w14_c4,12/export_avgSSEdist_k.png" alt="alt text">
<p>
<b>Figure 5:</b> The site at which the maximum orthogonal distance occurs is marked by the highest peak in this plot.  This iteration was run with categories 4 and 12 with a window of size 14.

The optimal number of clusters (k<sub>O</sub>) were then used to cluster each window.  Because  k<sub>O</sub> varies window to window, comparison between windows is achieved by evaluating the minimum path distance between the cluster centroids, and for two dimensional cases, the area encapsulated by the centroids.


