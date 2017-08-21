#!/bin/bash

patient_id="HCC1143"
snv_handle="test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.oxoG3.maf.annotated"
indel_handle="test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.indel.capture.maf.annotated"
coverage_handle="test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.somatic_mutation_covered_bases_capture.txt"

python calc_mutburden.py -patient_id $patient_id -snv $snv_handle -indel $indel_handle -coverage $coverage_handle
