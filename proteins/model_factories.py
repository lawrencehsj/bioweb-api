import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

# Factory objects used for testing
class SequenceFactory(factory.django.DjangoModelFactory):
    protein_id = "A123"
    sequence = "SEQUENCE"
    class Meta:
        model = Sequence

class TaxonomyFactory(factory.django.DjangoModelFactory):
    taxa_id = "123"
    clade = 'E'
    genus = "hocus"
    species = "pocus"
    class Meta:
        model = Taxonomy

class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = "pfam123"
    domain_description = "pfam description"
    class Meta:
        model = Pfam

class DomainsFactory(factory.django.DjangoModelFactory):
    pfam = factory.SubFactory(PfamFactory)
    description = "domains description"
    start = 1
    stop = 99
    class Meta:
        model = Domains

# create many 2 many domains
class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = factory.Sequence(lambda n: "protein_id%d" % n+str(1)) #protein_id1
    sequence = "2SEQUENCE"
    taxonomy = factory.SubFactory(TaxonomyFactory)
    length = 234

    # many-to-many object creation
    # @factory.post_generation
    # def domains(self, create, extracted, **kwargs):
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #     if extracted:
    #         for domain in extracted:
    #             self.domains.add(domain)
    class Meta:
        model = Protein

class ProteinDomainLinkFactory(factory.django.DjangoModelFactory):
    protein = factory.SubFactory(ProteinFactory)
    domains = factory.SubFactory(DomainsFactory)
    class Meta:
        model = ProteinDomainLink

# class ProteinWithDomainFactory(ProteinFactory):
#     organism = factory.RelatedFactory(
#         ProteinDomainLinkFactory,
#         protein = factory.SubFactory(ProteinFactory),
#         domains__pfam = factory.SubFactory(PfamFactory)
#     )
