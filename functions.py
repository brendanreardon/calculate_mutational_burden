import pandas as pd

class reader(object):
    cols = ['gene_name',
            'build',
            'chromosome',
            'start_position',
            'end_position',
            'reference_allele',
            'tumor_allele1',
            'tumor_allele2',
            'alteration_type',
            'alteration',
            'tumor_sample_barcode',
            'normal_sample_barcode',
            'ref_count',
            'alt_count',
            'total_coverage',
            'tumor_f']

    @staticmethod
    def read(handle, **kwargs):
        df = pd.read_csv(handle, sep = '\t', comment = '#', dtype = 'object', **kwargs)
        return df

    @classmethod
    def standard_read(cls, handle, column_map, **kwargs):
        df = cls.read(handle, usecols = column_map.keys(), **kwargs).rename(columns = column_map)
        return df

class SNVIndel(reader):
    _column_map = {
        'Hugo_Symbol': reader.cols[0],
        'NCBI_Build': reader.cols[1],
        'Chromosome': reader.cols[2],
        'Start_position': reader.cols[3],
        'End_position': reader.cols[4],
        'Reference_Allele': reader.cols[5],
        'Tumor_Seq_Allele1': reader.cols[6],
        'Tumor_Seq_Allele2': reader.cols[7],
        'Variant_Classification': reader.cols[8],
        'Protein_Change': reader.cols[9],
        'Tumor_Sample_Barcode': reader.cols[10],
        'Matched_Norm_Sample_Barcode': reader.cols[11],
        't_ref_count': reader.cols[12],
        't_alt_count': reader.cols[13],
    }

    alt_type_col = reader.cols[8]
    ref_count_col = reader.cols[12]
    alt_count_col = reader.cols[13]
    cov_col = reader.cols[14]
    af_col = reader.cols[15]

    @classmethod
    def append_coverage(cls, df):
        df[cls.cov_col] = df[cls.alt_count_col].astype(int) + df[cls.ref_count_col].astype(int)
        df[cls.af_col] = df[cls.alt_count_col].astype(int) / df[cls.cov_col].astype(int)
        df[cls.af_col] = df[cls.af_col].round(3)
        return df

    @classmethod
    def subset_by_classification(cls, df, classifications):
        df_accept = df[df[cls.alt_type_col].isin(classifications)]
        df_reject = df[~df[cls.alt_type_col].isin(classifications)]
        return df_accept, df_reject

    @classmethod
    def import_muts(cls, handle):
        df = reader.standard_read(handle, cls._column_map)
        variants = cls.append_coverage(df)

        coding_classifications = [
            'Frame_Shift_Del', 'Frame_Shift_Ins', 'In_Frame_Del', 'In_Frame_Ins',
            'Missense_Mutation','Nonsense_Mutation', 'Splice_Site', 'Nonstop_Mutation']

        coding_variants, noncoding_variants = cls.subset_by_classification(variants, coding_classifications)
        return coding_variants, noncoding_variants

class Burden(reader):
    @staticmethod
    def import_burden(handle):
        df = reader.read(handle)
        return df.columns.tolist()[0]

    @staticmethod
    def count_variants(df_list):
        count = 0
        for df in df_list:
            count += df.shape[0]
        return count

    @staticmethod
    def convert_b_Mb(mutations_per_b):
        mutations_per_Mb = float(mutations_per_b) * 10**6
        return round(mutations_per_Mb, 3)

    @classmethod
    def calculate_burden(cls, variants, somatic_bases):
        number_variants = cls.count_variants(variants)
        mutations_per_b = float(number_variants) / float(somatic_bases)
        mutations_per_Mb = cls.convert_b_Mb(mutations_per_b)
        return number_variants, mutations_per_Mb

    @classmethod
    def run_burden(cls, variants, patient):
        somatic_bases = cls.import_burden(patient['coverage_handle'])
        number_variants, burden = cls.calculate_burden(variants, somatic_bases)

        _cols = ['patient_id', 'tumor_sample_barcode', 'normal_sample_barcode',
                 'number_coding_variants', 'somatic_bases_covered', 'coding_mutations_per_Mb']

        df = pd.Series(index = _cols)
        df['patient_id'] = patient['patient_id']
        df['tumor_sample_barcode'] = variants[0]['tumor_sample_barcode'].unique().tolist()[0]
        df['normal_sample_barcode'] = variants[0]['normal_sample_barcode'].unique().tolist()[0]
        df['number_coding_variants'] = number_variants
        df['somatic_bases_covered'] = somatic_bases
        df['coding_mutations_per_Mb'] = burden
        return df

class writer(object):
    @staticmethod
    def export_series(df, output_name):
        df.to_csv(output_name, sep = '\t', index = True)
