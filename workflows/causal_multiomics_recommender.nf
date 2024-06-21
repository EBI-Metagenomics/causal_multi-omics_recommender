
include { SELECT_BEST_ALPHA_FOR_LASSO  } from '../modules/select_best_alpha_for_lasso'
include { LASSO_FEATURE_SELECTION      } from '../modules/lasso_feature_selection'
include { ROBUSTNESS_FEATURE_SELECTION } from '../modules/robustness_feature_selection'
include { AGGREGATE_MAES               } from '../modules/aggregate_MAEs'

workflow CAUSAL_MULTIOMICS_RECOMMENDER {

    features_csv = file("${params.features}", checkIfExists: true)

    SELECT_BEST_ALPHA_FOR_LASSO(
        features_csv,
        params.alpha_low,
        params.alpha_high
    )

    LASSO_FEATURE_SELECTION(
        SELECT_BEST_ALPHA_FOR_LASSO.out.alpha_mae_df,
        features_csv
    )

    ROBUSTNESS_FEATURE_SELECTION(
        LASSO_FEATURE_SELECTION.out.best_features,
        features_csv
    )

    AGGREGATE_MAES(
        ROBUSTNESS_FEATURE_SELECTION.out.robustness_feature_selection_unsorted_csv,LASSO_FEATURE_SELECTION.out.best_features
    )

}