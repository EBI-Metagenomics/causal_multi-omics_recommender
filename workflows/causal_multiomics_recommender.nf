
include { SELECT_BEST_ALPHA_FOR_LASSO  } from '../modules/select_best_alpha_for_lasso'
include { LASSO_FEATURE_SELECTION      } from '../modules/lasso_feature_selection'
include { ROBUSTNESS_FEATURE_SELECTION } from '../modules/robustness_feature_selection'
include { AGGREGATE_MAES               } from '../modules/aggregate_MAEs'

workflow CAUSAL_MULTIOMICS_RECOMMENDER {

    ch_versions = channel.empty()

    features_csv = file("${params.features}", checkIfExists: true)

    SELECT_BEST_ALPHA_FOR_LASSO(
        features_csv,
        params.alpha_low,
        params.alpha_high
    )

    ch_versions = ch_versions.mix( SELECT_BEST_ALPHA_FOR_LASSO.out.versions )

    LASSO_FEATURE_SELECTION(
        SELECT_BEST_ALPHA_FOR_LASSO.out.alpha_mae_parquet,
        features_csv
    )

    ch_versions = ch_versions.mix( LASSO_FEATURE_SELECTION.out.versions )

    ROBUSTNESS_FEATURE_SELECTION(
        LASSO_FEATURE_SELECTION.out.best_features,
        features_csv
    )

    ch_versions = ch_versions.mix( ROBUSTNESS_FEATURE_SELECTION.out.versions )

    AGGREGATE_MAES(
        ROBUSTNESS_FEATURE_SELECTION.out.robustness_feature_selection_unsorted_csv,
        LASSO_FEATURE_SELECTION.out.best_features
    )

    ch_versions = ch_versions.mix( AGGREGATE_MAES.out.versions )

    ch_versions.collectFile(name: "${params.outdir}/versions.yml")
}