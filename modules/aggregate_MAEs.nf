process AGGREGATE_MAES {

    conda "${moduleDir}/environment.yml"
    container "quay.io/microbiome-informatics/causal_multiomics_recommender:1.1dev"

    input:
    path(results_unsorted_lgb_csv)
    path(best_features_csv)

    output:
    path("results_ave_mae_${params.project_name}_lgb.csv"), emit: results_ave_mae_lgb
    path("versions.yml"),                                   emit: versions

    script:
    """
    aggregate_MAEs.py \\
    --results-unsorted-lgb ${results_unsorted_lgb_csv} \\
    --best-features ${best_features_csv} \\
    --output results_ave_mae_${params.project_name}_lgb.csv

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version 2>&1 | sed 's/Python //g')
        numpy: \$(python -c "import numpy; print(numpy.__version__)")
        pandas: \$(python -c "import pandas; print(pandas.__version__)")
    END_VERSIONS
    """
}