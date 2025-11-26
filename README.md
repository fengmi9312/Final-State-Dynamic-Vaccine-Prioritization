# Time-Course-Optimal-Vaccine-Prioritization

Overview

This repository implements a long-term vaccine allocation framework for epidemic control when transmission has memory. Many benefits of vaccination emerge only long after vaccination; short-horizon rules overweight immediate outcomes and miss indirect effects of vaccination. We build an age-structured non-Markovian model with a fast final-state predictor obtained by mapping the non-Markovian final state to an equivalent Markovian representation. At each decision point, the policy uses this predictor to choose the allocation that minimizes the eventual epidemic burden, balancing transmission blocking with direct protection as incidence, immunity, and coverage evolve.
Due to the long-horizon perspective, our strategy substantially outperforms static policies and short-term heuristics that focus only on immediate direct effects.

The analysis reveals two shift patterns that explain how priorities change over time. When R0 is low, marginal benefits across leading groups gradually converge and allocation rebalances smoothly (partial switch). 
When R0 is high, marginal benefits cross sharply and the policy flips priority between groups (full switch). 
Revealing this mechanism could guide when and how vaccination should shift between population groups
We demonstrate the approach on multiple countries, showing how optimal strategies adapt to demographics, contact patterns, and epidemic stage, while remaining robust across a broad class of mechanistic models.

Overall, our study makes long-term prediction tractable in general memory-dependent epidemic systems and offers practical guidance for vaccine deployment. 
It overcomes a key limitation of prior work by explicitly balancing direct and indirect effects, providing implementable procedures for real-time prioritization. 
Beyond improving performance, this framework also establishes a mechanistic basis for dynamic allocation, clarifying when and how vaccination priorities should shift across population groups.

Repository layout

ExperimentalCode runs the simulations and the predictor-guided allocation loops used in the study.
AnalysisCode reads experimental outputs and produces the plotting datasets used in the paper.
FigureCode takes those plotting datasets and renders the figures.
