process LASSO_FEATURE_SELECTION {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.0dev"

    input:
    path(alpha_mae_csv)
    path(dataset_xy_csv)

    output:
    path("best_features_${params.name}.csv"), emit: best_features
    path("versions.yml"),                     emit: versions

    script:
    """
    lasso_feature_selection.py \\
    --alpha-mae ${alpha_mae_csv} \\
    --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --output best_features_${params.name}.csv
    """
}