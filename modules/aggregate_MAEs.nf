process AGGREGATE_MAES {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.0dev"

    input:
    path(results_unsorted_lgb_csv)
    path(best_features_csv)

    output:
    path("results_ave_mae_${params.name}_lgb.csv"), emit: results_ave_mae_lgb
    path("versions.yml"),                           emit: versions

    script:
    """
    lasso_feature_selection.py \\
    --results-unsorted-lgb ${results_unsorted_lgb_csv} \\
    --best-features ${best_features_csv} \\
    --output results_ave_mae_${params.name}_lgb.csv
    """
}