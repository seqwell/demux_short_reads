process SAMPLESHEET {

    stageInMode 'copy'
    

    publishDir path: "${params.out_dir}", mode: 'copy'

    input:
      path(indexsheet) 

    output:
      path("*_samplesheet.csv"),  emit: samplesheet_ch

    

    """
    make_samplesheet.py $indexsheet
    """

}
