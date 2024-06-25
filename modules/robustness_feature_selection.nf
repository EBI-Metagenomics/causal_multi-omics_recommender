process ROBUSTNESS_FEATURE_SELECTION {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.1dev"

    input:
    path(best_features_csv)
    path(dataset_xy_csv)

    output:
    path("${params.project_name}_sorted.csv"),   emit: robustness_feature_selection_sorted_csv
    path("${params.project_name}_unsorted.csv"), emit: robustness_feature_selection_unsorted_csv
    path("versions.yml"),                        emit: versions

    script:
    """
    robustness_feature_selection.py \\
    --best-features ${best_features_csv} \\
    --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --output-name ${params.project_name}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version 2>&1 | sed 's/Python //g')
        numpy: \$(python -c "import numpy; print(numpy.__version__)")
        pandas: \$(python -c "import pandas; print(pandas.__version__)")
        scikit-learn: \$(python -c "import sklearn; print(sklearn.__version__)")
    END_VERSIONS
    """
}