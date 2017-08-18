import pandas as pd
import numpy as np
import sys
import os


from functions import reader, SNVIndel, Burden, writer

patient = {
	'patient_id': sys.argv[1],
	'snv_handle': sys.argv[2],
	'indel_handle': sys.argv[3],
	'coverage_handle': sys.argv[4]
}

patient_variants = []
filtered_variants = []

if os.path.exists(patient['snv_handle']):
    df_snv, df_snv_noncoding = SNVIndel.import_muts(patient['snv_handle'])

    patient_variants.append(df_snv)
    filtered_variants.append(df_snv_noncoding)

if os.path.exists(patient['indel_handle']):
    df_indel, df_indel_noncoding = SNVIndel.import_muts(patient['indel_handle'])

    patient_variants.append(df_indel)
    patient_variants.append(df_indel_noncoding)

if os.path.exists(patient['coverage_handle']):
    patient_burden = Burden.run_burden(patient_variants, patient)

    output_name = patient['patient_id'] + '.mutational_burden.txt'
    writer.export_series(patient_burden, output_name)
