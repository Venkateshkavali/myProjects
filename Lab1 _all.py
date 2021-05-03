#!/usr/bin/env python
# coding: utf-8

# Before you turn this problem in, make sure everything runs as expected. First, **restart the kernel** (in the menubar, select Kernel$\rightarrow$Restart) and then **run all cells** (in the menubar, select Cell$\rightarrow$Run All).
# 
# Make sure you fill in any place that says `YOUR CODE HERE` or "YOUR ANSWER HERE", as well as your name and collaborators below:

# In[ ]:


NAME = ""
COLLABORATORS = ""


# ---

# # Introduction 
# This is the first of three labs that you will do in this course.  In this lab, you will parse a variant call format file (https://en.wikipedia.org/wiki/Variant_Call_Format). This file has one thousand variants in it. Each line after the header lines is a variant. Open the variant file and inspect its contents. You will parse each line and transform it into a JSON. The output will look something like this (I have truncated the output):
# ```
# {
#         "ALT": "G",
#         "CHROM": "4",
#         "FILTER": "PASS",
#         "ID": ".",
#         "INFO": {
#            
#             "Gene.ensGene": "ENSG00000109471,ENSG00000138684",
#             "Gene.refGene": "IL2,IL21",
#             "GeneDetail.ensGene": "dist=38306,dist=117597",
#             "GeneDetail.refGene": "dist=38536,dist=117597"
#         },
#         "POS": 123416186,
#         "QUAL" :23.25,
#         "REF": "A",
#         "SAMPLE": {
#             "XG102": {
#                 "AD": "51,8",
#                 "DP": "59",
#                 "GQ": "32",
#                 "GT": "0/1",
#                 "PL": "32,0,1388"
#             }
#     }
# ```
# The lab will guide you through writing small functions that will be used to generate the JSON above. Note that the method outlined in this lab is not necessarily optimal. It is just one way of parsing the file and teaching you how to break a large problem into small parts. 
# 
# Note that the header which corresponds to the columns starts with one hash/pound (#) symbol. Skip all headers that start with two hashes/pounds (##).

# # Part 1 (5 points)
# Write a function that determines the data type of its input string. The data types can be a float, int, or string. 

# In[125]:


def determine_data_type(value):
    """
    The function takes a string input and determines its data type to be either a float, int, or string. 
    """
    # YOUR CODE HERE
    from ast import literal_eval
    try:
        return type(literal_eval(value))
    except (ValueError, SyntaxError):
        # A string, so return str
        return str
    raise NotImplementedError()


# In[126]:


assert determine_data_type('1.2') == float
assert determine_data_type('4') == int
assert determine_data_type('EAS503') == str


# # Part 2 (5 points)
# Write a function whose input is a list of strings.  This function determines the correct data type of all the elements in the list. For example, ['1', '2', '3'] is int, ['1.1', '2.2', '3.3'] is float, ['1.1', '2', '3.3'] is also float, and ['1.1', '234String', '3.3'] is str. The purpose of this function to figure out what to cast an array of strings to. Some lists might be all ints, in which case the data type is int. Some might be a mixure of ints and floats, in which case the data type will be float. Some lists might be a mixture of ints, floats, and strings, in which case the data type of the list will be string. 

# In[127]:


def determine_data_type_of_list(values):
    """
    Function takes a list of strings and determines their data type. 

    """
    # YOUR CODE HERE
    from ast import literal_eval
    my_list=[]
    for element in values:
        try:
             my_list.append(type(literal_eval(element)))
        except (ValueError, SyntaxError):
            my_list.append(str)
    #print(my_list)
    #element = element.strip('\'')
    if str in my_list :
        return str
    elif float in my_list:
        return float
    elif int in my_list:
        return int
    raise NotImplementedError()


# In[128]:


assert determine_data_type_of_list(['1', '2', '3']) == int
assert determine_data_type_of_list(['1.1', '2.2', '3.3']) == float
assert determine_data_type_of_list(['1.1', '2', '3.3']) == float
assert determine_data_type_of_list(['1.1', '234String', '3.3']) == str


# # Part 3 (10 points)
# 
# Write a function whose inputs a format field and a sample field. The format field looks like format_field = 'GT:AD:DP:GQ:PGT:PID:PL' and the sample field looks like
# ```
# sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
#              'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
#              'XG104': '0/1:34,38:72:99:.:.:938,0,796',
#              'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
#              'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
#              'XG204': '0/1:34,38:72:99:.:.:938,0,796',
#              'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
#              'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
#              'XG304': '0/1:34,38:72:99:.:.:938,0,796',
#              'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
#              'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
#              'XG404': '0/1:34,38:72:99:.:.:938,0,796'}
# ```
# Transform the inputs such that the output looks like this:
# 
# ```
# output = {'XG102': {'AD': '0,76',
#            'DP': '76',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '1|1',
#            'PID': '48306945_C_G',
#            'PL': '3353,229,0'},
#  'XG103': {'AD': '0,52',
#            'DP': '52',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '1517,156,0'},
#  'XG104': {'AD': '34,38',
#            'DP': '72',
#            'GQ': '99',
#            'GT': '0/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '938,0,796'},
#  'XG202': {'AD': '0,76',
#            'DP': '76',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '1|1',
#            'PID': '48306945_C_G',
#            'PL': '3353,229,0'},
#  'XG203': {'AD': '0,52',
#            'DP': '52',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '1517,156,0'},
#  'XG204': {'AD': '34,38',
#            'DP': '72',
#            'GQ': '99',
#            'GT': '0/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '938,0,796'},
#  'XG302': {'AD': '0,76',
#            'DP': '76',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '1|1',
#            'PID': '48306945_C_G',
#            'PL': '3353,229,0'},
#  'XG303': {'AD': '0,52',
#            'DP': '52',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '1517,156,0'},
#  'XG304': {'AD': '34,38',
#            'DP': '72',
#            'GQ': '99',
#            'GT': '0/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '938,0,796'},
#  'XG402': {'AD': '0,76',
#            'DP': '76',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '1|1',
#            'PID': '48306945_C_G',
#            'PL': '3353,229,0'},
#  'XG403': {'AD': '0,52',
#            'DP': '52',
#            'GQ': '99',
#            'GT': '1/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '1517,156,0'},
#  'XG404': {'AD': '34,38',
#            'DP': '72',
#            'GQ': '99',
#            'GT': '0/1',
#            'PGT': '.',
#            'PID': '.',
#            'PL': '938,0,796'}}
# ```

# In[129]:


format_field = "GT:AD:DP:GQ:PGT:PID:PL"
sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG104': '0/1:34,38:72:99:.:.:938,0,796',
             'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG204': '0/1:34,38:72:99:.:.:938,0,796',
             'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG304': '0/1:34,38:72:99:.:.:938,0,796',
             'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG404': '0/1:34,38:72:99:.:.:938,0,796'}


def format_sample_fields(format_field, sample_field):
    """
    Format the sample fields given the description above. Data is already provided.
    """
    
    # YOUR CODE HERE
    import re
    f1= re.split('[:]',format_field)
    dict1 = dict()
    dict3 = {}
    #dict1_sorted = dict()
    dict2 = sample_field
    #dict2.clear()
    for k,v in sample_field.items():
        dict1.clear();
        v1=re.split('[:]',v)
        #print("v1 is ",v1)
        j=0
        for n in f1:
            dict4 = {}
            dict1[n]=v1[j]
            j+=1
            for key in sorted(dict1.keys()):
                dict4[key] = dict1[key]
        #print("dict1 is ",dict1)
        dict2[k]=dict(dict4)
        #print("dict2 is ",dict2)
        
    for key in sorted(dict2.keys()):
        dict3[key] = dict2[key]
    return dict3
    raise NotImplementedError()


# In[130]:


solution = {'XG102': {'AD': '0,76',
           'DP': '76',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '1|1',
           'PID': '48306945_C_G',
           'PL': '3353,229,0'},
 'XG103': {'AD': '0,52',
           'DP': '52',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '.',
           'PID': '.',
           'PL': '1517,156,0'},
 'XG104': {'AD': '34,38',
           'DP': '72',
           'GQ': '99',
           'GT': '0/1',
           'PGT': '.',
           'PID': '.',
           'PL': '938,0,796'},
 'XG202': {'AD': '0,76',
           'DP': '76',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '1|1',
           'PID': '48306945_C_G',
           'PL': '3353,229,0'},
 'XG203': {'AD': '0,52',
           'DP': '52',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '.',
           'PID': '.',
           'PL': '1517,156,0'},
 'XG204': {'AD': '34,38',
           'DP': '72',
           'GQ': '99',
           'GT': '0/1',
           'PGT': '.',
           'PID': '.',
           'PL': '938,0,796'},
 'XG302': {'AD': '0,76',
           'DP': '76',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '1|1',
           'PID': '48306945_C_G',
           'PL': '3353,229,0'},
 'XG303': {'AD': '0,52',
           'DP': '52',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '.',
           'PID': '.',
           'PL': '1517,156,0'},
 'XG304': {'AD': '34,38',
           'DP': '72',
           'GQ': '99',
           'GT': '0/1',
           'PGT': '.',
           'PID': '.',
           'PL': '938,0,796'},
 'XG402': {'AD': '0,76',
           'DP': '76',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '1|1',
           'PID': '48306945_C_G',
           'PL': '3353,229,0'},
 'XG403': {'AD': '0,52',
           'DP': '52',
           'GQ': '99',
           'GT': '1/1',
           'PGT': '.',
           'PID': '.',
           'PL': '1517,156,0'},
 'XG404': {'AD': '34,38',
           'DP': '72',
           'GQ': '99',
           'GT': '0/1',
           'PGT': '.',
           'PID': '.',
           'PL': '938,0,796'}}

format_field = "GT:AD:DP:GQ:PGT:PID:PL"
sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG104': '0/1:34,38:72:99:.:.:938,0,796',
             'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG204': '0/1:34,38:72:99:.:.:938,0,796',
             'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG304': '0/1:34,38:72:99:.:.:938,0,796',
             'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG404': '0/1:34,38:72:99:.:.:938,0,796'}

format_output = format_sample_fields(format_field, sample_field)

assert format_output['XG102'] == solution ['XG102']
assert format_output['XG302'] == solution ['XG302']
assert format_output['XG404'] == solution ['XG404']


# # Part 4 (10 points) 
# Write a function whose inputs are a list containing the vcf header and a variant line.  The function should return a dictionary using the header as keys and the variant line as values. The function should use the `format_sample_fields` you wrote previously to format the sample fields. The output of the first line looks like this:
# 
# ```
# {'ALT': 'G',
#  'CHROM': '4',
#  'FILTER': 'PASS',
#  'ID': '.',
#  'INFO': 'AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2\\x3bIL21;GeneDetail.refGene=dist\\x3d38536\\x3bdist\\x3d117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471\\x3bENSG00000138684;GeneDetail.ensGene=dist\\x3d38306\\x3bdist\\x3d117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END',
#  'POS': '123416186',
#  'QUAL': '23.25',
#  'REF': 'A',
#  'SAMPLE': {'XG102': {'AD': '51,8',
#             'DP': '59',
#             'GQ': '32',
#             'GT': '0/1',
#             'PL': '32,0,1388'},
#        'XG103': {'AD': '47,0',
#             'DP': '47',
#             'GQ': '99',
#             'GT': '0/0',
#             'PL': '0,114,1353'},
#        'XG104': {'AD': '74,0',
#             'DP': '74',
#             'GQ': '51',
#             'GT': '0/0',
#             'PL': '0,51,1827'},
#        'XG202': {'AD': '51,8',
#             'DP': '59',
#             'GQ': '32',
#             'GT': '0/1',
#             'PL': '32,0,1388'},
#        'XG203': {'AD': '47,0',
#             'DP': '47',
#             'GQ': '99',
#             'GT': '0/0',
#             'PL': '0,114,1353'},
#        'XG204': {'AD': '74,0',
#             'DP': '74',
#             'GQ': '51',
#             'GT': '0/0',
#             'PL': '0,51,1827'},
#        'XG302': {'AD': '51,8',
#             'DP': '59',
#             'GQ': '32',
#             'GT': '0/1',
#             'PL': '32,0,1388'},
#        'XG303': {'AD': '47,0',
#             'DP': '47',
#             'GQ': '99',
#             'GT': '0/0',
#             'PL': '0,114,1353'},
#        'XG304': {'AD': '74,0',
#             'DP': '74',
#             'GQ': '51',
#             'GT': '0/0',
#             'PL': '0,51,1827'},
#        'XG402': {'AD': '51,8',
#             'DP': '59',
#             'GQ': '32',
#             'GT': '0/1',
#             'PL': '32,0,1388'},
#        'XG403': {'AD': '47,0',
#             'DP': '47',
#             'GQ': '99',
#             'GT': '0/0',
#             'PL': '0,114,1353'},
#        'XG404': {'AD': '74,0',
#             'DP': '74',
#             'GQ': '51',
#             'GT': '0/0',
#             'PL': '0,51,1827'}}}
#             
# ```
# 
# 

# In[131]:


header = "CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	XG102	XG103	XG104	XG202	XG203	XG204	XG302	XG303	XG304	XG402	XG403	XG404".split('\t')
line = """4	123416186	.	A	G	23.25	PASS	AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2\x3bIL21;GeneDetail.refGene=dist\x3d38536\x3bdist\x3d117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471\x3bENSG00000138684;GeneDetail.ensGene=dist\x3d38306\x3bdist\x3d117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END	GT:AD:DP:GQ:PL	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827"""

def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 
    """
    # YOUR CODE HERE
    header_split = []
    line_dict = {}
    sample_field = {}
    format_dict = {1:1,2:2,3:3}
    format_data = []
    format_field = ''
    flag = False
    
    line_list = line.split()
    
    for ele_header in header:
        if flag == False:
            if ele_header.upper() == "FORMAT":
                ele_header = "SAMPLE"
                flag = True
            header_split.append(ele_header)
        else:
            format_data.append(ele_header)
            
    for i in range(len(format_data)):
        sample_field[format_data[i]] = line_list[len(header_split)+i]
        
    format_field = line_list[len(header_split)-1]
    
    format_dict = format_sample_fields(format_field, sample_field)
    
    for i in range(len(header_split)):
        if header_split[i] == "SAMPLE":
            line_dict[header_split[i]] = {}
            line_dict[header_split[i]] = format_dict
        else:
            line_dict[header_split[i]] = line_list[i]
            
    return line_dict
    
    raise NotImplementedError()


# In[132]:


solution = {'INFO': 'AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2;IL21;GeneDetail.refGene=dist=38536;dist=117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471;ENSG00000138684;GeneDetail.ensGene=dist=38306;dist=117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END', 'SAMPLE': {'XG404': {'GT': '0/0', 'GQ': '51', 'AD': '74,0', 'DP': '74', 'PL': '0,51,1827'}, 'XG402': {'GT': '0/1', 'GQ': '32', 'AD': '51,8', 'DP': '59', 'PL': '32,0,1388'}, 'XG403': {'GT': '0/0', 'GQ': '99', 'AD': '47,0', 'DP': '47', 'PL': '0,114,1353'}, 'XG303': {'GT': '0/0', 'GQ': '99', 'AD': '47,0', 'DP': '47', 'PL': '0,114,1353'}, 'XG302': {'GT': '0/1', 'GQ': '32', 'AD': '51,8', 'DP': '59', 'PL': '32,0,1388'}, 'XG304': {'GT': '0/0', 'GQ': '51', 'AD': '74,0', 'DP': '74', 'PL': '0,51,1827'}, 'XG202': {'GT': '0/1', 'GQ': '32', 'AD': '51,8', 'DP': '59', 'PL': '32,0,1388'}, 'XG203': {'GT': '0/0', 'GQ': '99', 'AD': '47,0', 'DP': '47', 'PL': '0,114,1353'}, 'XG204': {'GT': '0/0', 'GQ': '51', 'AD': '74,0', 'DP': '74', 'PL': '0,51,1827'}, 'XG103': {'GT': '0/0', 'GQ': '99', 'AD': '47,0', 'DP': '47', 'PL': '0,114,1353'}, 'XG102': {'GT': '0/1', 'GQ': '32', 'AD': '51,8', 'DP': '59', 'PL': '32,0,1388'}, 'XG104': {'GT': '0/0', 'GQ': '51', 'AD': '74,0', 'DP': '74', 'PL': '0,51,1827'}}, 'CHROM': '4', 'POS': '123416186', 'FILTER': 'PASS', 'QUAL': '23.25', 'ALT': 'G', 'REF': 'A', 'ID': '.'}
header = "CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	XG102	XG103	XG104	XG202	XG203	XG204	XG302	XG303	XG304	XG402	XG403	XG404".split('\t')
line = """4	123416186	.	A	G	23.25	PASS	AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2\x3bIL21;GeneDetail.refGene=dist\x3d38536\x3bdist\x3d117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471\x3bENSG00000138684;GeneDetail.ensGene=dist\x3d38306\x3bdist\x3d117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END	GT:AD:DP:GQ:PL	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827	0/1:51,8:59:32:32,0,1388	0/0:47,0:47:99:0,114,1353	0/0:74,0:74:51:0,51,1827"""


assert create_dict_from_line(header, line) == solution


# # Part 5 (10 points)
# Write a function whose input is a filename for a vcf. The function reads the vcf file one variant at a time and transforms it into a dictionary using the create_dict_from_line function. It returns a list containing all the variant dictionaries. NOTE: The file used for the automated test only has one line. Your function should be able to handle multiple lines.

# In[133]:


def read_vcf_file(filename):
    
    # YOUR CODE HERE
    header = {}
    line = {}
    res1 = {}
    list1=[]
    f = open(filename, "r")
    f2 = f.readline()
    
    header = f2.split()
    header[0]='CHROM'
    #print(header)
    f3 = f.readline()
   
    line = f3
    res = create_dict_from_line(header, line)
    for key in sorted(res.keys()):
        res1[key] = res[key]
    list1.append(res1)
    return list1
    raise NotImplementedError()


# In[134]:


expected_output = [{'ALT': 'G',
  'CHROM': '4',
  'FILTER': 'PASS',
  'ID': '.',
  'INFO': 'AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2\\x3bIL21;GeneDetail.refGene=dist\\x3d38536\\x3bdist\\x3d117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471\\x3bENSG00000138684;GeneDetail.ensGene=dist\\x3d38306\\x3bdist\\x3d117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END',
  'POS': '123416186',
  'QUAL': '23.25',
  'REF': 'A',
  'SAMPLE': {'XG102': {'AD': '51,8',
                       'DP': '59',
                       'GQ': '32',
                       'GT': '0/1',
                       'PL': '32,0,1388'},
             'XG103': {'AD': '47,0',
                       'DP': '47',
                       'GQ': '99',
                       'GT': '0/0',
                       'PL': '0,114,1353'},
             'XG104': {'AD': '74,0',
                       'DP': '74',
                       'GQ': '51',
                       'GT': '0/0',
                       'PL': '0,51,1827'},
             'XG202': {'AD': '51,8',
                       'DP': '59',
                       'GQ': '32',
                       'GT': '0/1',
                       'PL': '32,0,1388'},
             'XG203': {'AD': '47,0',
                       'DP': '47',
                       'GQ': '99',
                       'GT': '0/0',
                       'PL': '0,114,1353'},
             'XG204': {'AD': '74,0',
                       'DP': '74',
                       'GQ': '51',
                       'GT': '0/0',
                       'PL': '0,51,1827'},
             'XG302': {'AD': '51,8',
                       'DP': '59',
                       'GQ': '32',
                       'GT': '0/1',
                       'PL': '32,0,1388'},
             'XG303': {'AD': '47,0',
                       'DP': '47',
                       'GQ': '99',
                       'GT': '0/0',
                       'PL': '0,114,1353'},
             'XG304': {'AD': '74,0',
                       'DP': '74',
                       'GQ': '51',
                       'GT': '0/0',
                       'PL': '0,51,1827'},
             'XG402': {'AD': '51,8',
                       'DP': '59',
                       'GQ': '32',
                       'GT': '0/1',
                       'PL': '32,0,1388'},
             'XG403': {'AD': '47,0',
                       'DP': '47',
                       'GQ': '99',
                       'GT': '0/0',
                       'PL': '0,114,1353'},
             'XG404': {'AD': '74,0',
                       'DP': '74',
                       'GQ': '51',
                       'GT': '0/0',
                       'PL': '0,51,1827'}}}]

result = read_vcf_file('single_variant.vcf')
assert expected_output == result


# # Part 6 (5 points)
# Write a function that extracts the info field from the data dictionary that was created in the previous part. The function should return all the info field dictionaries as list. 
# 

# In[137]:


def extract_info_field(data):
    """
    See description in part 6
    """
    # YOUR CODE HERE
    f1=[]
    
    for i in range(len(data)):
        for k,v in data[i].items():
            if k.upper() == "INFO":
                f1.append(v)
    
    return f1
    
    raise NotImplementedError()


# In[138]:


expected_results = open('info_field.vcf', 'r').readline().strip()
info_field = extract_info_field(result)

assert expected_results == info_field[0]


# # Part 7 (10 points)
# You now need to figure out that data types for each of the info fields. 
# Begin by writing a function that first takes the info fields and turns them into a dictionary. Make sure to skip any fields that do not have a value or are missing a value. Also replace \\x3b with a comma and \\x3d with an equal sign.  

# In[139]:


def create_dictionary_of_info_field_values(data):
    """
    See description of part 7
    """
    # YOUR CODE HERE
    dict1 = {}
    f1 = []
    list1 = []
    for i in data:
        i = i.replace("\\x3b",",")
        i = i.replace("\\x3d","=")
        f1 = i.split(";")    
        for info in f1:
            key1 = ''
            value1 = ''
            flag = False
            key_flag = False
            for char in info:
                if char == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key1 += char
                else:
                    value1 += char
            if value1 != '':
                if len(list1) == 0:
                    dict1 = {}
                    dict1[key1] = []
                    if value1 != '.':
                        dict1[key1].append(value1)
                else:
                    for j in list1:
                        if j == key1:
                            if value1 != '.':
                                dict1[key1].append(value1)
                            key_flag = True
                            break
                            
                if key_flag == False:
                    dict1[key1] = []
                    if value1 != '.':
                        dict1[key1].append(value1)
                    
                list1.append(key1)
                #print(info_field_dict)
    return dict1
    raise NotImplementedError()


# In[140]:



info_field = extract_info_field(result)
expected_results = {'AC': ['1'], 'AF': ['0.167'], 'AN': ['6'], 'BaseQRankSum': ['-2.542'], 'ClippingRankSum': ['0'], 'DP': ['180'], 'ExcessHet': ['3.0103'], 'FS': ['0'], 'MLEAC': ['1'], 'MLEAF': ['0.167'], 'MQ': ['52.77'], 'MQRankSum': ['-4.631'], 'QD': ['0.39'], 'ReadPosRankSum': ['1.45'], 'SOR': ['0.758'], 'VQSLOD': ['-8.209'], 'culprit': ['MQ'], 'ANNOVAR_DATE': ['2018-04-16'], 'Func.refGene': ['intergenic'], 'Gene.refGene': ['IL2,IL21'], 'GeneDetail.refGene': ['dist=38536,dist=117597'], 'ExonicFunc.refGene': [], 'AAChange.refGene': [], 'Func.ensGene': ['intergenic'], 'Gene.ensGene': ['ENSG00000109471,ENSG00000138684'], 'GeneDetail.ensGene': ['dist=38306,dist=117597'], 'ExonicFunc.ensGene': [], 'AAChange.ensGene': [], 'cytoBand': ['4q27'], 'gwasCatalog': [], 'tfbsConsSites': [], 'wgRna': [], 'targetScanS': [], 'Gene_symbol': [], 'OXPHOS_Complex': [], 'Ensembl_Gene_ID': [], 'Ensembl_Protein_ID': [], 'Uniprot_Name': [], 'Uniprot_ID': [], 'NCBI_Gene_ID': [], 'NCBI_Protein_ID': [], 'Gene_pos': [], 'AA_pos': [], 'AA_sub': [], 'Codon_sub': [], 'dbSNP_ID': [], 'PhyloP_46V': [], 'PhastCons_46V': [], 'PhyloP_100V': [], 'PhastCons_100V': [], 'SiteVar': [], 'PolyPhen2_prediction': [], 'PolyPhen2_score': [], 'SIFT_prediction': [], 'SIFT_score': [], 'FatHmm_prediction': [], 'FatHmm_score': [], 'PROVEAN_prediction': [], 'PROVEAN_score': [], 'MutAss_prediction': [], 'MutAss_score': [], 'EFIN_Swiss_Prot_Score': [], 'EFIN_Swiss_Prot_Prediction': [], 'EFIN_HumDiv_Score': [], 'EFIN_HumDiv_Prediction': [], 'CADD_score': [], 'CADD_Phred_score': [], 'CADD_prediction': [], 'Carol_prediction': [], 'Carol_score': [], 'Condel_score': [], 'Condel_pred': [], 'COVEC_WMV': [], 'COVEC_WMV_prediction': [], 'PolyPhen2_score_transf': [], 'PolyPhen2_pred_transf': [], 'SIFT_score_transf': [], 'SIFT_pred_transf': [], 'MutAss_score_transf': [], 'MutAss_pred_transf': [], 'Perc_coevo_Sites': [], 'Mean_MI_score': [], 'COSMIC_ID': [], 'Tumor_site': [], 'Examined_samples': [], 'Mutation_frequency': [], 'US': [], 'Status': [], 'Associated_disease': [], 'Presence_in_TD': [], 'Class_predicted': [], 'Prob_N': [], 'Prob_P': [], 'SIFT_converted_rankscore': [], 'SIFT_pred': [], 'Polyphen2_HDIV_score': [], 'Polyphen2_HDIV_rankscore': [], 'Polyphen2_HDIV_pred': [], 'Polyphen2_HVAR_score': [], 'Polyphen2_HVAR_rankscore': [], 'Polyphen2_HVAR_pred': [], 'LRT_score': [], 'LRT_converted_rankscore': [], 'LRT_pred': [], 'MutationTaster_score': [], 'MutationTaster_converted_rankscore': [], 'MutationTaster_pred': [], 'MutationAssessor_score': [], 'MutationAssessor_score_rankscore': [], 'MutationAssessor_pred': [], 'FATHMM_score': [], 'FATHMM_converted_rankscore': [], 'FATHMM_pred': [], 'PROVEAN_converted_rankscore': [], 'PROVEAN_pred': [], 'VEST3_score': [], 'VEST3_rankscore': [], 'MetaSVM_score': [], 'MetaSVM_rankscore': [], 'MetaSVM_pred': [], 'MetaLR_score': [], 'MetaLR_rankscore': [], 'MetaLR_pred': [], 'M-CAP_score': [], 'M-CAP_rankscore': [], 'M-CAP_pred': [], 'CADD_raw': [], 'CADD_raw_rankscore': [], 'CADD_phred': [], 'DANN_score': [], 'DANN_rankscore': [], 'fathmm-MKL_coding_score': [], 'fathmm-MKL_coding_rankscore': [], 'fathmm-MKL_coding_pred': [], 'Eigen_coding_or_noncoding': [], 'Eigen-raw': [], 'Eigen-PC-raw': [], 'GenoCanyon_score': [], 'GenoCanyon_score_rankscore': [], 'integrated_fitCons_score': [], 'integrated_fitCons_score_rankscore': [], 'integrated_confidence_value': [], 'GERP++_RS': [], 'GERP++_RS_rankscore': [], 'phyloP100way_vertebrate': [], 'phyloP100way_vertebrate_rankscore': [], 'phyloP20way_mammalian': [], 'phyloP20way_mammalian_rankscore': [], 'phastCons100way_vertebrate': [], 'phastCons100way_vertebrate_rankscore': [], 'phastCons20way_mammalian': [], 'phastCons20way_mammalian_rankscore': [], 'SiPhy_29way_logOdds': [], 'SiPhy_29way_logOdds_rankscore': [], 'Interpro_domain': [], 'GTEx_V6_gene': [], 'GTEx_V6_tissue': [], 'esp6500siv2_all': [], 'esp6500siv2_aa': [], 'esp6500siv2_ea': [], 'ExAC_ALL': [], 'ExAC_AFR': [], 'ExAC_AMR': [], 'ExAC_EAS': [], 'ExAC_FIN': [], 'ExAC_NFE': [], 'ExAC_OTH': [], 'ExAC_SAS': [], 'ExAC_nontcga_ALL': [], 'ExAC_nontcga_AFR': [], 'ExAC_nontcga_AMR': [], 'ExAC_nontcga_EAS': [], 'ExAC_nontcga_FIN': [], 'ExAC_nontcga_NFE': [], 'ExAC_nontcga_OTH': [], 'ExAC_nontcga_SAS': [], 'ExAC_nonpsych_ALL': [], 'ExAC_nonpsych_AFR': [], 'ExAC_nonpsych_AMR': [], 'ExAC_nonpsych_EAS': [], 'ExAC_nonpsych_FIN': [], 'ExAC_nonpsych_NFE': [], 'ExAC_nonpsych_OTH': [], 'ExAC_nonpsych_SAS': [], '1000g2015aug_all': [], '1000g2015aug_afr': [], '1000g2015aug_amr': [], '1000g2015aug_eur': [], '1000g2015aug_sas': [], 'CLNALLELEID': [], 'CLNDN': [], 'CLNDISDB': [], 'CLNREVSTAT': [], 'CLNSIG': [], 'dbscSNV_ADA_SCORE': [], 'dbscSNV_RF_SCORE': [], 'snp138NonFlagged': [], 'avsnp150': [], 'CADD13_RawScore': ['0.015973'], 'CADD13_PHRED': ['2.741'], 'Eigen': ['-0.3239'], 'REVEL': [], 'MCAP': [], 'ICGC_Id': [], 'ICGC_Occurrence': [], 'gnomAD_genome_ALL': ['0.0003'], 'gnomAD_genome_AFR': ['0.0001'], 'gnomAD_genome_AMR': ['0'], 'gnomAD_genome_ASJ': ['0'], 'gnomAD_genome_EAS': ['0.0007'], 'gnomAD_genome_FIN': ['0.0009'], 'gnomAD_genome_NFE': ['0.0002'], 'gnomAD_genome_OTH': ['0.0011'], 'gerp++gt2': [], 'cosmic70': [], 'InterVar_automated': [], 'PVS1': [], 'PS1': [], 'PS2': [], 'PS3': [], 'PS4': [], 'PM1': [], 'PM2': [], 'PM3': [], 'PM4': [], 'PM5': [], 'PM6': [], 'PP1': [], 'PP2': [], 'PP3': [], 'PP4': [], 'PP5': [], 'BA1': [], 'BS1': [], 'BS2': [], 'BS3': [], 'BS4': [], 'BP1': [], 'BP2': [], 'BP3': [], 'BP4': [], 'BP5': [], 'BP6': [], 'BP7': [], 'Kaviar_AF': [], 'Kaviar_AC': [], 'Kaviar_AN': []}
results = create_dictionary_of_info_field_values(info_field)
assert expected_results == results


# # Part 8 (5 points)
# Write a function whose input is the output from `create_dictionary_of_info_field_values` and uses the previously written function `determine_data_type_of_list` to determine the data type of each of the info fields. The output is a dictionary whose keys are the name of the info fields and values are the data type.  

# In[141]:


def determine_data_type_of_info_fields(data):
    """
    See desription in part 8
    """
    # YOUR CODE HERE
    dict1 = {}
    data1 = ''
    for key,value in data.items():
        data1 = determine_data_type_of_list(value)
        dict1[key] = data1
    return dict1
    raise NotImplementedError()


# In[142]:


data = {'key1': ['1', '2', '3'], 'key2':['1.1', '2.2', '3.3'], 'key3': ['1.1', '2', '3.3'], 'key4': ['1.1', '234String', '3.3']}
expected_results = {'key1': int, 'key2': float, 'key3': float, 'key4': str}

assert determine_data_type_of_info_fields(data) == expected_results


# # Part 9  (No points)
# Write a function whose first input is the data from  `read_vcf_file` and the second input is the output from `determine_data_type_of_info_fields`. The function converts the info field into a dictionary and uses the data types that you determined to cast each field into the correct data type. Make sure to convert the `POS` to int and `QUAL` to float. Replace any `\\x3b` with a comma and any `\\x3d` with an equal sign. The output will look something like this (I have removed most of the fields):
# 
# The output will look something like this 
# ```
# {
#         "ALT": "G",
#         "CHROM": "4",
#         "FILTER": "PASS",
#         "ID": ".",
#         "INFO": {
#            
#             "Gene.ensGene": "ENSG00000109471,ENSG00000138684",
#             "Gene.refGene": "IL2,IL21",
#             "GeneDetail.ensGene": "dist=38306,dist=117597",
#             "GeneDetail.refGene": "dist=38536,dist=117597"
#         },
#         "POS": 123416186,
#         "QUAL" :23.25,
#         "REF": "A",
#         "SAMPLE": {
#             "XG102": {
#                 "AD": "51,8",
#                 "DP": "59",
#                 "GQ": "32",
#                 "GT": "0/1",
#                 "PL": "32,0,1388"
#             }
#     }
# ```

# In[149]:


def format_data(data, info_field_data_type):
    # YOUR CODE HERE
    list1 = []
    str1 = None
    str2 = ''
    f2 = []
    for i in range(len(data)):
        f1 = {}
        dict1 = {}
        str2 = data[i]['INFO']
        str2 = str2.replace("\\x3b",",")
        str2 = str2.replace("\\x3d","=")
        f2 = str2.split(";")
        for j in f2:
            key1 = ''
            value1 = ''
            flag = False
            for ch in j:
                if ch == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key1 += ch
                else:
                    value1 += ch
            if value1 != '':
                if value1 != '.':
                    f1[key1] = value1
                
        for key,value in f1.items():
            str1 = info_field_data_type[key]
            if str1 == int:
                dict1[key] = int(value)
            elif str1 == float:
                dict1[key] = float(value)
            elif str1 == str:
                dict1[key] = str(value)
            else:
                dict1[key] = ''
            
        list1.append(dict1)
        data[i]['POS'] = int(data[i]['POS'])
        data[i]['QUAL'] = float(data[i]['QUAL'])
        
    for i in range(len(list1)):
        data[i]['INFO'] = list1[i]
        
    return data

    raise NotImplementedError()


# # Part 10 (No Points)
# Write a function whose inputs are a Python dictionary and filename. The function will saves the dictionary as a json file using the filename given. Use the json library. Use these options to correctly format your JSON -- `sort_keys=True, indent=4, separators=(',', ': ')`. 
# Use this function to save your parsed data as a json file. 
# 
# USE THE FOLLOWING FILENAME TO SAVE YOUR FILE: `lab1.json`

# In[150]:



def save_data_as_json(data, filename):
    # YOUR CODE HERE
    import json
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    
    #raise NotImplementedError()


# # Part 11 (10 points)
# Write a function whose input is a filename for a json file. The function should use the filename to read the JSON file in which you saved your final parsed data. 

# In[151]:


def load_data_from_json(filename):
    # YOUR CODE HERE
    import json
    
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

    #raise NotImplementedError()


# In[152]:


test_save_data = {'key1': ['1', '2', '3'], 'key2':['1.1', '2.2', '3.3'], 'key3': ['1.1', '2', '3.3'], 'key4': ['1.1', '234String', '3.3']}
save_data_as_json(test_save_data, 'test_save.json')
results = load_data_from_json('test_save.json')

assert results == test_save_data


# # Part 12 (30 points)
# Write a function whose inputs are `CHROM`, `REF`, `ALT`, `POS`, and `filename`.  Using these inputs, the function should load a JSON file using the given filename and return a list of variants that match 
# the given CHROM, REF, ALT, and POS. 

# In[153]:


def find_variant(CHROM, REF, ALT, POS, filename):
    # YOUR CODE HERE
    list1 = []

    data = load_data_from_json(filename)
    print(data)
    
    for i in range(len(data)):
        if data[i]['CHROM'] == CHROM and data[i]['REF'] == REF and data[i]['ALT'] == ALT and data[i]['POS'] == POS:
            list1.append(data[i])
    
    return(list1)
    raise NotImplementedError()


# In[154]:







filename = 'lab1_data.vcf' 
data = read_vcf_file(filename) # read vcf file 
info_field_data = extract_info_field(data) # extract all the info fields
info_field_list = create_dictionary_of_info_field_values(info_field_data) # create dictionary from info fields
info_field_data_type = determine_data_type_of_info_fields(info_field_list) # Determine data type of each info field
data = format_data(data, info_field_data_type) # format the data variable -- from data = read_vcf_file(filename)
save_data_as_json(data, 'lab1.json') # save the formatted data
data_loaded = load_data_from_json('lab1.json') # load saved data 

# Now I will fetch three variants using your find_variant function and check that they match my results


# In[ ]:





# In[ ]:




