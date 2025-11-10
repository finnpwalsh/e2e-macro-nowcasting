# End-to-End Macro Nowcasting
## Overview
Real-time inflation nowcasting system built on a full MLOps stack. This project serves both as an applied investigation into machine learning pipeline production and as an introduction to operational best practices in model deployment and monitoring practices.

### Contents
1. [Inspiration](#inspiration)
2. [Repository Architecture](#repo-architecture)
3. [Tech Stack & Workflow](#stack--workflow)
4. [Modeling & Forecasting](#model--forecast)
5. [Future Work](#future-work)

## Inspiration
### Inflation Nowcasting
In Fall 2025, I participated in the University of Pittsburgh's National College Federal Reserve Challenge team as a Price Level & Inflation team member. The team's goal was to anticipate the Federal Reserve's short-term policy decision through a combination of theoretical analysis and empirical modeling. 

I focused on analyzing how real-time inflation nowcasts influence the Fed's assessment of economic conditions and subsequency policy responses.

#### What is inflation nowcasting?
Actual inflation cannot be observed in real time. Thus, agencies like the Bureau of Labor Statistics (BLS) and the Bureau of Economic Analysis (BEA) release official inflation data monthly after substantial revisions and testing. Inflation nowcasting is the process of estimating inflation metrics, like PCE and CPI, more frequently than official releases.

#### When is official release data insufficient?
Companies and financial entities often require high frequency inflation updates to optimize their decision-making. For example, large retailers like Walmart use nowcasts to improve profit margins by monitoring cost-push inflation.