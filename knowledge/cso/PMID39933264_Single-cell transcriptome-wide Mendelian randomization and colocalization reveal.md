# Single-cell transcriptome-wide Mendelian randomization and colocalization reveals immune-mediated regulatory mechanisms and drug targets for COVID-19.

**PMID:** 39933264
**Journal:** EBioMedicine (2025)
**Authors:** Ying H, Wu X, Jia X et al.
**PMC:** PMC11867302
**Search context:** genetic_target_validation

## Full Text

Research in contextEvidence before this studyWe searched for key terms in PubMed for publications prior to August 1, 2024, using the following terms: (“COVID-19" or “SARS-CoV-2”) AND (“single-cell eQTL” or “protein” or “transcript”) AND (“Genome-wide association study” or “single-cell Mendelian randomization” or “causal genes”). Our search identified multiple studies that have pinpointed genes or proteins associated with COVID-19. However, there is a notable lack of studies that integrate single-cell eQTLs with Mendelian randomization to systematically investigate the potential causal relationships between immune-related genes and COVID-19 in European populations.Added value of this studyWe systematically evaluated the immune-mediated genes and mechanisms for COVID-19 by combining single-cell eQTL MR and colocalization with pathway and protein–protein interaction information. We identified 343 MR associations for 132 genes in 14 immune-cell types related to four types of COVID-19 outcomes, with 58 genes that, to the best of our knowledge, were not reported previously. NCR3, a gene with robust MR evidence on severe COVID-19, interacted with SARS-COV-2 proteins, and its targeted drug is currently under clinical trials for cancer treatment. We further developed a tier system to prioritize COVID-19 drug targets and identified 37 promising drug target genes that showed multiple layers of evidence.Implications of all the available evidenceOur study identifies immune-mediated causal genes and mechanisms for COVID-19 and provides a tier system to prioritize immune-related drug targets for COVID-19.

### Research in context


### Evidence before this study

We searched for key terms in PubMed for publications prior to August 1, 2024, using the following terms: (“COVID-19" or “SARS-CoV-2”) AND (“single-cell eQTL” or “protein” or “transcript”) AND (“Genome-wide association study” or “single-cell Mendelian randomization” or “causal genes”). Our search identified multiple studies that have pinpointed genes or proteins associated with COVID-19. However, there is a notable lack of studies that integrate single-cell eQTLs with Mendelian randomization to systematically investigate the potential causal relationships between immune-related genes and COVID-19 in European populations.

### Added value of this study

We systematically evaluated the immune-mediated genes and mechanisms for COVID-19 by combining single-cell eQTL MR and colocalization with pathway and protein–protein interaction information. We identified 343 MR associations for 132 genes in 14 immune-cell types related to four types of COVID-19 outcomes, with 58 genes that, to the best of our knowledge, were not reported previously. NCR3, a gene with robust MR evidence on severe COVID-19, interacted with SARS-COV-2 proteins, and its targeted drug is currently under clinical trials for cancer treatment. We further developed a tier system to prioritize COVID-19 drug targets and identified 37 promising drug target genes that showed multiple layers of evidence.

### Implications of all the available evidence

Our study identifies immune-mediated causal genes and mechanisms for COVID-19 and provides a tier system to prioritize immune-related drug targets for COVID-19.

### Introduction

The coronavirus disease (COVID-19) pandemic has resulted in nearly 7 million deaths during the past four years (https://covid19.who.int/).1,2 Although vaccination against COVID-19 reduces the risk of severe COVID-19 disease and death, the continual emergence of SARS-CoV-2 variants with increased transmission and immune evasion has led to breakthrough infections in vaccinated individuals.3,4
Until now, over 700 agents with anti-SARS-CoV-2 mechanisms have been investigated in preclinical and/or clinical studies, with more than 20 anti-SARS-CoV-2 drugs proposed to reduce the risk of severe COVID-19.5 However, the emergence of drug safety issues,6 drug resistance,7,8 and limited treatment effectiveness9,10 have made it imperative to search for new anti-coronavirus drug candidates that are highly specific to one cell type and widely applicable to many people.
Given the strong connections between the immune system and COVID-19,11, 12, 13, 14 previous studies have extensively investigated the use of immunomodulators, such as systemic corticosteroids,15 anticoagulants,16 and cytokine antagonists,17 to mitigate the dysfunctional responses in patients with COVID-19.11,13,18, 19, 20, 21 Immune cells exhibit diverse states during different stages of infection. In the early stage, the virus enters the body through endothelial cells expressing targets like OAS1 and ACE2. This alters the expression of genes like IFNAR2, affecting cell interactions and downstream gene expression. Consequently, a cascade effect occurs, leading to reduced functionality of natural killer (NK) cells and monocytes/macrophages, as well as coagulation disorders.22 However, the exact cause of immune cell responses, e.g. NK cell dysfunction, on COVID-19 remains unclear.21 It is urgently needed to uncover the immune-mediated mechanism and additional drug targets for COVID-19.
Recent studies have shown the value of human genetic evidence in increasing the success rate of drug trials.23 Existing genome-wide association studies (GWAS) have identified a whole set of genomic loci that are associated with COVID-19.22,24, 25, 26 However, the causality of these genes is less clear. Some post-GWAS approaches, such as Mendelian randomization (MR), can estimate the putative causal effects of expression levels of genes and proteins on COVID-19, which have prioritized drug targets, such as OAS1, IL6R, in a cost-effective manner.27,28 However, most of the existing studies have used expression data measured in bulk tissues, which may mask the cell-type specific effect of genes and proteins on COVID-19. Advancements in single-cell RNA sequencing (scRNA-seq) technology have facilitated the examination of gene expression patterns at the individual cell level.29 Recent genetic studies have mapped genetic variants with single-cell expression data and identified a list of cell-type specific expression quantitative trait loci (eQTL, which is a genetic variant robustly associated with expression levels of a gene in a certain cell type).30 Single cell eQTL mapping has proven to be a valuable tool in identifying causal genes and understanding their involvement in disease pathogenesis, including immune diseases31,32 and COVID-19 in the Japanese population.33,34 However, few studies have integrated single-cell eQTLs with MR to systematically investigate the putative causal relationships between immune-related genes and COVID-19 in other ancestries.
In this study, we conducted a single-cell eQTL MR and colocalization analysis to investigate the putative causal effects of gene expressions from 14 immune cell types on risk of COVID-19 severities. Functional enrichment analysis and predictions of host-pathogen protein interactions were further applied to identify immune-mediated causal genes and networks involved in the pathophysiology of COVID-19. Integrating genetic evidence with clinical trial information, we developed a tier system to prioritize immune-mediated drug targets for COVID-19.

### Methods


### Ethics

This study did not require ethical approval as all analysis was based on publicly available aggregated statistics without access to individual data. The included GWAS studies obtained informed consent from the study participants and were approved by the relevant local ethics committees.

### Instrument selection and validation

In this study, the genetic variants associated with plasma eQTLs were used as genetic instruments for the Mendelian randomization (MR) analysis. We started the instrument selection process by accessing the cis-eQTL data from OneK1K data. We selected all conditionally independent cis-eQTLs that were associated with eGenes at a p-value <0.005. To ensure accuracy, w
[...truncated]