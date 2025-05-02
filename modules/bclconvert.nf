process BCLCONVERT {
  
     publishDir path: "${params.out_dir}/${params.run_name}/", mode: 'copy'

     input:
      path(bcl) 
      path(samplesheet) 

     output:
      path("*")
      path("Reports"),  emit: reports 

     """
     bcl-convert \
        --bcl-input-directory $bcl \
        --output-directory . \
        --force \
        --sample-sheet ${samplesheet} 
   
     ## organize fastq files
     ls *.fastq.gz | grep -v Undetermined > fq_list.txt

    while read fq; do
        fname=\$(basename "\$fq" .fastq.gz)

        # Match prefix before the well ID
        if [[ "\$fname" =~ ^([A-Za-z0-9_-]+)_[A-H][0-9]{2}_ ]]; then
            prefix="\${BASH_REMATCH[1]}"
            outdir="\${prefix}_FASTQ"
            mkdir -p "\$outdir"
            
            # Remove _S##_L001 from the name
            newname=\$(echo "\$fname" | sed -E 's/_S[0-9]{1,}_L001//')
            mv "\$fq" "\$outdir/\${newname}.fastq.gz"
        else
            echo "Skipping file (no match): \$fname"
        fi
    done < fq_list.txt

    rm fq_list.txt
     
     """
}
