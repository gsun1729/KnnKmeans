# Modeling and Predicting Behavior
## Objective
The purpose of this program is to analyze biometric data to recognize deviant changes in behavior and predict future behavior output.
This program was designed and developed for BIOE 553, Systems Biology and Neuroengineering, for the purpose of diagnosing neural state.
## Background
Current diagnostic tools for neurodegeneration are highly invasive, time consuming, and economically unfeasible.  While accurate, they are limited in long duration high frequency time point sampling for patient health monitoring and prognosis of neural state progression.  For these reasons, an alternative strategy for disease state evaluation is desperately needed for long term patient monitoring and subsequent proper treatment of disease progression outcomes.

Prior research has demonstrated neurodegeneration influences behavioral routines, albeit at various degrees dependent on disease state.  Basic routines, including and not limited to computer use, physical activity, and sleep patterns, have been implicated in neurodegenerative disease pathogenesis.  Under the premise that behavior impacts neural state, and that neural state influences behavior, we have developed an algorithmic approach for monitoring and identifying significant behavioral change over long time periods.  With the emergent popularity of activity trackers, such as Apple health, Google fit, and Fitbit trackers, our approach allows for dissection and interpretation of physiological and behavioral data to achieve diagnosis of neural state.

Because controlled stimuli do not predicate uniform behavioral output, this method uses clustering to normalize the spectrum of output.  By using center of mass (except with distance) weighing of data, a behavioral average can be determined.

## Fundamental Assumptions
Behavior is cyclical
Alterations in behavior should alter the clustering average over time
Insidious change can be characterized by slow gradual change over time. Large fluctuations of change are less likely to predict neurodegeneration, a process that typically takes years before disease state realization
