#!/usr/bin/env nextflow
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    polavieja_lab/causal_multi-omics_recommender
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Github : https://gitlab.com/polavieja_lab/causal_multi-omics_recommender
----------------------------------------------------------------------------------------
*/

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    VALIDATE & PRINT PARAMETER SUMMARY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { validateParameters; paramsHelp; paramsSummaryLog; samplesheetToList } from 'plugin/nf-schema'

// Print help message, supply typical command line usage for the pipeline
if (params.help) {
    // TODO: use the github/gitlab organization to pull the pipeline
    log.info paramsHelp("nextflow run https://gitlab.com/polavieja_lab/causal_multi-omics_recommender --features input_file.csv --phenotype_column phenotype")
    exit 0
}

// Validate input parameters
validateParameters()

// Print summary of supplied parameters
log.info paramsSummaryLog(workflow)

include { CAUSAL_MULTIOMICS_RECOMMENDER } from './workflows/causal_multiomics_recommender'

//
// WORKFLOW: Run main ebi-metagenomics/mettannotator analysis pipeline
//
workflow POLAVIEJA_LAB_CAUSAL_MULTIOMICS_RECOMMENDER {
    CAUSAL_MULTIOMICS_RECOMMENDER ()
}
