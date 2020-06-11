#!/usr/bin/env python

# run this in directory above inputdata and datapackage

import sys
import csv
import datapackage
from tableschema.exceptions import CastError

def validate(dpackage, resource='all'):
    
    datapackage.validate(dpackage)
    gtex_package = datapackage.DataPackage(dpackage, strict=True)
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

    if len(sys.argv) == 2:
        validate(sys.argv[1], 'all')
    else:
        validate(sys.argv[1], sys.argv[2])

