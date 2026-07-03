# Dynamic Vaccine Prioritization via Non-Markovian Final-state Optimization

This repository contains the code, data products, figures, and manuscript files for the project **Dynamic Vaccine Prioritization via Non-Markovian Final-state Optimization**.

The project studies age-stratified, non-Markovian epidemic dynamics and dynamic vaccine allocation. It compares allocation strategies that minimize different final epidemic burdens, including cumulative infections (`c`), deaths (`d`), and years of life lost (`y`), and generates the analysis tables and figures used in the manuscript.

## Repository Layout

```text
.
|-- AnalysisCode/        # Scripts that aggregate raw experiment outputs into analysis workbooks
|-- AnalysisData/        # Generated analysis workbooks used by plotting scripts
|-- Dependencies/        # Shared model code, helper utilities, and input data dependencies
|-- ExperimentalCode/    # Experiment entry points and task implementations
|-- ExperimentalData/    # Generated experiment workbooks
|-- ExtensionCode/       # Optional C++/Python extension source and build files
|-- Figure/              # Generated and assembled figures
|-- FigureCode/          # Figure drawing scripts
|-- RefinementCode/      # Refinement workflow scripts
`-- Text/                # Manuscript, supplementary material, submission PDFs, and responses
```

## Environment

The codebase is Python-based and uses common scientific Python packages. A typical environment should include:

```bash
pip install numpy pandas scipy matplotlib seaborn scikit-learn openpyxl filelock
```

Some workflows use a compiled extension named `metapopulation_simulation`. Prebuilt platform-specific binaries are present in the repository under `ExperimentalCode/experiments/elements/` and `ExtensionCode/`. If you need to rebuild it, use the setup script under the relevant extension folder, for example:

```bash
cd ExtensionCode/metapopulation_simulation_mac
python setup.py build_ext --inplace
```

On Windows, the Visual Studio solution is under `ExtensionCode/metapopulation_simulation/`.

## Data Dependencies

Input data used by the model are stored under `Dependencies/DataDependencies/`, including:

- COVID-19 time series data
- contact matrices
- population data
- infectiousness profiles
- vaccination data

Generated outputs are stored separately:

- `ExperimentalData/`: per-task simulation outputs
- `AnalysisData/`: aggregated workbooks consumed by plotting code
- `Figure/`: generated PDF panels and assembled image/Illustrator files

## Running Experiments

Experiment definitions live in `ExperimentalCode/experiments/`, and valid task names and parameter values are registered in `ExperimentalCode/task_info.py`.

The main entry point is:

```bash
cd ExperimentalCode
python main.py <task_idx> <task_amount> <expr_name> <task_param>
```

For example, on a Linux/SLURM worker:

```bash
python main.py 0 40 optm_from_param r0
```

`task_idx` and `task_amount` split a large experiment into independent work chunks. The SLURM template in `ExperimentalCode/submit_job.sh` shows how to launch all chunks in parallel.

Note: the Windows/macOS branch in `ExperimentalCode/main.py` contains local debugging placeholders. For reproducible runs, pass explicit command-line arguments on Linux or edit the local branch deliberately before running.

## Running Analysis

Analysis scripts load experiment files from `ExperimentalData/` and write aggregated Excel workbooks to `AnalysisData/`.

```bash
python AnalysisCode/analysis_main.py
```

Before running, set the `additional_task_dict` and `anal_list` variables in `AnalysisCode/analysis_main.py` to the experiment outputs and analysis functions you want to regenerate. Individual analysis functions are in `AnalysisCode/analysis_func/`.

## Generating Figures

Figure scripts load workbooks from `AnalysisData/` and write figure panels to `Figure/`.

```bash
python FigureCode/figure_main.py
```

Before running, set `anal_list` and `fig_dict` in `FigureCode/figure_main.py` to the required analysis datasets and figure panels. Drawing modules are in `FigureCode/figure_func/`, with shared plotting helpers under `FigureCode/figure_func/figure_dependencies/`.

## Manuscript Files

The manuscript source and compiled submission materials are under `Text/`:

- `Text/Response-of-Time-Course-Optimal-Vaccine-Prioritization/MainText/`
- `Text/Response-of-Time-Course-Optimal-Vaccine-Prioritization/SupplementaryMaterial/`
- `Text/Final_Submission/`

The main manuscript title is:

> Dynamic Vaccine Prioritization via Non-Markovian Final-state Optimization

## Notes for Reproduction

- Many experiment outputs are large Excel workbooks. Regenerating all experiments can be computationally expensive and is intended for parallel execution.
- Existing `AnalysisData/` and `Figure/` files can be used directly to inspect or regenerate figures without rerunning every simulation.
- Task output paths are controlled by `Dependencies/FrameDependencies/name_principle.py`.
- The `.gitignore` treats large data, outputs, figures, and text build products as generated artifacts, even though this working copy may include them for local reproduction.
