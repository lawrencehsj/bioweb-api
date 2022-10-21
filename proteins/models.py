from enum import unique
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import related

# Entities: 
#       Sequence | protein_id, sequence
#       Taxonomy | taxa_id, clade, genus, species
#       Pfam     | domains_id, domain_description
#       Domains  | pfam, description, start, stop
#       Protein  | protein_id, sequence, taxonomy, length, domains
#       ProteinDomainLink | Protein, Domains

# Relationships:
#       Taxonomy --(one-to-one)--> Protein <--(many-to-many)-- Domains <--(one-to-one)-- Pfam

class Sequence(models.Model): 
    protein_id=models.CharField(max_length=64, null=False, blank=False)
    sequence=models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return "Sequence | " + self.protein_id + " " + self.sequence

class Taxonomy(models.Model):
    taxa_id=models.IntegerField(null=False, blank=False)
    clade=models.CharField(max_length=1, null=False, blank=False, default='E')
    genus=models.CharField(max_length=128, null=False, blank=False)
    species=models.CharField(max_length=128, null=False, blank=False)
    def __str__(self):
        return str(self.taxa_id) + ", " + self.clade + ", " + self.genus + ", " + self.species

class Pfam(models.Model):
    domain_id=models.CharField(max_length=64, null=False, blank=False)
    domain_description=models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return self.domain_id + ", " + self.domain_description

class Domains(models.Model):
    pfam=models.ForeignKey(Pfam, on_delete=models.CASCADE)
    description=models.CharField(max_length=256, null=False, blank=False)
    start=models.IntegerField(null=False, blank=False)
    stop=models.IntegerField(null=False, blank=False)
    # group values together to ensure unique entry
    class Meta:
        unique_together = ['pfam', 'start', 'stop']
    def __str__(self):
        return self.pfam.domain_id + ", " + self.pfam.domain_description + ", " + self.description + ", " + str(self.start) + ", " + str(self.stop)

class Protein(models.Model):
    protein_id=models.CharField(max_length=64, null=False, blank=False)
    sequence=models.CharField(max_length=256, null=False, blank=False)
    # sequence=models.ForeignKey(Sequence.sequence, on_delete=models.CASCADE)
    taxonomy=models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
    length=models.IntegerField(null=False, blank=False)
    domains=models.ManyToManyField(Domains, through='ProteinDomainLink')
    def __str__(self):
        return "Protein | " + self.protein_id + " " + str(self.taxonomy.taxa_id) + " " + str(self.length) + " " + str(self.domains)

class ProteinDomainLink(models.Model):
    protein=models.ForeignKey(Protein, on_delete=models.CASCADE)
    domains=models.ForeignKey(Domains, on_delete=models.CASCADE)
    # group values together to ensure unique entry
    class Meta:
        unique_together = ['protein', 'domains']