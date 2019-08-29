# aTAV
Exploratory data analysis and flitering of incoming material lots inspection data for TAV (Ti-6Al-4V)


### ASTM-F136.py

The incoming material inspection data on TAV alloys for medical device companies has to be (or could be/should be) in compliance with ASTM-F136. This standard put acceptance
criteria on mechanical performance (modulus, yield strength, ultimate strength and elongarion) for different lot geometries. This code filters 
the `CSV` file input according to the standard and create a filetered `CSV` sheet file with accepted lot. The following table is the accepted critera:

| Nominal Diameter (mm)  | Yield Strength (MPa)   | UTS (MPa)  | Elongation % | 
| ------------- |:-------------:|:-----:| -----:|
|  < 4.75      | 795 | 860 | 10 |
|  4.75 - 44.45      | 795     |   860 | 10 |
| 44.45 - 63.5 | 760      |    825 | 8 |
| 63.5 - 101.6 | 760      |    825 | 8 |



### Plotting_Stats.py

This code plots series of scatter plots and histogram of input database for the purpose of Exploratory Data Analysis (EDA). The missed data points are replaced with `NaN` that can be handled
easily by `NumPy` and consequently `Seaborn` libraries.

### Prbability.py

The probability of mechanical performance is of interest.

*Definitions:*

**Mechanical performance:** Mechanical performance of a material lot is defined via its Young's modulus, yield strength and ultimate strength. The higher these 
values the higher performance the material has in mechanical strength and stiffness. 

**Lower peformance probability (P_l):** Is defined as the probability of performing any lot lower than the rest of the lots within some inference space (~4%).

**Higher peformance probability (P_h):** Is defined as the probability of performing any lot higher than the rest of the lots within some error space (~4%).

For example, a material with high P_l has very low P_h, and vice versa.

The material that performs around **P_l ~ P_h ~ 0.5** considers the average performance or a *typical* lot. The lowest performance is the material with the least P_h (essentially zero), and the highest performance is the material with the most P_l.
