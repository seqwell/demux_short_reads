process SUMMARIZE_DEMUX { 
  
   
   input:
    path(reports) 

   output:
    path("*.xlsx")

  """
  demux_bclconvert_report.py ${params.run_name}
  """
}