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

