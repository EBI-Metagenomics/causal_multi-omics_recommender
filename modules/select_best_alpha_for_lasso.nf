process SELECT_BEST_ALPHA_FOR_LASSO {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.1dev"

    input:
    path(dataset_xy_csv)
    val(alpha_low)
    val(alpha_high)

    output:
    path("${params.project_name}_alpha_mae_df.parquet"), emit: alpha_mae_parquet
    path("versions.yml"),                                emit: versions

    script:
    """
    select_best_alpha_for_lasso.py --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --alpha-low ${alpha_low} \\
    --alpha-high ${alpha_high} \\
    --output ${params.project_name}_alpha_mae_df.parquet

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version 2>&1 | sed 's/Python //g')
        numpy: \$(python -c "import numpy; print(numpy.__version__)")
        pandas: \$(python -c "import pandas; print(pandas.__version__)")
        scikit-learn: \$(python -c "import sklearn; print(sklearn.__version__)")
    END_VERSIONS
    """
}