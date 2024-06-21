process SELECT_BEST_ALPHA_FOR_LASSO {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.0dev"

    input:
    path(dataset_xy_csv)
    val(alpha_low)
    val(alpha_high)

    output:
    path("${params.name}_alpha_mae_df.csv"), emit: alpha_mae_df
    path("versions.yml"),                    emit: versions

    script:
    """
    select_best_alpha_for_lasso.py --xy ${dataset_xy_csv} \\
    --phenotype-col ${params.phenotype_column} \\
    --apha-low ${alpha_low} \\
    --alha-high ${alpha_high} \\
    --output ${params.name}_alpha_mae_df.csv
    """
}