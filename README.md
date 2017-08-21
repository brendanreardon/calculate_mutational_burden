# calculate_mutational_burden
A lightweight python script to calculate coding mutational burden. 

## Using calculate_mutational_burden
Please edit wrapper.sh to include the following details for your given sample
- patient_id: An individual ID for the sample being considered
- snv_handle: Path to a MAF file containing single nucleotide variants
- indel_handle: Path to a MAF file containing insertion or deletion variants
- coverage_handle: Path to text file containing only the number of somatic bases covered

Given MAF files should follow the [specifications detailed by the NCI](https://wiki.nci.nih.gov/display/TCGA/Mutation+Annotation+Format+(MAF)+Specification). The following variant classifications considered to be coding, and thus are used in the calculation of mutational burden: 
- Missense_Mutation
- Nonsense_Mutation
- Splice_Site
- Nonstop_Mutation
- Frame_Shift_Del
- Frame_Shift_Ins
- In_Frame_Del
- In_Frame_Ins
