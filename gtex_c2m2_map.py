#!/usr/bin/env python

# run this in directory above inputdata and datapackage

import sys
import csv
import datapackage

from pronto import Ontology
from gtex_maps import anatomy_dict, assay_types, edam_types

from tableschema.exceptions import CastError

namespace = 'https://gtexportal.org'
project_namespace = 'https://gtexportal.org'
project_id = 0
collection_id = 'V8'
biobank_collection_id = 'biobank'
histology_collection_id = 'biobank'

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
      open('datapackage/subject_role_taxonomy.tsv', 'w') as role_taxononmy_file:
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
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                                'biosample_id': sample['id'],
                                                'collection_id_namespace': namespace,
                                                'collection_id': histology_collection_id})
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
            sample_in_coll_writer.writerow({'biosample_id_namespace': namespace,
                                                'biosample_id': sample['id'],
                                                'collection_id_namespace': namespace,
                                                'collection_id': biobank_collection_id})
            sample_from_subject_writer.writerow({'biosample_id_namespace': namespace,
                                                     'biosample_id': sample['id'],
                                                     'subject_id_namespace': namespace,
                                                     'subject_id':  row['subjectId']})

        srasamples = {}
        for row in srarunreader:
            sample_id = row['biospecimen_repository_sample_id']
            release_date = row['ReleaseDate']
            if sample_id in srasamples:
                if release_date < srasamples[sample_id]['date']:
                    srasamples[sample_id]['date'] = release_date
            else:
                srasamples[sample_id] = {'date': release_date,
                                             'anatomy': anatomy_dict[row['body_site']],
                                             'assay_type': assay_types[row['Assay Type']]
                                             }
                          
        for sample_id in srasamples:
            release_date = srasamples[sample_id]['date']
            assay_type = srasamples[sample_id]['assay_type']
            anatomy = srasamples[sample_id]['anatomy']
            sample = {'id_namespace': namespace,
                          'id': sample_id,
                          'project_id_namespace': namespace,
                          'project': project_id,
                          'persistent_id': None,
                          'creation_time': release_date,
                          'assay_type': assay_type,
                          'anatomy': anatomy
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
            biospecimen = row['biospecimen_repository_sample_id']
            experiment = row['Experiment']
            file_id = '{sample}/{experiment}'.format(sample = biospecimen,
                                                         experiment = experiment)

            nbytes = '{:.0f}'.format(float(row['Bytes']))
            filerow = {'id_namespace': namespace,
                           'id': file_id,
                           'project_id_namespace': namespace,
                           'project': project_id,
                           'persistent_id': None,
                           'creation_time': row['ReleaseDate'],
                           'size_in_bytes': nbytes,
                           'sha256': None,
                           'md5': None,
                           'filename': None,
                           'file_format': edam_types['file_formats'][row['DATASTORE filetype']],
                           'data_type': edam_types['data_types'][row['Assay Type']]
                           }

            filewriter.writerow(filerow)
            file_in_coll_writer.writerow({'file_id_namespace': namespace,
                                              'file_id': file_id,
                                              'collection_id_namespace': namespace,
                                              'collection_id': collection_id})
            file_describes_subject_writer.writerow({'file_id_namespace': namespace,
                                                        'file_id': file_id,
                                                        'subject_id_namespace': namespace,
                                                        'subject_id': row['submitted_subject_id']})
            file_describes_biosample_writer.writerow({'file_id_namespace': namespace,
                                                          'file_id': file_id,
                                                          'biosample_id_namespace': namespace,
                                                          'biosample_id': biospecimen})

def build_vocabularies():
    edam_onto = Ontology('inputdata/edam.obo')
    # Hacked up Uberon so it will load
    uberon_onto = Ontology('inputdata/human-view.obo')
    obi_onto = Ontology('inputdata/obi.obo')
    
    fieldnames = ['id', 'name', 'description', 'synonyms']
    
    with open('datapackage/data_type.tsv', 'w') as data_type_file:
        data_type_writer = csv.DictWriter(data_type_file,
                                              fieldnames=fieldnames, delimiter='\t')
        data_type_writer.writeheader()
        for v in set(i for i in edam_types['data_types'].values() if i is not None):
            dt_id = 'http://edamontology.org/' + v.replace(':', '_')
            dt_term = edam_onto.get(dt_id)
            dt_name = dt_term.name
            dt_def = dt_term.definition
            syns = ''
            for s in dt_term.synonyms:
                syns += s.description + ''
            if not syns:
                syns = None
            else:
                syns = syns[:-1]

            data_type = {'id': v,
                             'name': dt_name,
                             'description': dt_def,
            # Synonyms in EDAM don't provide references
            #                 'synonyms': syns}
                             'synonyms': None}
            data_type_writer.writerow(data_type) 

    with open('datapackage/file_format.tsv', 'w') as file_format_file:
        file_format_writer = csv.DictWriter(file_format_file,
                                              fieldnames=fieldnames, delimiter='\t')
        file_format_writer.writeheader()
        for v in set(i for i in edam_types['file_formats'].values() if i is not None):
            ff_id = 'http://edamontology.org/' + v.replace(':', '_')
            ff_term = edam_onto.get(ff_id)
            ff_name = ff_term.name
            ff_def = ff_term.definition
            syns = ''
            for s in ff_term.synonyms:
                syns += s.description + '|' 
            if not syns:
                syns = None
            else:
                syns = syns[:-1]
            file_format = {'id': v,
                               'name': ff_name,
                               'description': ff_def,
            # Synonyms in EDAM don't provide references
            #                 'synonyms': syns}
                             'synonyms': None}
            file_format_writer.writerow(file_format)

    with open('datapackage/assay_type.tsv', 'w') as assay_type_file:
        assay_type_writer = csv.DictWriter(assay_type_file,
                                              fieldnames=fieldnames, delimiter='\t')
        assay_type_writer.writeheader()
        for at_id in set(i for i in assay_types.values() if i is not None):
            at_term = obi_onto.get(at_id)
            at_name = at_term.name
            at_def = at_term.definition
            syns = ''
            for s in at_term.synonyms:
                syns += s.description + '|' 
            if not syns:
                syns = None
            else:
                syns = syns[:-1]
            assay_type = {'id': at_id,
                             'name': at_name,
                             'description': at_def,
            # Synonyms semi-broken
            #                 'synonyms': syns}
                             'synonyms': None}
            assay_type_writer.writerow(assay_type) 

    with open('datapackage/anatomy.tsv', 'w') as anatomy_file:
        anatomy_writer = csv.DictWriter(anatomy_file,
                                              fieldnames=fieldnames, delimiter='\t')
        anatomy_writer.writeheader()
        for an_id in set(i for i in anatomy_dict.values() if i is not None):
            an_term = uberon_onto.get(an_id)
            an_name = an_term.name
            an_def = an_term.definition
            syns = ''
            for s in an_term.synonyms:
                syns += s.description + '|' 
            if not syns:
                syns = None
            else:
                syns = syns[:-1]
            anatomy = {'id': an_id,
                             'name': an_name,
                             'description': an_def,
            # Synonyms semi-broken
            #                 'synonyms': syns}
                             'synonyms': None}
            anatomy_writer.writerow(anatomy)

def validate(resource=None):
    
    datapackage.validate('datapackage/gtex-v8-datapackage.json')
    gtex_package = datapackage.DataPackage('datapackage/gtex-v8-datapackage.json', strict=True)
    if resource != 'all':
        r = gtex_package.get_resource(resource)
        print(r.name)
        try:
            t = r.read()
        except CastError as ce:
            print('Hit cast error')
            for err in ce.errors:
                print(err)
            print(ce)
        except Exception as inst:
            print('Hit generic exception')
            print(type(inst))
            print(inst.args)
            print(inst)
    else:
        for r in gtex_package.resources:
            print(r.name)
            try:
                t = r.read()
            except CastError as ce:
                print('Hit cast error')
                print(ce.errors)
                print(ce)
            except Exception as inst:
                print('Hit generic exception')
                print(type(inst))
                print(inst.args)
                print(inst)
            
if __name__ == '__main__':

    if len(sys.argv) == 1:
        sraruntsv = 'inputdata/SraRunTable.tsv' # tab delimited
        histologycsv = 'inputdata/GTExHistology.csv' # comma delimited
        biobanktsv = 'inputdata/biobank_collection_20200527_070347.tsv' # tab delimited
        subject_ids = build_subject_table(sraruntsv)
        build_subject_in_collection_table(subject_ids)
        build_samples(histologycsv, biobanktsv, sraruntsv)
        build_files(sraruntsv)
        build_vocabularies()
        validate('all')
    else:
        validate(sys.argv[1])

