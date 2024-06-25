process LASSO_FEATURE_SELECTION {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.2dev"

    input:
    path(alpha_mae_parquet)
    path(dataset_xy_csv)

    output:
    path("best_features_${params.project_name}.csv"), emit: best_features
    path("versions.yml"),                             emit: versions

    script:
    """
    lasso_feature_selection.py \\
    --alpha-mae ${alpha_mae_parquet} \\
    --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --output best_features_${params.project_name}.csv

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version 2>&1 | sed 's/Python //g')
        numpy: \$(python -c "import numpy; print(numpy.__version__)")
        pandas: \$(python -c "import pandas; print(pandas.__version__)")
        scikit-learn: \$(python -c "import sklearn; print(sklearn.__version__)")
    END_VERSIONS
    """
}