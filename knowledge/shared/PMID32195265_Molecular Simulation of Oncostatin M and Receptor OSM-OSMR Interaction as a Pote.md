# Molecular Simulation of Oncostatin M and Receptor (OSM-OSMR) Interaction as a Potential Therapeutic Target for Inflammatory Bowel Disease.

**PMID:** 32195265
**Journal:** Frontiers in molecular biosciences (2020)
**Authors:** Du Q, Qian Y, Xue W
**PMC:** PMC7064634
**Search context:** osmr_ibd

## Full Text


### Introduction

Inflammatory bowel diseases (IBDs) are complex chronic inflammatory conditions of the gastrointestinal tract that are driven by perturbed signal pathways of cytokines such as tumor necrosis factor (TNF)-α and IL-6 (Neurath, 2014). Nowadays, anti-TNF antibodies (such as infliximab and golimumab) are mainstay therapies for IBD (Choi et al., 2017). However, there are still more than 40% of patients who are non-responsive to anti-TNF agents, making the discovery of alternative therapeutic targets a priority (Kim et al., 2017). One of those potential targets, oncostatin M (OSM)-mediated inflammation, has gained a lot of interest (Verstockt et al., 2019). It is found that high pretreatment expression of OSM is strongly associated with failure of anti-TNF therapy of patients with IBD, which revealed the role of the receptor (OSMR) as part of a unique pathway that contributes to the chronicity of intestinal inflammation (West et al., 2017).
OSM belongs to the IL-6 family, and the activation of the OSM signal pathway is highly determined by the high affinity of OSM to the receptor (OSMR) (Adrian-Segarra et al., 2018a,b). The crystal structure of OSM reveals that the protein comprises four α helices ranging from 15 to 22 amino acids in length (termed A, B, C, and D) and linked by polypeptide loops (Figure 1A) (Deller et al., 2000). The OSMR is a member of the IL-6 receptor family that transduces signaling events of OSM (Yu et al., 2019). Currently, available antibodies, such as GSK315234 and GSK2330811, have already been proven to affect the OSM signal (Verstockt et al., 2019). Although neutralizing OSM antibodies are being developed and should be considered as a novel proof-of-concept trial in IBD patients (West et al., 2017), these developed biological medicines are large, complex, and relatively fragile molecules, which make them difficult and expensive to produce and administer on a large scale (Monaco et al., 2015).
(A) Structure of oncostatin M (OSM); the modeled fragments are colored in red. (B) Sequence alignment between oncostatin M receptor (OSMR) and leukemia inhibitory factor receptor (LIFR). (C) Structural alignment of OSMR homology model (red) and LIFR crystal structure (green). (D) Docking funnel of OSM and OSMR. Inset: the top scoring conformation as near-native OSM–OSMR structure.
In recent years, development of small molecule modulators targeting protein–protein interactions (PPIs) has emerged as a promising therapeutic intervention in complex diseases (Nero et al., 2014; Nim et al., 2016; Weng et al., 2019). In selecting biologically relevant protein–protein interfaces, the availability of computer-aided drug design (CADD) approach has led to the discovery of small molecules either stabilizing or disrupting the biological processes (Arkin et al., 2014; Laraia et al., 2015). The critical role for OSM in antipathogen immunity has not been described, and targeting OSM–OSMR may offer inhibition of the inflammatory pathology while preserving protective immunity (Verstockt et al., 2019). These hypotheses stimulate the idea of identification of small molecular inhibitors against the OSM–OSMR interface, which might provide safer and more broadly effective alternatives to conventional antibodies targeting monomeric macromolecules. To discover ligands specifically disrupting the OSM–OSMR interface, the information of the protein–protein interactions is needed. Unfortunately, the 3D structure of the OSM–OSMR complex remains elusive (Kim et al., 2017). It is of paramount importance to understand the details of the OSM and OSMR complex formation as well as the potential binding site between the protein–protein interface.
In this work, molecular simulation approaches aimed at filling the aforementioned gap were performed to accelerate the discovery of small molecules targeting OSM–OSMR. Starting from the crystal structure of OSM (Deller et al., 2000) and the model of the OSMR [a protein-binding region was built using the leukemia inhibitory factor receptor (LIFR) crystal structure (Huyton et al., 2007) as a template], the near-native conformation of the OSM–OSMR complex was obtained through protein–protein docking. The docking conformation was further sampled through long-time scale (1 μs) molecular dynamics (MD) simulation to get the equilibrated binding states. Based on the simulation trajectory, per-residue binding free energy decomposition (Tu et al., 2018; Wang et al., 2019) and computational alanine scanning (CAS) (Huo et al., 2002) analysis were carried out to identify the protein–protein interface “hotspots.” Using one of the identified “hotspots” (Arg100) as an example, an additional 500 ns of MD simulation was performed to investigate the stability of the R100A mutant complex. Finally, the “hotspots” were mapped to the seven binding sites located at the OSM–OSMR interface detected using FTMap (Kozakov et al., 2011), and three of them were suggested as important target sites for future designs of small molecular modulators in the OSM–OSMR interaction.

### Materials and Methods


### Structure Preparation


### Construction of OSM Missing Loop

The crystal structure and sequence of OSM were obtained from the PDB database (PDB code: 1EVS) (Deller et al., 2000). Residues from 1 to 3 and 135 to 155 (highlighted in red color in Table S1) were missing in the resolved crystal structure. The coordinates of the missing fragments of the OSM structure were constructed using the optimization-based approach (Fiser et al., 2000) in Modeler (Webb and Sali, 2016).

### Homology Modeling of OSMR

The full-length sequence of the OSMR was obtained from the NCBI database (GenBank: AAI25210.1) (Strausberg et al., 2002). Then the sequence of the OSMR was submitted to search a template structure with the BLAST algorithm (Schaffer et al., 2001). Searching result showed that the sequence identity between the OSMR and LIFR was higher than 30%, especially in the protein-binding domain (57%). Therefore, based on the crystal structure (PDB code: 2Q7N) (Huyton et al., 2007) of the LIFR (residues from 201 to 383), 10 homology models of the OSMR protein-binding domain was constructed using Modeler (Webb and Sali, 2016).

### Protein–Protein Docking

OSM–OSMR docking was performed using the protein docking module of the latest version of Rosetta (Alford et al., 2017). Before docking, the PDB structures of OSM and OSMR were first formed through the script of clean_pdb.py. The formed structures of the two proteins were refined by running the Rosetta relax protocol, and the PDB files consisting of refined OSM and OSMR were generated. Then, according to the knowledge of the residues of OSM for OSMR binding detected by site mutagenesis studies (Adrian-Segarra et al., 2018b), the generated two complexes were loaded into PyMOL (Schrödinger, 2010) and with OSM reoriented to contact with the OSMR. To ensure low-energy starting side-chain conformations for docking, further prepacking of the OSM and OSMR complexes were conducted. Finally, 10,000 poses were calculated for the OSM–OSMR interactions using the Monte Carlo (MC) refinement method (Gray et al., 2003), with the pre-packed conformation as a starting point.

### Docking Funnel Analysis

With InterfaceAnalyzer mover in RosettaScripts (Fleishman et al., 2011), the RMSD was calculated from the heavy atoms of the interface residues (Table S2) using each pose of the top five scorers as a reference structure (Chaudhury et al., 2011). The docking funnel was then identified through plotting total_score against RMSD. Finally, the top scoring structure with the lowest RMSD was selected as the successful pose of the OSM–OSMR complex.

### Molecular Dynamics Simulation

Molecular dynamics (MD) simulation was performed with GPU-accelerated PMEMD in AMBER14 (Babin et al., 2014). The selected near-native structure of OSM–OSMR from Rosetta docking was used as the initial conformation for MD simulation. The LEaP (Wang et al., 2
[...truncated]