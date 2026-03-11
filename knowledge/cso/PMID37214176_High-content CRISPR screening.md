# High-content CRISPR screening.

**PMID:** 37214176
**Journal:** Nature reviews. Methods primers (2022)
**Authors:** Bock C, Datlinger P, Chardon F et al.
**PMC:** PMC10200264
**Search context:** crispr_target_discovery

## Full Text

There is a need in molecular biology and biomedical research for open-ended, hypothesis-generating research, in order to discover previously unknown molecular mechanisms. Genetic screening provides a powerful approach for identifying genes, pathways and mechanisms involved in a given phenotype or biological process. This is illustrated by the many successes of forward genetics in cell lines1 and in model organisms such as flies2,3, worms4, yeast5, plants6 and fish7, and pioneering work in RNA interference (RNAi) screens8,9.

### Forward genetics

Screening approach in which genes involved in the phenotype of interest are identified by screening genetically perturbed cells.
CRISPR screens exploit the efficiency and flexibility of CRISPR–Cas genome editing10. They have become a popular and productive tool for biological discovery in a broad range of applications11,12. In a typical pooled CRISPR screen (FIG. 1), a CRISPR guide RNA (gRNA) library is introduced in bulk into cells, such that individual cells receive different gRNAs and are perturbed according to the gRNA received by the cell. These gRNAs are usually delivered by lentiviral transduction and are integrated into the DNA of the target cells, making it possible to efficiently determine the induced perturbations based on the gRNA sequence. The CRISPR–Cas protein is either stably expressed in the cells or ectopically introduced as a plasmid, virus, mRNA or protein. The gene-edited cells are challenged with a selective pressure such as drug treatment, viral infection or cell proliferation, such that the cells compete with each other based on the fitness effect of the engineered genetic perturbations. The gRNAs are then counted in the pool of cells retained after the challenge. This is usually done by high-throughput sequencing. Finally, their representation is compared between different challenges or different time points. In the resulting data, depletion of specific gRNAs identifies genes whose disruption sensitizes cells to the challenge, whereas their enrichment identifies genes whose disruption confers a selective advantage.

### Pooled CRISPR screen

A technique in which genetically encoded perturbations are introduced in bulk and read out with sequencing or imaging technology.
In contrast to pooled screens, arrayed CRISPR screens maintain physical separation between perturbations throughout the screen (FIG. 1). As each target gene occupies a separate compartment — for example, different wells on a 96-well plate — arrayed screens tend to be more labour-intensive, costly and limited in scale than pooled screens. Their advantage is that the perturbation a cell receives is predefined by the study design and does not need to be measured explicitly. Therefore, arrayed screens are easier to combine with read-outs that do not involve any sequencing, such as imaging, proteomics and metabolomics profiling.

### Arrayed CRISPR screens

A technique in which perturbations are introduced in individual reaction compartments and remain physically separated.
For reasons of scale and scope, pooled screens are primarily used for discovery, whereas arrayed screens are primarily used for validation and follow-up investigation. Nevertheless, recent technological advances make it possible to obtain detailed biological insights as part of discovery-oriented pooled CRISPR screens. The use of sophisticated models such as organoids and whole organisms, flexible perturbations such as gene activation and repression, diverse biological challenges and data-rich read-outs such as single-cell sequencing and imaging are establishing pooled CRISPR screens as a powerful method for functional biology. Such high-content CRISPR screens provide exciting opportunities to perform mechanistic research at scale.

### High-content CRISPR screens

Screens combining complex models, perturbations and stimuli with data-rich read-outs.
This Primer introduces concepts, practical considerations and applications of CRISPR screens, with a focus on pooled screens and high-content approaches. We describe how a typical CRISPR screen is designed and executed, including the choice and optimization of the model system. We discuss various CRISPR perturbations such as gene knockout, activation and inhibition, and complex read-outs such as single-cell sequencing and imaging. We outline good practices for analysing and interpreting data from CRISPR screens, and review groundbreaking applications of CRISPR screening across a broad range of fields. We also describe how CRISPR screens should be documented to enhance their reproducibility and provide lasting value. Finally, we outline current challenges and future developments in the area of high-content CRISPR screening.

### Experimentation

The experimental design of a typical CRISPR screen comprises four main elements (FIG. 1): the biological model; a method for CRISPR-based perturbation; biological challenges that influence the competition among the perturbed cells; and a read-out that connects the observed biological phenotypes to the gRNAs that induced them. The research question typically defines the selection of the right model and the most relevant biological challenges, and recent advances in CRISPR technology and high-throughput profiling provide flexibility for selecting suitable perturbations and read-outs. This section provides an overview of typical CRISPR screens. In addition, a checklist of considerations when starting a CRISPR screen is shown in BOX 1.

### Conducting a pooled CRISPR screen


### Selection of the biological model.

The first step for a successful CRISPR screen is to select a model system that captures the relevant biological processes and is amenable to genetic screening. Immortalized cell lines provide an inexpensive and easy to handle model for studying biological mechanisms that are adequately represented by simple in vitro cultures. To study more complex and context-dependent biological phenomena, screens can be conducted in primary cells, in tissue explants or in stem-cell-derived cultures including organoids. CRISPR screening is also possible in living animals13, albeit at a smaller scale than is feasible for in vitro screens. For example, screens in mouse models can be performed by editing cells ex vivo and then transplanting them into the organism, or by delivering the gRNAs and the CRISPR–Cas protein into the mice for in vivo editing.
To enhance the efficiency of CRISPR screening, the target cells can be engineered to express the CRISPR–Cas protein. This way, only the gRNAs need to be delivered ectopically during the screen. This separation can also improve safety as no single construct contains both components needed for inducing double-strand breaks. Clones with high and stable Cas9 expression can be preselected14. However, working with just one or a few clones increases the risk of clone-specific artefacts and requires careful validation to ensure that the selected clones are representative and informative for the biological question. For in vivo screens in mice and ex vivo screens in mouse primary cells, transgenic mice can be used that constitutively express Cas9 (REFS15,16) or one of its derivatives17. For human primary cells, viral delivery of the gRNAs can be combined with transfection of a Cas-encoding plasmid, a chemically modified mRNA or the CRISPR–Cas protein itself18.
Careful selection and optimization of the screening model are essential to ensure that the results are broadly relevant to the investigated biological phenomena. It is often advisable to use several variants of the same model — for example, cell lines with different genetic backgrounds — to enhance the relevance and interpretability19,20. Such biological replicates are particularly important because the same perturbation may cause different phenotypic consequences depending on the genetic background21. CRISPR screens should be performed using at least three biological replicates to ob
[...truncated]