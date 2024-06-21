process ROBUSTNESS_FEATURE_SELECTION {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.0dev"

    input:
    path(best_features_csv)
    path(dataset_xy_csv)

    output:
    path("${params.name}_sorted.csv"),   emit: robustness_feature_selection_sorted_csv
    path("${params.name}_unsorted.csv"), emit: robustness_feature_selection_unsorted_csv
    path("versions.yml"),                             emit: versions

    script:
    """
    robustness_feature_selection.py \\
    --best_features ${best_features_csv} \\
    --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --output ${params.name}
    """
}