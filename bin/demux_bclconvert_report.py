#!/usr/bin/env python3

import os
import sys
import pandas as pd

def generate_excel_report(reports_dir, output_path):
    # Define important CSVs
    important_csvs = [
        "Demultiplex_Stats.csv",
        "Top_Unknown_Barcodes.csv",
        "Quality_Metrics.csv",
        "Index_Hopping_Counts.csv"
    ]

    # Use xlsxwriter explicitly
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for csv_file in important_csvs:
            file_path = os.path.join(reports_dir, csv_file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                sheet_name = os.path.splitext(csv_file)[0][:31]  # Excel sheet name limit
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                print(f"Warning: {csv_file} not found in {reports_dir}", file=sys.stderr)



reports_folder = "Reports"
output_excel_file = sys.argv[1] + '.xlsx'
generate_excel_report(reports_folder, output_excel_file)

