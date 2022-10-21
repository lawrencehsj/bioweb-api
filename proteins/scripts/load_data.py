import os
import sys
import django
import csv
from collections import defaultdict
from django.db.models import Q

# RELATIVE PATH for app
sys.path.append(os.path.realpath('..'))
# sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb.settings')
django.setup()

from proteins.models import *

# RELATIVE PATH for csv files
protein_sequence_file = '../assignment_data_sequences.csv'
protein_file = '../assignment_data_set.csv'
pfam_file = '../pfam_descriptions.csv'

# class variables for caching data
# key:value pair for easy access to certain values depending on matching keys
protein_sequence = defaultdict(dict) #key value pair
taxonomy = defaultdict(list)
domains = defaultdict(list)
protein = defaultdict(list)
# dict to contain created model objects for appending
protein_sequence_rows={}
pfam_rows={}
taxonomy_rows={}

# clear database before insertion
Sequence.objects.all().delete()
Taxonomy.objects.all().delete()
Pfam.objects.all().delete()
Domains.objects.all().delete()
Protein.objects.all().delete()
ProteinDomainLink.objects.all().delete()

# protein_sequence | protein_id
with open(protein_sequence_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        protein_sequence[row[0]] = row[1]
        # directly adding to Sequence model
        add = Sequence.objects.create(protein_id=row[0], sequence=row[1])
        add.save()
        protein_sequence_rows[row[0]] = add # save for access later 

# pfam | pfam_id
with open(pfam_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        # directly adding to Pfam model
        add = Pfam.objects.create(domain_id=row[0], domain_description=row[1])
        add.save()
        pfam_rows[row[0]] = add # save for access later 
        
# protein details
with open(protein_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        # retrieve genus and species by splitting
        genus_species = row[3].split(' ', 1)
        # if already exist in taxonomy, then will not create a new entry
        if row[1] not in taxonomy:
            taxonomy[row[1]] = {"taxa_id": row[1], "clade": row[2], "genus": genus_species[0], "species": genus_species[1]}
       
        # there might be multiple domains per protein_id
        # append multiple domains to a single protein_id key (handling many-to-many)
        domains[row[0]].append({"pfam_id": row[5], "description": row[4], "start": row[6], "stop": row[7]})
       
        # in the dataset csv, there are rows of recurring proteins with different domain data
        # if there is no pre-existing match for the given protein_id, create a new entry.
        # otherwise, append multiple domains details to a single protein_id (handling many-to-many)
        if row[0] not in protein:
            protein[row[0]] = {"pfam_id": [row[5]], "description": row[4], "taxa_id": row[1], "length": row[8], "start": [row[6]], "stop": [row[7]]}
        else:
            protein[row[0]]["pfam_id"].append(row[5])
            protein[row[0]]["start"].append(row[6])
            protein[row[0]]["stop"].append(row[7])

# create Taxonomy objects 
for taxa_id, data in taxonomy.items():
    row = Taxonomy.objects.create(taxa_id=data["taxa_id"], clade=data["clade"], genus=data["genus"], species=data["species"])
    row.save()
    taxonomy_rows[taxa_id] = row # save to class var for use later when creating Proteins objects

# create Domains objects 
for protein_id, data in domains.items():
    for values in data:
        try:
            row = Domains.objects.create(pfam=pfam_rows[values["pfam_id"]], description=values["description"], start=values["start"], stop=values["stop"])
            row.save()
        except:
            DO_NOTHING

# create Proteins objects 
for protein_id, data in protein.items():
    row = Protein.objects.create(
        protein_id=protein_id, 
        sequence=protein_sequence[protein_id], 
        taxonomy=taxonomy_rows[data["taxa_id"]], 
        length=data["length"], 
    )
    # unzip appended domain values to a single protein_id
    for pfam_id, start, stop in zip(data['pfam_id'], data['start'], data['stop']):
        # retrieve Domains object that match the above existing conditions
        pfam_object = Pfam.objects.get(domain_id = pfam_id)
        domains_object = Domains.objects.filter(Q(pfam = pfam_object) & Q(start= start) & Q(stop= stop)).get()
        # add the Domains object to the Proteins object
        row.domains.add(*[domains_object])
    row.save()