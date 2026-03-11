# Oncostatin M Is a Biomarker of Diagnosis, Worse Disease Prognosis, and Therapeutic Nonresponse in Inflammatory Bowel Disease.

**PMID:** 33624092
**Journal:** Inflammatory bowel diseases (2021)
**Authors:** Verstockt S, Verstockt B, Machiels K et al.
**PMC:** PMC8522791
**Search context:** osmr_ibd

## Full Text


### INTRODUCTION

Crohn disease (CD) and ulcerative colitis (UC) are chronic, relapsing inflammatory bowel diseases (IBDs) with increasing prevalence worldwide.1, 2 A single reference standard for IBD diagnosis does not exist.3 Often, the diagnosis is significantly delayed, leading to a postponed treatment initiation and subsequently affecting overall quality of life and disease progression.4 Together with the significant rate of primary and secondary resistance to current IBD treatments,5 novel therapeutic targets and biomarkers supporting these clinical needs are eagerly awaited.
Among potential targets and biomarkers, oncostatin M (OSM) has gained a lot of interest. In 2017, West, Hegazy, et al6 reported an increased expression of OSM and the OSM receptor-β (OSMR) in inflamed intestinal tissue from patients with IBD, where it drives intestinal stromal cell inflammation. The authors also showed that increased OSM predicts nonresponsiveness to anti-tumor necrosis factor (TNF) therapy.
OSM is part of the interleukin (IL)-6 cytokine family and signals via a receptor complex composed of the gp130 co-receptor (similar for all IL-6 family members) and either OSMR or the leukemia inhibitory factor receptor-β (LIFR; Fig. 1A).7-9 In both cases (ie. OSMR or LIFR), formation of the heterodimeric complex can induce different signaling cascades (ie, JAK-STAT pathway, PI3K-Akt pathway), which depend on cell type and environmental conditions.10, 11
Mucosal OSM and OSMR levels and serum OSM in newly diagnosed patients with IBD. A, OSM signals via a receptor complex composed of the gp130 co-receptor and either OSMR or LIFR. B-C, Boxplots of mucosal OSM and OSMR as measured by RNA sequencing (normalized counts). D, Boxplots of serum OSM as measured by the OLINK proximity extension technology (NPX values). Significant comparisons are highlighted in bold. NPX indicates normalized protein expression values.
In this study, we aimed to further unravel the potential of OSM and related receptors as markers of diagnosis, prognosis, and therapy response in IBD, both in the mucosa and in serum. We therefore investigated 5 different clinical scenarios: (1) newly diagnosed patients with IBD, (2) patients initiating anti-TNF or (3) vedolizumab therapy, (4) postoperative patients with CD 6 months after surgery, and (5) unaffected first-degree relatives (FDRs).

### MATERIALS AND METHODS


### Patient Recruitment and Sample Collection

We cross-sectionally studied mucosal biopsies and serum from patients with CD and with UC: (1) newly diagnosed patients, (2) patients initiating anti-TNF or (3) vedolizumab therapy, (4) postoperative patients with CD 6 months after ileocolonic resection with ileocolonic anastomosis, and (5) multiple-affected families with IBD, including unaffected FDRs. For each group, matched samples from non-IBD control patients were included as comparison. Baseline characteristics for each study cohort are listed in Supplementary Tables S1–5. An overview of the studied samples and groups can be found in Table 1. Ileal expression data generated in our study center were only available in the context of early IBD, ie, newly diagnosed and postoperative patients with recurrent CD.12
Overview of the Studied Samples and Corresponding Applied Definitions and Technologies
RNAseq indicates RNA sequencing. *RNA sequencing based; **Microarray based.
Newly diagnosed patients with IBD who were treatment-naïve were included 6 months after diagnosis, were naïve for biologics/immunosuppressives, and had not had IBD-related surgery. A poor prognosis at the time of diagnosis was defined as the need for biologic therapy within 2 years after diagnosis. Endoscopic remission after anti-TNF or vedolizumab therapy was defined as the complete absence of ulcerations at month 6 (CD) or a Mayo endoscopic subscore of 0 to 1 at week 8/14 (UC). Patients with CD who underwent ileocecal resection with ileocolonic anastomosis and had a Rutgeerts score ≥ i2b at month 6, were considered as postoperative recurrent patients.13,14 Multiple-affected families with IBD were defined as those with at least 3 FDRs with IBD.
All biopsies were taken during endoscopy and stored in RNALater buffer (Ambion, Austin, TX) at –80°C. Biopsies from patients with IBD were collected at the most affected site, at the edge of the ulcerative surface. Control biopsies were collected from individuals undergoing screening colonoscopies and who had a normal endoscopy.
To localize OSM, resected intestinal tissue from patients with IBD undergoing surgery and resected unaffected intestinal tissue from control patients who did not hae IBD but did have colorectal cancer were collected. Tissue from these control patients was collected adjacent to the tumor-free resection margin.

### Mucosal

Mucosal expression levels of OSM, OSMR, LIFR, and IL6ST (encode for the gp130 co-receptor) were obtained using microarray technology or RNA sequencing (Table 1).
For microarray analysis (postoperative CD cohort only), total RNA was extracted from biopsies using the RNeasy Mini Kit (Qiagen, Hilden, Germany) and was analyzed via GeneChip Human Gene 1.0 ST arrays (Affymetrix, Santa Clara, CA). Quality control and data analysis (R) were performed as previously described.12 The robust multichip average method15 was applied on Affymetrix raw data (.cel files), resulting in log2 expression values at the probe level.
We performed RNA sequencing on mucosal biopsies from newly diagnosed patients and patients initiating anti-TNF or vedolizumab therapy. Total RNA was extracted from the samples using the AllPrep DNA/RNA Mini kit (Qiagen) after tissue lysis using the FastPrep Lysing Matrix D tubes (MP Biomedicals, Brussels, Belgium). The integrity and quantity of RNA were evaluated with a 2100 Bioanalyzer and a Nanodrop ND-1000 spectrophotometer, respectively. After library preparation using the TruSeq Stranded mRNA protocol (Illumina, San Diego, CA), single-end RNA sequencing was performed on 500 ng total RNA (Illumina HiSeq 4000NGS). Raw sequencing data were then aligned to the reference genome (Hisat2 v.2.1.016), and absolute counts were generated using HTSeq.17 Counts were then normalized for library size using the R\DESeq2 package.18 Using the cellular xCell deconvolution method,19 macrophage enrichment scores from bulk RNA data were calculated. The effect of anti-TNF therapy on genes of interest in the colonic mucosa was investigated using publicly available microarray datasets (GEO GSE12251, GSE14580, GSE16879).20, 21

### Serum OSM Levels

Relative serum OSM protein levels were quantified using proximity extension technology with an inflammation panel (Olink Proteomics AB, Uppsala, Sweden). Quality control and normalization of the data were performed using an internal extension control and an interplate control to adjust for intra- and interrun variation. Validation data can be found on the manufacturer’s website (https://www.olink.com). The final readout was expressed in normalized protein expression values, an arbitrary unit on a log2 scale.

### Fecal Calprotectin

Fecal calprotectin was extracted using the Smart Prep extraction device (Roche Diagnostics, Mannheim, Germany), and concentrations were measured using the fCAL enzyme-linked immunosorbent assay kit (Bühlmann Laboratories AG, Schönenbuch, Switzerland).

### Immunohistochemistry

Immunohistochemical stainings were performed on 5 μm–thick glass-mounted sections prepared from formalin-fixed paraffin-embedded transmural bowel biopsies, using the BOND MAX autostainer (Leica Microsystems Ltd., Heerbrugg, Switzerland). Epitope retrieval was performed in citrate buffer (pH 6) at 98°C for 30 minutes. Rabbit polyclonal OSM antibody (ab198830, Abcam, Cambridge, UK) concentration was optimized, and a dilution of 1:200 was applied. The bound primary antibody was visualized using the BOND Polymer Refine Detection kit. All stains were evaluated by an IBD-experienced pathologist (G. De Hertogh). Micro
[...truncated]