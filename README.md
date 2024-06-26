# Causal Multi-Omics Recommender pipeline

![Alt Text](figures/fp_magnets.gif)

## Introduction

TODO

## Pipeline summary

TODO

## Usage

```bash
 N E X T F L O W   ~  version 24.04.2

Launching `main.nf` [desperate_curie] DSL2 - revision: f2e9fa2fcf

Typical pipeline command:

  nextflow run main.nf --features input_file.csv --phenotype_column phenotype

Input/output options
  --project_name     [string]  A name for the project, used for output file names.
  --features         [string]  The dataset with the features
  --phenotype_column [string]  The phenotype column name
  --outdir           [string]  The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure. 
                               [default: results] 

Models parameters
  --alpha_high       [number]  null [default: 0.02]
  --alpha_low        [number]  null [default: 0.01]

------------------------------------------------------
```

## Pipeline output

The outputs of the pipeline will be stored in the specified `outdir` directory.

### Results structure

```bash
results/
├── aggregate_maes
│   └── results_ave_mae_test_lgb.csv
├── lasso_feature_selection
│   └── best_features_test.csv
├── pipeline_info
│   ├── execution_report.html
│   ├── execution_timeline.html
│   ├── execution_trace.txt
│   └── pipeline_dag.html
├── robustness_feature_selection
│   ├── test_sorted.csv
│   └── test_unsorted.csv
├── select_best_alpha_for_lasso
│   └── test_alpha_mae_df.parquet
└── versions.yml
```