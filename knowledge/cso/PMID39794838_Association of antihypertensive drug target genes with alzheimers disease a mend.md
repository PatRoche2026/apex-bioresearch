# Association of antihypertensive drug target genes with alzheimer's disease: a mendelian randomization study.

**PMID:** 39794838
**Journal:** Alzheimer's research & therapy (2025)
**Authors:** Zheng H, Chen C, Feng Y
**PMC:** PMC11720623
**Search context:** genetic_target_validation

## Full Text


### Introduction

Nearly one in three adults aged 30–79 years were estimated to have hypertension globally in 2019 [1], leading to a high prevalence of antihypertensive medication use. Hypertension, particularly in midlife, is recognized as a significant predisposing factor for late-life cognitive decline, manifesting in both vascular dementia and Alzheimer’s disease (AD) [2–4]. The relationship between blood pressure (BP) and dementia risk in advanced age tends to exhibit a negative or U-shaped curve, indicating increased risk associated with both hypotension and hypertension [5]. Additionally, different antihypertensive medications have yielded divergent effects on the risk of AD. For instance, a meta-analysis of 15 observational studies with 3,307,532 participants found that angiotensin receptor blockers (ARBs), but not angiotensin-converting enzyme inhibitors (ACEIs), reduced the risk of any dementia and AD [6]. However, observational studies are susceptible to biases from factors such as residual confounding and reverse causation. Given the high prevalence of hypertension among Alzheimer’s patients, understanding the precise influence of these pharmaceuticals on neurodegenerative symptoms is critical for optimizing therapeutic strategies in patients with comorbidity conditions.
Conventionally, randomized clinical trials (RCTs) are the gold standard for establishing causal relationships in drug efficacy studies. However, due to financial constraints and feasibility issues, large, high-quality RCTs still need to be conducted to investigate the effects of antihypertensives on AD. Mendelian randomization (MR) is a statistical genetics approach that uses genetic variants robustly associated with exposure as potentially unconfounded instruments to infer whether an observed association between the exposure and outcome is causal. Several genome-wide association studies (GWAS) of AD have identified genetic risk variants within the ACE gene, whose encoded protein is the target of antihypertensive agents inhibiting the angiotensin converting enzyme [7, 8]. However, the effect of whole standard classes of antihypertensive drugs on AD risk remains unknown. Ou et al. reported that calcium channel blockers (CCBs) were identified as a promising strategy for AD prevention using a two-sample MR analysis [9]. However, the analysis did not include the ACEi, a common antihypertensive medication [10]. Additionally, the instrumental variables (IVs) for some classes of drugs were so limited that analyses capturing all possible drug target genes with corresponding IVs are needed. Finally, IVs for the drugs were not distinguished tissue, such as blood or brain, which may limit its interpretability. Furthermore, both empirical results and theoretical models provide evidence that most common disease-associated variants act through changes in gene expression rather than directly influencing protein structure or function [11]. MR analysis is particularly advantageous in analyzing the effects of drugs, where genetic variants associated with the expression of drug target genes (termed expression or protein quantitative trait loci - eQTLs or pQTLs) serve as proxies for drug exposure, such as eQTLGen [12], GTEx [13], PsychENCODE [14], and BrainMeta V2 [15].
In this study, we utilized publicly available eQTL datasets both in blood and brain to elucidate the potential associations between antihypertensive treatments and AD risk using a two-sample MR design. This study will add evidence to the current knowledge derived from observational studies and try to draw causal conclusions regarding the potential association between antihypertensive medication use and AD risk.

### Methods


### Study design

The study design is illustrated in Fig. 1. First, we conducted a two-sample MR analysis to identify drug target genes utilizing publicly available eQTL datasets in blood and brain as genetic instruments (IVs) and GWAS summary statistics of SBP as the outcome. Second, we employed a two-sample MR analysis to estimate the relationship between each drug target gene expression and the risk of AD. Third, we performed sensitivity analyses to further validate the MR associations, including detecting reverse causality, assessing horizontal pleiotropy, Bayesian colocalization, scanning phenotypes, and protein quantitative trait loci (pQTL) analysis. Finally, we verified our findings with additional eQTL datasets and GWAS summary statistics for AD.
Fig. 1Summary of study design
Summary of study design
The MR framework relies on three key assumptions: (i) relevance, where genetic variants should be significantly associated with exposures; (ii) exclusiveness, where genetic variants are not linked to potential confounders; and (iii) independence, where genetic variants affect outcomes only through the exposures. The study adhered to the Strengthening the Reporting of Observational Studies in Epidemiology-Mendelian randomization reporting guidelines (STROBE-MR) [16] (Table S1). The online tool mRnd (https://shiny.cnsgenomics.com/mRnd/) was utilized to assess the statistical power and calculate the results.

### Identification of drug target genes

The commonly prescribed antihypertensive medications, including ACEis, ARBs, beta-blockers (BBs), CCBs, diuretics, and other antihypertensive agents, were included in the analysis. Potential therapeutic genes were obtained from the DrugBank (https://go.drugbank.com/) [17] and ChEMBL (https://www.ebi.ac.uk/chembl/) databases. Genomic regions associated with these genes were retrieved from GeneCards (https://www.genecards.org/). To demonstrate that changes in gene expression are associated with reduced blood pressure due to drug exposure, we conducted summary-data-based Mendelian Randomization (SMR) analysis with blood gene expression (from the eQTLGen data) as exposure [12] and systolic blood pressure (SBP) as the positive outcome, with summary data from a GWAS of SBP in 757,601 individuals of European ancestry sourced from the UK Biobank and the International Consortium of Blood Pressure Genome Wide Association Studies (ICBP) [18]. Genes with blood expression associated with SBP at least nominal significance (i.e., P < 0.05) were included in further analysis. The SMR method estimated SBP change per standard deviation (SD) increment in gene expression.

### Blood and brain expression quantitative trait loci

Our analysis utilized publicly available data from the eQTLGen consortium (comprising 31,684 individuals) to identify significant (minor allele frequency > 1%; p < 5 × 10− 8) single-nucleotide polymorphisms (SNPs) associated with the expression of antihypertensive drug target genes in blood. Only cis associations are available in the eQTLGen data (distance between SNP and gene is < 1 MB). The eQTL data are scaled to a 1-SD change in gene expression per additional effect allele. The strength of SNP instruments was assessed using the F statistic. The discovery brain eQTL data were obtained from the PsychENCODE consortium [14], which included 1,387 prefrontal cortex, predominantly of European samples. In addition, we used whole blood and brain-related eQTLs from the Genotype-Tissue Expression (GTEx) project V8 [13] and BrainMeta V2 [15], including 2,865 cortex European samples, to validate our findings. Further details on the eQTLs are provided in Table S2.

### GWAS summary statistics of Alzheimer’s disease

We obtained publicly available case-control GWAS summary statistics for AD, including 111,326 clinically diagnosed cases and 677,663 controls [19]. This dataset includes contributions from various European GWAS consortia and a new dataset from 15 European countries. Moreover, an AD GWAS from the FinnGen cohort, which included 9,301 cases and 367,976 controls, was used to validate our finding [20]. Details for accessing the summary statistics used in the current analyses are provided in Table S3.

### Summary-level mendelian randomization

We conducte
[...truncated]