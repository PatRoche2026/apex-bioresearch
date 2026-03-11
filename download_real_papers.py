"""Download real PMC full-text papers to replace synthetic knowledge base documents.

Each role gets papers matching their domain expertise:
- CSO: target validation, genetics, functional genomics
- CTO: druggability, modality selection, drug delivery
- CMO: clinical trial design, regulatory strategy, biomarkers
- CBO: biotech market analysis, IP strategy, competitive landscape
- shared: drug discovery pipeline, general biotech

Usage:
    python download_real_papers.py          # Download + write to knowledge/
    python download_real_papers.py --ingest  # Also re-ingest into ChromaDB
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from Bio import Entrez, Medline

# Reuse project config
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents import ENTREZ_EMAIL, PUBMED_RATE_LIMIT_DELAY
from agents.tools import _pmids_to_pmc_ids, _fetch_pmc_full_text

Entrez.email = ENTREZ_EMAIL

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"

# ---------------------------------------------------------------------------
# Papers to download — curated PubMed queries per role
# ---------------------------------------------------------------------------

ROLE_QUERIES: dict[str, list[dict]] = {
    "cso": [
        {
            "query": "genetic evidence drug target validation GWAS Mendelian randomization",
            "label": "genetic_target_validation",
            "max_results": 5,
        },
        {
            "query": "CRISPR functional genomics drug target discovery",
            "label": "crispr_target_discovery",
            "max_results": 5,
        },
        {
            "query": "convergent evidence target biology mechanism of action",
            "label": "convergent_evidence_moa",
            "max_results": 5,
        },
    ],
    "cto": [
        {
            "query": "druggability assessment protein target small molecule antibody",
            "label": "druggability_assessment",
            "max_results": 5,
        },
        {
            "query": "RNA therapeutics delivery CNS blood brain barrier",
            "label": "rna_therapeutics_delivery",
            "max_results": 5,
        },
        {
            "query": "antibody drug conjugate ADC linker payload design",
            "label": "adc_design",
            "max_results": 5,
        },
    ],
    "cmo": [
        {
            "query": "adaptive clinical trial design biomarker-driven oncology",
            "label": "adaptive_trial_design",
            "max_results": 5,
        },
        {
            "query": "FDA accelerated approval surrogate endpoint breakthrough therapy",
            "label": "regulatory_strategy",
            "max_results": 5,
        },
        {
            "query": "patient stratification companion diagnostic clinical development",
            "label": "patient_stratification",
            "max_results": 5,
        },
    ],
    "cbo": [
        {
            "query": "biotech venture capital investment thesis portfolio strategy",
            "label": "biotech_investment",
            "max_results": 5,
        },
        {
            "query": "pharmaceutical licensing deal structure partnership biotech",
            "label": "pharma_licensing",
            "max_results": 5,
        },
        {
            "query": "drug pricing reimbursement market access rare disease orphan",
            "label": "pricing_market_access",
            "max_results": 5,
        },
    ],
    "shared": [
        {
            "query": "drug discovery pipeline target to IND preclinical development",
            "label": "drug_discovery_pipeline",
            "max_results": 5,
        },
        {
            "query": "oncostatin M OSMR inflammatory bowel disease therapeutic",
            "label": "osmr_ibd",
            "max_results": 5,
        },
    ],
}


def search_pubmed(query: str, max_results: int = 5) -> list[dict]:
    """Search PubMed and return structured results."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    time.sleep(PUBMED_RATE_LIMIT_DELAY)

    id_list = record.get("IdList", [])
    if not id_list:
        return []

    handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="medline", retmode="text")
    records = list(Medline.parse(handle))
    handle.close()
    time.sleep(PUBMED_RATE_LIMIT_DELAY)

    results = []
    for rec in records:
        authors = rec.get("AU", [])
        results.append({
            "pmid": rec.get("PMID", ""),
            "title": rec.get("TI", ""),
            "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
            "journal": rec.get("JT", rec.get("TA", "")),
            "year": rec.get("DP", "").split()[0] if rec.get("DP") else "",
            "abstract": rec.get("AB", "No abstract available."),
        })
    return results


def download_papers_for_role(role: str) -> list[dict]:
    """Download papers for a role. Returns list of paper dicts with full_text if available."""
    queries = ROLE_QUERIES[role]
    all_papers: list[dict] = []
    seen_pmids: set[str] = set()

    for q in queries:
        print(f"  Searching: {q['query'][:60]}...")
        papers = search_pubmed(q["query"], q["max_results"])
        for p in papers:
            if p["pmid"] and p["pmid"] not in seen_pmids:
                seen_pmids.add(p["pmid"])
                p["search_label"] = q["label"]
                all_papers.append(p)

    # Look up PMC IDs for full text
    pmids = [p["pmid"] for p in all_papers]
    print(f"  Looking up PMC IDs for {len(pmids)} papers...")
    pmc_map = _pmids_to_pmc_ids(pmids)
    print(f"  Found {len(pmc_map)} papers with PMC full text")

    # Fetch full text where available
    full_text_count = 0
    for p in all_papers:
        pmc_id = pmc_map.get(p["pmid"])
        if pmc_id:
            print(f"    Fetching PMC{pmc_id} (PMID {p['pmid']})...")
            full_text = _fetch_pmc_full_text(pmc_id, max_chars=8000)
            if full_text:
                p["full_text"] = full_text
                p["pmc_id"] = pmc_id
                full_text_count += 1
                time.sleep(PUBMED_RATE_LIMIT_DELAY)

    print(f"  Total: {len(all_papers)} papers, {full_text_count} with full text")
    return all_papers


def write_papers_to_knowledge(role: str, papers: list[dict]) -> int:
    """Write downloaded papers as .md files in the knowledge directory."""
    role_dir = KNOWLEDGE_DIR / role
    role_dir.mkdir(parents=True, exist_ok=True)

    # Remove old synthetic files
    for old_file in role_dir.glob("*.md"):
        old_file.unlink()
        print(f"  Removed old: {old_file.name}")

    files_written = 0
    for p in papers:
        pmid = p["pmid"]
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in p["title"])[:80].strip()
        filename = f"PMID{pmid}_{safe_title}.md"

        lines = [
            f"# {p['title']}",
            "",
            f"**PMID:** {pmid}",
            f"**Journal:** {p['journal']} ({p['year']})",
            f"**Authors:** {p['authors']}",
        ]

        if p.get("pmc_id"):
            lines.append(f"**PMC:** PMC{p['pmc_id']}")

        lines.append(f"**Search context:** {p.get('search_label', 'general')}")
        lines.append("")

        if p.get("full_text"):
            lines.append("## Full Text")
            lines.append("")
            lines.append(p["full_text"])
        else:
            lines.append("## Abstract")
            lines.append("")
            lines.append(p["abstract"])

        filepath = role_dir / filename
        filepath.write_text("\n".join(lines), encoding="utf-8")
        files_written += 1

    return files_written


def main():
    do_ingest = "--ingest" in sys.argv

    print("=" * 60)
    print("APEX Knowledge Base — Downloading Real PMC Papers")
    print("=" * 60)

    total_papers = 0
    total_files = 0

    for role in ROLE_QUERIES:
        print(f"\n{'-'*40}")
        print(f"Role: {role.upper()}")
        print(f"{'-'*40}")

        papers = download_papers_for_role(role)
        n_files = write_papers_to_knowledge(role, papers)

        total_papers += len(papers)
        total_files += n_files
        print(f"  Wrote {n_files} files to knowledge/{role}/")

    print(f"\n{'='*60}")
    print(f"DONE: {total_papers} papers downloaded, {total_files} files written")
    print(f"{'='*60}")

    if do_ingest:
        print("\nRe-ingesting into ChromaDB (--ingest flag)...")
        from rag.ingest import ingest_all
        ingest_all(force=True)
    else:
        print("\nTo ingest into ChromaDB, run:")
        print("  python download_real_papers.py --ingest")
        print("  # or: python -m rag.ingest --force")


if __name__ == "__main__":
    main()
