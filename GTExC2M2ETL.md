---
pdf_options:
  format: Letter
---

# To Do

Vocabulary tables should not be part of the DCC work

## Tables

- [X] `file`
- [X] `biosample`
- [X] `subject`
- [X] `project`
- [X] `project_in_project`
- [X] `collection`
- [X] `collection_in_collection`
- [X] `file_in_collection`
- [X] `biosample_in_collection`
- [X] `subject_in_collection`
- [X] `file_describes_biosample`
- [X] `file_describes_subject`
- [X] `biosample_from_subject`
- [X] `subject_role_taxonomy`
- [ ] `assay_type`
- [X] `ncbi_taxonomy`
- [ ] `anatomy`
- [ ] `file_format`
- [ ] `data_type`
- [X] `subject_role`
- [X] `subject_granularity`
- [X] `id_namespace`


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


## Validate

```
import datapackage
datapackage.Package("datapackage.json", strict=True)
datapackage.Package(datapackage_json_contents, strict=True)

import tableschema
tableschema.validate(datapackage_json_contents)


lincs_datapackage_json = json.loads(dpackage_json)
lincs_datapackage = datapackage.Package(lincs_datapackage_json, strict=True)
>>> for resource in lincs_datapackage['resources']:
...     print(resource['profile'])
...     print(resource['name'])
...     tableschema.validate(resource['schema'])
```

```


import datapackage
package = datapackage.DataPackage('gtex-v8-datapackage.json')
anatomy = package.get_resource('anatomy')
anatomy.descriptor
from tableschema import Table
table = Table('anatomy.tsv', schema=anatomy.descriptor)

import datapackage
package = datapackage.DataPackage('datapackage/gtex-v8-datapackage.json')
anatomy = package.get_resource('anatomy')
from tableschema import Table
table = Table('anatomy.tsv', schema=anatomy.descriptor)
from sqlalchemy import create_engine
engine = create_engine('sqlite://')
table = Table('datapackage/anatomy.tsv', schema=anatomy.descriptor)
anatomy.table.save('data', storage='sql', engine=engine)

# Load order
datapackage/id_namespace.tsv
datapackage/subject_role.tsv
datapackage/subject_granularity.tsv
datapackage/anatomy.tsv
datapackage/assay_type.tsv
datapackage/file_format.tsv
datapackage/data_type.tsv
datapackage/ncbi_taxonomy.tsv
datapackage/project.tsv
datapackage/project_in_project.tsv
datapackage/collection.tsv
datapackage/collection_defined_by_project.tsv
datapackage/collection_in_collection.tsv
datapackage/subject.tsv
datapackage/biosample.tsv
datapackage/file.tsv
datapackage/biosample_from_subject.tsv
datapackage/biosample_in_collection.tsv
datapackage/file_describes_biosample.tsv
datapackage/file_describes_subject.tsv
datapackage/file_in_collection.tsv
datapackage/subject_in_collection.tsv
datapackage/subject_role_taxonomy.tsv
```
