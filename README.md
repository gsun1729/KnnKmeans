# Modeling and Predicting Behavior
## Objective
The purpose of this program is to analyze biometric data to recognize deviant changes in behavior and predict future behavior output.
This program was designed and developed for BIOE 553, Systems Biology and Neuroengineering, for the purpose of diagnosing neural state.
## Background
Current diagnostic tools for neurodegeneration are highly invasive, time consuming, and economically unfeasible.  While accurate, they are limited in long duration high frequency time point sampling for patient health monitoring and prognosis of neural state progression.  For these reasons, an alternative strategy for disease state evaluation is desperately needed for long term patient monitoring and subsequent proper treatment of disease progression outcomes.

Prior research has demonstrated neurodegeneration influences behavioral routines, albeit at various degrees dependent on disease state.  Basic routines, including and not limited to computer use, physical activity, and sleep patterns, have been implicated in neurodegenerative disease pathogenesis.  Under the premise that behavior impacts neural state, and that neural state influences behavior, we have developed an algorithmic approach for monitoring and identifying significant behavioral change over long time periods.  With the emergent popularity of activity trackers, such as Apple health, Google fit, and Fitbit trackers, our approach allows for dissection and interpretation of physiological and behavioral data to achieve diagnosis of neural state.

Using various clustering and machine learning algorithms, this approach analyzes local and global histories of behavior and their emergent patterns to predict behavioral output changes as a recursive function of prior behavioral output history.  In particular, this method implements K-means clustering with a fast Fourier transform extrapolation to estimate future behavior output trajectories based on training parameters set by behavioral output.

## Fundamental Assumptions
Because behavioral output is highly variable at small time scales, in order to evaluate long term behavior we implement the following assumptions:
* Continuous small alterations in behavior integrated over time should alter behavioral clusters over time
* Insidious changes in behavior can be characterized by slow gradual change over time. Large fluctuations in change are less likely to predict neurodegeneration, a process that typically takes years before disease state realization.
* Behavioral routines are cyclical in the long term



Because controlled stimuli do not predicate uniform behavioral output, this method uses clustering to normalize the spectrum of output.  By using center of mass (except with distance) weighing of data, a behavioral average can be determined.

