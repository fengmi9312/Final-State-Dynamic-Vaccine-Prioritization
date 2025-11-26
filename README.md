# Time-Course-Optimal-Vaccine-Prioritization

Preprint: arXiv:2511.07200

Overview

This repository implements a long-horizon vaccine allocation framework for epidemic control when transmission has memory. Many benefits of vaccination emerge late; short-horizon rules overweight immediate outcomes and miss indirect protection. We pair an age-structured non-Markovian model with a fast final-state predictor obtained by mapping the non-Markovian final state to an equivalent Markovian representation. At each decision point, the policy uses this predictor to choose the allocation that minimizes the eventual epidemic burden, balancing transmission blocking with direct protection as incidence, immunity, and coverage evolve.

The analysis reveals two shift patterns that explain how priorities change over time. When R0 is low, marginal benefits across leading groups gradually converge and allocation rebalances smoothly (partial switch). When R0 is high, marginal benefits cross sharply and the policy flips priority between groups (full switch). We demonstrate the approach on multiple countries, showing how optimal strategies adapt to demographics, contact patterns, and epidemic stage, while remaining robust across a broad class of mechanistic models.

Repository layout

ExperimentalCode runs the simulations and the predictor-guided allocation loops used in the study.
AnalysisCode reads experimental outputs and produces the plotting datasets used in the paper.
FigureCode takes those plotting datasets and renders the figures.
