---
pdf_options:
  format: Letter
---

# MoTrPAC ETL Recipe

## Start with Minimal Tables

1. Namespace
2. Project one single project
3. Collection (skip for now)
4. Make these tables
 * Subject
 * File
 * Biosample
5. Link the Subject, File, Biosample
 * `file_describes_biosample.tsv`
 * `file_describes_subject.tsv`
 * `biosample_from_subject.tsv`

* Don't worry about external vocabulary tables, just get the term in the "noun" tables.
(E.g., file_format.tsv or anatomy.tsv)

Install CFDE Client
`cfde run <datapackage dir>`
`cfde status`

Contact Jonathon Gaff if you need help with the flow.

## Vocabularies

* both tables project_id_namespace needs to be provided. It's a compound key with project.
* biosample
 - assay_type terms come from OBI, http://www.ontobee.org/ontology/OBI
  + epigenomics OBI:0002020 http://purl.obolibrary.org/obo/OBI_0002020
  + transcriptomics is this RNA-seq or a microarry?
 - anatomy comes from UBERON https://www.ebi.ac.uk/ols/ontologies/uberon
  + Gastrocnemius UBERON:0001388 http://purl.obolibrary.org/obo/UBERON_0001388
  + White Adipose UBERON:0001347 http://purl.obolibrary.org/obo/UBERON_0001347
  + Heart UBERON:0000948 http://purl.obolibrary.org/obo/UBERON_0000948
  + Liver UBERON:0002107 http://purl.obolibrary.org/obo/UBERON_0002107
  + PaxGene Whole Blood? UBERON:0013756 http://purl.obolibrary.org/obo/UBERON_0013756
* subject
 - granularity needs to be one of items from subject_granularity.tsv
  + probably cfde_subject_granularity:0, single organism
