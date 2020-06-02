#!/usr/bin/env python

# run this in directory above inputdata and datapackage

import sys
import csv

from anatomy_map import anatomy_dict

namespace = 'https://gtexportal.org'
project_namespace = 'https://gtexportal.org'
project_id = 0
collection_id = 'V8'

def build_subject_table(srarun):
    fieldnames = ['id_namespace', 'id', 'project_id_namespace',
                    'project', 'persistent_id', 'creation_time',
                    'granularity']
    granularity = 'cfde_subject_granularity:0' # single organism One organism        
    subjects = set()
    with open(srarun) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:            
            subjects.add(row['submitted_subject_id'])

    with open('datapackage/subject.tsv', 'w') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for s in subjects:
            subject = {'id_namespace': namespace,
                       'id': s,
                       'project_id_namespace': project_namespace,
                       'project': project_id,
                       'persistent_id': None,
                       'creation_time': None,
                       'granularity': granularity}
            writer.writerow(subject)
    return subjects

def build_subject_in_collection_table(subjects):
    fieldnames = ['subject_id_namespace',
                      'subject_id',
                      'collection_id_namespace',
                      'collection_id']
    with open('datapackage/subject_in_collection.tsv', 'w') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for s in subjects:
            subject = {'subject_id_namespace': namespace,
                       'subject_id': s,
                       'collection_id_namespace': namespace,
                       'collection_id': collection_id}
            writer.writerow(subject)

def add_histology_biobank_samples_table(histology, biobank):
    sample_fieldnames = ['id_namespace', 'id', 'project_id_namespace',
                    'project', 'persistent_id', 'creation_time',
                    'assay_type', 'anatomy']
    sample_in_coll_fieldnames = ['biosample_id_namespace',
                                     'biosample_id',
                                     'collection_id_namespace',
                                     'collection_id']
    sample_from_subject_fieldnames = ['biosample_id_namespace',
                                          'biosample_id',
                                          'subject_id_namespace', 'subject_id']

    #    biospecimen_repository_sample_id
    with open(histology) as histfile, open('datapackage/biosample.tsv', 'w') as samplefile,\
      open('datapackage/biosample_in_collection.tsv', 'w') as sample_in_coll_file,\
      open('datapackage/biosample_from_subject.tsv', 'w') as sample_from_subject_file:
        histreader = csv.DictReader(histfile)
        samplewriter = csv.DictWriter(samplefile,
                                          fieldnames=sample_fieldnames,
                                          delimiter='\t')
        samplewriter.writeheader()
        sample_in_coll_writer = csv.DictWriter(sample_in_coll_file,
                                                fieldnames=sample_in_coll_fieldnames,
                                                delimiter='\t')
        sample_in_coll_writer.writeheader()
        sample_from_subject_writer = csv.DictWriter(sample_from_subject_file,
                                                fieldnames=sample_from_subject_fieldnames,
                                                delimiter='\t')
        sample_from_subject_writer.writeheader()

        for row in histreader:
            # ID, anatomy, subject
            # "Tissue Sample ID","Tissue","Subject ID"
            sample = {'id_namespace': namespace,
                          'id': row['Tissue Sample ID'],
                          'project_id_namespace': namespace,
                          'project': project_id,
                          'persistent_id': None,
                          'creation_time': None,
                          'assay_type': None,
                          'anatomy': anatomy_dict[row['Tissue']]
                          }

            samplewriter.writerow(sample)
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                     'biosample_id': sample['id'],
                                     'collection_id_namespace': namespace,
                                     'collection_id': collection_id})
            sample_from_subject_writer.writerow({'biosample_id_namespace': namespace,
                                     'biosample_id': row['Tissue Sample ID'],
                                     'subject_id_namespace': namespace,
                                     'subject_id':  row['Subject ID']})

if __name__ == '__main__':

    sraruntsv = 'inputdata/SraRunTable.tsv' # tab delimited
    histologycsv = 'inputdata/GTExHistology.csv' # comma delimited
    biobanktsv = 'inputdata/biobank_collection_20200527_070347.tsv' # tab delimited
    subject_ids = build_subject_table(sraruntsv)
    build_subject_in_collection_table(subject_ids)
    add_histology_biobank_samples_table(histologycsv, biobanktsv)

    # when adding samples from SRA run table, watch for duplicates
