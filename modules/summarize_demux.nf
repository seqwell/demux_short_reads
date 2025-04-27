process SUMMARIZE_DEMUX { 
  
   publishDir path: "${params.out_dir}/${params.run_name}/", mode: 'copy'
  
   
   input:
    path(reports) 

   output:
    path("*.xlsx")

  """
  demux_bclconvert_report.py ${params.run_name}
  """
}