#!/bin/bash

nextflow run \
    -profile docker \
    main.nf \
    --indexsheet "${PWD}/tests/example_indexsheet.csv" \
    --bcl_path "${PWD}/tests/example_BCL" \
    --run_name 'example' \
    --out_dir "${PWD}/test_output" \
    -resume  -bg 