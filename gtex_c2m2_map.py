#!/usr/bin/env python

# run this in directory above inputdata and datapackage

import sys
import csv

from gtex_maps import anatomy_dict, assay_types, edam

namespace = 'https://gtexportal.org'
project_namespace = 'https://gtexportal.org'
project_id = 0
collection_id = 'V8'

def build_subject_table(srarun):
    fieldnames = ['id_namespace', 'id', 'project_id_namespace',
                    'project', 'persistent_id', 'creation_time',
                    'granularity']
    role_taxonomy_fieldnames = ['subject_id_namespace', 'subject_id',
                                    'role_id', 'taxonomy_id']
    
    granularity = 'cfde_subject_granularity:0' # single organism One organism
    role = 'cfde_subject_role:0' # single organism	The organism represented by a subject in the 'single organism' granularity category
    taxonomy_id = 'NCBI:txid9606'
    subjects = set()
    with open(srarun) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:            
            subjects.add(row['submitted_subject_id'])

    with open('datapackage/subject.tsv', 'w') as tsvfile,\
      open('subject_role_taxonomy.tsv', 'w') as role_taxononmy_file:
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        role_taxonomy_writer = csv.DictWriter(role_taxononmy_file,
                                                  fieldnames=role_taxonomy_fieldnames, delimiter='\t')
        role_taxonomy_writer.writeheader()
        for s in subjects:
            subject = {'id_namespace': namespace,
                       'id': s,
                       'project_id_namespace': project_namespace,
                       'project': project_id,
                       'persistent_id': None,
                       'creation_time': None,
                       'granularity': granularity}
            writer.writerow(subject)
            role_taxonomy = {'subject_id_namespace': namespace,
                                 'subject_id': s,
                                 'role_id': role,
                                 'taxonomy_id': taxonomy_id
                                 }
            role_taxonomy_writer.writerow(role_taxonomy)

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

def build_samples(histology, biobank, srarun):
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

    #  
    with open(histology) as histfile, open(biobank) as biobankfile, open(srarun) as srarunfile,\
      open('datapackage/biosample.tsv', 'w') as samplefile,\
      open('datapackage/biosample_in_collection.tsv', 'w') as sample_in_coll_file,\
      open('datapackage/biosample_from_subject.tsv', 'w') as sample_from_subject_file:
        histreader = csv.DictReader(histfile)
        biobankreader = csv.DictReader(biobankfile, delimiter='\t')
        srarunreader = csv.DictReader(srarunfile, delimiter='\t')
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
            sample = {'id_namespace': namespace,
                          'id': row['Tissue Sample ID'],
                          'project_id_namespace': namespace,
                          'project': project_id,
                          'persistent_id': None,
                          'creation_time': None,
                          'assay_type': 'OBI:0600020',
                          'anatomy': anatomy_dict[row['Tissue']]
                          }

            samplewriter.writerow(sample)
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                                'biosample_id': sample['id'],
                                                'collection_id_namespace': namespace,
                                                'collection_id': collection_id})
            sample_from_subject_writer.writerow({'biosample_id_namespace': namespace,
                                                     'biosample_id': sample['id'],
                                                     'subject_id_namespace': namespace,
                                                     'subject_id':  row['Subject ID']})

        for row in biobankreader:
            sample = {'id_namespace': namespace,
                          'id': row['sampleId'],
                          'project_id_namespace': namespace,
                          'project': project_id,
                          'persistent_id': None,
                          'creation_time': None,
                          'assay_type': None,
                          'anatomy': anatomy_dict[row['tissueSiteDetail']]
                          }

            samplewriter.writerow(sample)
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                                'biosample_id': sample['id'],
                                                'collection_id_namespace': namespace,
                                                'collection_id': collection_id})
            sample_from_subject_writer.writerow({'biosample_id_namespace': namespace,
                                                     'biosample_id': sample['id'],
                                                     'subject_id_namespace': namespace,
                                                     'subject_id':  row['subjectId']})

        for row in srarunreader:
            sample = {'id_namespace': namespace,
                          'id': row['biospecimen_repository_sample_id'],
                          'project_id_namespace': namespace,
                          'project': project_id,
                          'persistent_id': None,
                          'creation_time': row['ReleaseDate'],
                          'assay_type': assay_types[row['Assay Type']],
                          'anatomy': anatomy_dict[row['body_site']]
                          }

            samplewriter.writerow(sample)
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                                'biosample_id': sample['id'],
                                                'collection_id_namespace': namespace,
                                                'collection_id': collection_id})
            sample_from_subject_writer.writerow({'biosample_id_namespace': namespace,
                                                     'biosample_id': sample['id'],
                                                     'subject_id_namespace': namespace,
                                                     'subject_id':  row['submitted_subject_id']})

def build_files(srarun):
    file_fieldnames = ['id_namespace', 'id', 'project_id_namespace', 'project',
                           'persistent_id', 'creation_time', 'size_in_bytes',
                           'sha256', 'md5', 'filename', 'file_format', 'data_type']
    file_in_coll_fieldnames = ['file_id_namespace',
                                   'file_id',
                                   'collection_id_namespace',
                                   'collection_id']
    file_describes_subject_fieldnames = ['file_id_namespace',
                                            'file_id',
                                             'subject_id_namespace', 'subject_id']
    file_describes_biosample_fieldnames = ['file_id_namespace', 'file_id',
                                               'biosample_id_namespace',
                                               'biosample_id']

    with open(srarun) as srarunfile,\
      open('datapackage/file.tsv', 'w') as filefile,\
      open('datapackage/file_in_collection.tsv', 'w') as file_in_coll_file,\
      open('datapackage/file_describes_biosample.tsv', 'w') as file_describes_biosample_file,\
      open('datapackage/file_describes_subject.tsv', 'w') as file_describes_subject_file:
        srarunreader = csv.DictReader(srarunfile, delimiter='\t')
        filewriter = csv.DictWriter(filefile,
                                        fieldnames=file_fieldnames,
                                        delimiter='\t')
        filewriter.writeheader()
        file_in_coll_writer = csv.DictWriter(file_in_coll_file,
                                                 fieldnames=file_in_coll_fieldnames,
                                                 delimiter='\t')
        file_in_coll_writer.writeheader()
        file_describes_subject_writer = csv.DictWriter(file_describes_subject_file,
                                                           fieldnames=file_describes_subject_fieldnames,
                                                           delimiter='\t')
        file_describes_subject_writer.writeheader()
        file_describes_biosample_writer = csv.DictWriter(file_describes_biosample_file,
                                                           fieldnames=file_describes_biosample_fieldnames,
                                                           delimiter='\t')
        file_describes_biosample_writer.writeheader()

        for row in srarunreader:
            # not clear how to map to 
            filerow = {'id_namespace': namespace,
                           'id': row['biospecimen_repository_sample_id'],
                           'project_id_namespace': namespace,
                           'project': project_id,
                           'persistent_id': None,
                           'creation_time': row['ReleaseDate'],
                           'size_in_bytes': row['Bytes'],
                           'sha256': None,
                           'md5': None,
                           'filename': None,
                           'file_format': edam['file_formats'][row['DATASTORE filetype']],
                           'data_type': edam['data_types'][row['Assay Type']]
                           }

            filewriter.writerow(filerow)
            file_in_coll_writer.writerow({'file_id_namespace': namespace,
                                              'file_id': filerow['id'],
                                              'collection_id_namespace': namespace,
                                              'collection_id': collection_id})
            file_describes_subject_writer.writerow({'file_id_namespace': namespace,
                                                        'file_id': filerow['id'],
                                                        'subject_id_namespace': namespace,
                                                        'subject_id': row['submitted_subject_id']})
            file_describes_biosample_writer.writerow({'file_id_namespace': namespace,
                                                          'file_id': filerow['id'],
                                                          'biosample_id_namespace': namespace,
                                                          'biosample_id': row['biospecimen_repository_sample_id']})

if __name__ == '__main__':

    sraruntsv = 'inputdata/SraRunTable.tsv' # tab delimited
    histologycsv = 'inputdata/GTExHistology.csv' # comma delimited
    biobanktsv = 'inputdata/biobank_collection_20200527_070347.tsv' # tab delimited
    subject_ids = build_subject_table(sraruntsv)
    build_subject_in_collection_table(subject_ids)
    build_samples(histologycsv, biobanktsv, sraruntsv)
    build_files(sraruntsv)
