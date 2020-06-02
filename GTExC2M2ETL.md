---
pdf_options:
  format: Letter
---

# To Do

## Tables

- [ ] `file`
- [ ] `biosample`
- [ ] `subject`
- [ ] `project`
- [ ] `project_in_project`
- [ ] `collection`
- [ ] `collection_in_collection`
- [ ] `file_in_collection`
- [ ] `biosample_in_collection`
- [ ] `subject_in_collection`
- [ ] `file_describes_biosample`
- [ ] `file_describes_subject`
- [ ] `biosample_from_subject`
- [ ] `subject_role_taxonomy`
- [ ] `assay_type`
- [ ] `ncbi_taxonomy`
- [ ] `anatomy`
- [ ] `file_format`
- [ ] `data_type`
- [ ] `subject_role`
- [ ] `subject_granularity`
- [ ] `id_namespace`


# GTEx V8 C2M2 Level 1 ETL Process

Notes on getting the GTEx V8 data release into the Level 1 C2M2.

## Things (Proper Nouns)

The Level 1 C2M2 includes tables to describe the following things (entities), and the relationships between them.

 * Namespaces
 * Project
 * Collection
 * Subject
 * Biosample
 * File

## Data Sources

Release Information
https://gtexportal.org/home/releaseInfoPage

SRA Run Table
https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=phs000424&o=biospecimen_repository_sample_id_sam_s%3Aa%3Bacc_s%3Aa

UBERON Terms
https://gtexportal.org/home/samplingSitePage

Histology
https://gtexportal.org/home/histologyPage

## Namespace and Project

We defined a single namespace for all of the GTEx things. For this
first draft, we also defined a single project. For the persistent
identifier of the project, we used the dbGaP accession number linked
from the GTEx Portal, since it it resolves using `identifiers.org`:
`https://identifiers.org/dbgap:phs000424.v2.p1`.

## Collections

We also defined several collections, all associated with the GTEx
project.

 * A single collection for the V8 data release, using its specific accession
number as the persistent ID: `https://identifiers.org/dbgap:phs000424.v8.p2`.


Collection for Biobank

biobank_collection_20200528_070345.txt

Add collection for histology samples

## Subject

For the subject table, our primary goal was to find the unique name
GTEx uses for each. We pulled this from the `submitted_subject_id`
column of the SRA run table, e.g., `GTEX-12WSA`.

## Biosample

The list of biosamples comes from the histology table, Biobank, and
the SRA run table.

And assuming I’m following, the assay type should be one of these? http://www.ontobee.org/ontology/catalog/OBI?iri=http://purl.obolibrary.org/obo/OBI_0000070





12:11
and the closest I see are ‘sequencing assay’ http://www.ontobee.org/ontology/OBI?iri=http://purl.obolibrary.org/obo/OBI_0600047 and ‘histolological assay’ http://www.ontobee.org/ontology/OBI?iri=http://purl.obolibrary.org/obo/OBI_0600020

### File

 * **file_format** An EDAM CV term ID identifying the digital format of this file (e.g. TSV or FASTQ)
 * **data_type** An EDAM CV term ID identifying the type of information stored in this file (e.g. RNA sequence reads)


## Relationships

### Subject Role and Taxonomy

I'm not sure what this is all about.

A table linking a subject, a subject_role (a named organism-level constituent component of a subject, like 'host', 'pathogen', 'endosymbiont', 'taxon detected inside a microbiome subject', etc.) and a taxonomic label (which is hereby assigned to this particular subject_role within this particular subject)".

#### Attributes

 * **subject**
   - **namespace** The namespaec of the subject
   - **id** The ID of this subject
 * **role** The role assigned to this organism-level constituent component of this subject (see Subject Role under Controlled Vocabularies). One of
   - single organism
   - host
   - symbiont
   - pathogen
   - microbiome taxon
   - cell line ancestor
   - synthetic
 * **taxonomy_id** An NCBI Taxonomy Database ID identifying this taxon


## Thoughts 5/27/20

https://gtexportal.org/home/releaseInfoPage

https://gtexportal.org/home/histologyPage (click csv to
download)

Many subjects

54 tissue types, from most or all subjects
biosamples = tissue types X subjects

several different file types possible per biosample


One GTEx project
 * entities declare their membership in GTEx

Once v8 collection
 * Gathers all v8 data

### Questions
    Creation date for subject records? ReleaseDate?


And assuming I’m following, the assay type should be one of these? http://www.ontobee.org/ontology/catalog/OBI?iri=http://purl.obolibrary.org/obo/OBI_0000070


12:11
and the closest I see are ‘sequencing assay’ http://www.ontobee.org/ontology/OBI?iri=http://purl.obolibrary.org/obo/OBI_0600047 and ‘histolological assay’ http://www.ontobee.org/ontology/OBI?iri=http://purl.obolibrary.org/obo/OBI_0600020
12:11
unless we’re allowed to use sub-types of those?

