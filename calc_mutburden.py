import pandas as pd
import numpy as np
import argparse
import sys
import os

from functions import reader, SNVIndel, Burden, writer

parser = argparse.ArgumentParser()
parser.add_argument("-patient_id", help="patient id label", required=True) 
parser.add_argument("-snv", help="handle for SNV MAF", required=True)
parser.add_argument("-indel", help="handle for InDel MAF", default="NA")
parser.add_argument("-coverage", help="handle for text file that only contains the numeric number of somatic bases covered", required=True)

args = parser.parse_args()

patient = {
	'patient_id': args.patient_id,
	'snv_handle': args.snv,
	'indel_handle': args.indel,
	'coverage_handle': args.coverage
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
    filtered_variants.append(df_indel_noncoding)

df_variants = pd.concat(patient_variants, ignore_index = True)
df_filtered = pd.concat(filtered_variants, ignore_index = True)

if os.path.exists(patient['coverage_handle']):
    patient_burden_series = Burden.run_burden(df_variants, patient)
    burden = Burden.extract_burden(patient_burden_series)

    output_name = '.'.join([patient['patient_id'], 'mutational_burden.txt'])
    writer.export_series(patient_burden_series, output_name)

    output_name = '.'.join([patient['patient_id'], 'mutational_burden.value.txt'])
    writer.export_float(burden, output_name)