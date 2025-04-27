#!/usr/bin/env nextflow

include { validateParameters; paramsSummaryLog } from 'plugin/nf-schema'


include { BCLCONVERT } from './modules/bclconvert.nf'
include { SAMPLESHEET } from './modules/samplesheet.nf'
include { SUMMARIZE_DEMUX } from './modules/summarize_demux.nf'




workflow {
  
    validateParameters(input: params.indexsheet, 
                       schema: 'schemas/input_schema.json')
                       
    log.info paramsSummaryLog(workflow)
  
    bcl_ch = file(params.bcl_path)
    
    indexsheet_ch = Channel.fromPath(params.indexsheet)
    
    samplesheet_ch = SAMPLESHEET(indexsheet_ch)
    
    demux_ch = BCLCONVERT( bcl_ch, samplesheet_ch.samplesheet_ch )
    
    SUMMARIZE_DEMUX( demux_ch.reports)
    
    
    // Pipeline Cleanup ////////////////////////////////////////////////////////////////////////////

    workflow.onComplete = {
        println "Project output directory: ${workflow.projectDir}/${params.out_dir}"
        println "Pipeline completed at: $workflow.complete"
        println "Pipeline completed time duration: $workflow.duration"
        println "Command line: $workflow.commandLine"
        println "Execution status: ${ workflow.success ? 'OK' : 'failed' }"
    }

    workflow.onError = {
        println "Error: Pipeline execution stopped with the following message: ${workflow.errorMessage}"
    }
  
}
