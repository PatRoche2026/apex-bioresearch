# Modality Selection Guide: A CTO's Decision Framework

## Decision Tree for Modality Selection
The choice of therapeutic modality is one of the most consequential decisions in drug development. The wrong modality can doom a program regardless of target quality.

### Small Molecules (MW < 500 Da)
**Best for**: Intracellular targets with defined binding pockets, enzymes, GPCRs, ion channels, nuclear receptors.
**Advantages**: Oral bioavailability, tissue penetration (including CNS), low COGS, established manufacturing.
**Limitations**: Requires a defined binding pocket (rule of 5 compliance), selectivity challenges for target families with conserved active sites (kinases, proteases).
**Key question**: Is there a tractable binding site? Check crystal structures, AlphaFold predictions, and prior medicinal chemistry efforts on the target family.

### Monoclonal Antibodies (mAbs)
**Best for**: Extracellular targets — membrane receptors, secreted ligands, cell surface antigens.
**Advantages**: High specificity, long half-life (2-4 weeks), well-understood manufacturing platform.
**Limitations**: Cannot access intracellular targets, IV/SC administration only, immunogenicity risk, high COGS (~$100-300/g), cold chain requirements.
**Key question**: Is the target extracellular and accessible? What is the required tissue penetration?

### Bispecific Antibodies
**Best for**: Engaging two targets simultaneously (e.g., T-cell redirectors like CD3×target), bridging mechanisms.
**Advantages**: Novel mechanisms not achievable with monospecifics, potential for enhanced efficacy.
**Limitations**: Complex manufacturing, stability challenges, cytokine release syndrome risk for T-cell engagers.

### Antibody-Drug Conjugates (ADCs)
**Best for**: Targeted delivery of cytotoxic payloads to tumor cells expressing a surface antigen.
**Advantages**: Combines antibody targeting with small molecule potency, expanding to non-oncology.
**Limitations**: Complex linker chemistry, bystander toxicity, resistance via antigen downregulation, high manufacturing complexity.

### RNA Therapeutics (siRNA, ASO, mRNA)
**Best for**: "Undruggable" targets — transcription factors, scaffolding proteins, targets without enzymatic activity.
**Advantages**: Can silence any gene with known sequence, rapid target switching, platform scalability.
**Limitations**: Delivery challenge (liver-centric for LNP, conjugate-dependent for other tissues), durability, manufacturing scale for LNP formulations.
**Key question**: What tissue needs to be reached? Liver delivery is solved (GalNAc conjugates, LNP). CNS, muscle, and lung delivery remain challenging.

### Gene Therapy (AAV, lentiviral)
**Best for**: Monogenic diseases with clear loss-of-function genetics, one-time correction.
**Advantages**: Potentially curative, one-time treatment.
**Limitations**: Immunogenicity to viral capsids, limited payload size (AAV ~4.7kb), redosing challenges, high manufacturing cost ($1-2M per dose), durability questions.

## Manufacturing Considerations
- Small molecules: Established, scalable, low cost. Chemical synthesis well understood.
- Biologics (mAbs): CHO cell culture, complex purification. ~18 month timeline to clinical material.
- RNA therapeutics: Enzymatic synthesis or in vitro transcription. LNP formulation adds complexity.
- Gene therapy: Viral vector production is a major bottleneck. Yields are low, costs are high.

## Red Flags for Technical Feasibility
- No structural data (crystal structure, cryo-EM, or AlphaFold) for the target
- Target family has a history of selectivity failures (e.g., broad-spectrum kinase inhibitors)
- Required tissue penetration that the modality cannot achieve (e.g., mAb for CNS target)
- No precedent for the modality in the target class
- Manufacturing process not scalable for the required dose/frequency
