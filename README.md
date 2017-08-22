# calculate_mutational_burden
A lightweight python script to calculate coding mutational burden. 

## Run calculate_mutational_burden
calc_mutburden.py can be run by either editing the wrapper.sh or directly from python. Please edit wrapper.sh or run to include the following details for your given sample
- `patient_id`: An individual ID for the sample being considered
- `snv_handle`: Path to a MAF file containing single nucleotide variants
- `indel_handle`: Path to a MAF file containing insertion or deletion variants
- `coverage_handle`: Path to text file containing only the number of somatic bases covered

Example:
`python calc_mutburden.py -patient_id HCC1143 -snv test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.oxoG3.maf.annotated -indel test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.indel.capture.maf.annotated -coverage test_data/HCC1143_TP_NT_HCC1143T_HCC1143N.somatic_mutation_covered_bases_capture.txt`

Given MAF files should follow the [specifications detailed by the NCI](https://wiki.nci.nih.gov/display/TCGA/Mutation+Annotation+Format+(MAF)+Specification). The following variant classifications considered to be coding, and thus are used in the calculation of mutational burden: 
- Missense_Mutation
- Nonsense_Mutation
- Splice_Site
- Nonstop_Mutation
- Frame_Shift_Del
- Frame_Shift_Ins
- In_Frame_Del
- In_Frame_Ins
