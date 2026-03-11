# Genomics-Based Target Validation: A CSO's Framework

## The Hierarchy of Genetic Evidence
Not all genetic evidence is created equal. The gold standard for target validation is convergent evidence from multiple independent genetic approaches:

1. **Tier 1 — Mendelian disease phenocopy**: If loss-of-function mutations in a gene cause a human disease that phenocopies the target indication, this is the strongest possible genetic evidence. Examples: PCSK9 loss-of-function → low LDL (validated by evolocumab/alirocumab), SCN9A loss-of-function → pain insensitivity.

2. **Tier 2 — GWAS + colocalization**: A genome-wide significant association (p < 5e-8) in a well-powered GWAS, where colocalization analysis confirms the signal maps to the target gene (not a neighbor). Must distinguish correlation from causation using Mendelian randomization.

3. **Tier 3 — Functional genomics support**: CRISPR screens, gene expression data, or proteomics showing the target is active in relevant cell types and disease contexts. Necessary but insufficient alone.

4. **Tier 4 — Animal model data only**: The weakest evidence. Many targets validated in mice fail in humans due to species differences in pathway biology, immune function, or target expression patterns.

## Critical Assessment Questions
- Does the genetic evidence point to gain-of-function or loss-of-function? This determines whether you need an agonist or antagonist.
- Is the genetic effect size clinically meaningful? A statistically significant GWAS hit with tiny effect size may not translate to therapeutic benefit.
- Are there compensatory pathways? Genetic redundancy can undermine therapeutic efficacy even when the target is valid.
- What is the expression pattern? A target expressed broadly may have on-target toxicity in non-disease tissues.

## Common Pitfalls in Target Validation
- **Confounding by linkage disequilibrium**: Nearby genes in LD can create false attribution of GWAS signals
- **Population stratification**: Genetic associations that reflect ancestry rather than biology
- **Publication bias**: Positive functional genomics results are published; negative results are not
- **Species extrapolation**: ~50% of targets validated in rodent models fail to translate to humans
- **Single-study reliance**: Any single study can be wrong. Demand replication across independent cohorts and methodologies.

## Quantitative Benchmarks
Programs with human genetic evidence supporting the target mechanism have approximately 2x higher probability of clinical success (Nelson et al., Nature Genetics 2015). Programs with Mendelian disease phenocopy evidence have even higher success rates (~3x). These statistics should inform scoring: a target with only animal model data deserves a substantially lower scientific validity score than one with convergent human genetic evidence.
