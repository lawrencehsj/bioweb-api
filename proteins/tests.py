import json

from django.test import TestCase
from django.urls import reverse #allows us to take a path in our urls file to turn it into a url string
from django.urls import reverse_lazy

# rest api testing packages
from rest_framework.test import APIRequestFactory 
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# Create your tests here.
# any function that starts with test will be run automatically
# ==================== SERIALIZER TESTING ======================
class SerializerTest(APITestCase):
    taxonomy1 = None
    pfam1 = None
    domains1 = None
    protein1 = None
    taxonomySerializer = None
    pfamSerializer = None
    domainsSerializer = None
    proteinSerializer = None

# create protein object based on other sub objects
    def setUp(self):
        # instantiate factory objects
        self.taxonomy1 = TaxonomyFactory.create(taxa_id=1)
        self.pfam1 = PfamFactory.create(pk=1, domain_id="domain1")
        self.domains1 = DomainsFactory.create(pk=1, pfam=self.pfam1)
        self.protein1 = ProteinFactory.create(pk=1, protein_id="protein1", taxonomy=self.taxonomy1)
        self.proteinDomainLink = ProteinDomainLinkFactory.create(protein=self.protein1, domains=self.domains1)
        self.protein1.domains.add(self.domains1)

        # instantiate serializer objects
        self.taxonomySerializer = TaxonomySerializer(instance=self.taxonomy1)
        self.pfamSerializer = PfamSerializer(instance=self.pfam1)
        self.domainsSerializer = DomainsSerializer(instance=self.domains1)
        self.proteinSerializer = ProteinSerializer(instance=self.protein1)
        self.proteinDomainLinkSerializer = ProteinDomainLinkSerializer(instance=self.proteinDomainLink)
        self.proteinTaxaIDSerializer = ProteinTaxaIDSerializer(instance=self.protein1)
        self.domainsTaxaIDSerializer = DomainsTaxaIDSerializer(instance=self.pfam1)

    def tearDown(self):
        # Sequence.objects.all().delete()
        # Taxonomy.objects.all().delete()
        # Pfam.objects.all().delete()
        # Domains.objects.all().delete()
        # Protein.objects.all().delete()
        SequenceFactory.reset_sequence(0)
        TaxonomyFactory.reset_sequence(0)
        PfamFactory.reset_sequence(0)
        DomainsFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)

    # =================== SET OF SERIALIZER TESTS ===========================
    # =================== comment out when necessary =======================
    # ======================================================================
    def test_taxonomySerializer(self):
        data = self.taxonomySerializer.data
        # check for correct keys
        self.assertEqual(set(data.keys()), set(['taxa_id', 'clade', 'genus', 'species'])) 
        # check for correct existing taxa data
        self.assertEqual(data['taxa_id'],1)

    def test_pfamSerializer(self):
        data = self.pfamSerializer.data
        # check for correct keys
        self.assertEqual(set(data.keys()), set(['domain_id', 'domain_description'])) 
        # check for correct existing pfam data
        self.assertEqual(data['domain_id'],'domain1')

    def test_domainsSerializer(self):
        data = self.domainsSerializer.data
        # check for correct keys
        self.assertEqual(set(data.keys()), set(['pfam', 'description', 'start', 'stop'])) 
        # check for correct existing domains data
        self.assertEqual(data['pfam']['domain_id'],self.pfam1.domain_id)

    # check for domains existence in protein serializer (many-to-many)
    def test_proteinSerializer(self):
        data = self.proteinSerializer.data
        # check for correct keys
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequence', 'taxonomy', 'length', 'domains']))
        # check for existing protein data
        self.assertEqual(data['domains'][0]['pfam']['domain_id'],self.domains1.pfam.domain_id)

    # def test_proteinDomainLinkSerializer(self):
    #     data = self.proteinDomainLinkSerializer.data
    #     # check for correct keys
    #     self.assertEqual(set(data.keys()), set(['protein', 'domains']))
    #     # check for existing protein data
    #     self.assertEqual(data['protein']['protein_id'],self.protein1.protein_id)
    
    

# ==================== ROUTE TESTING ======================
class RouteTest(APITestCase):
    taxa1 = None
    pfam1 = None
    domains1 = None
    protein1 = None

    # setup class variables to use for testing
    # override
    def setUp(self):
        # instantiate factory objects
        self.taxa1 = TaxonomyFactory.create(pk=1,taxa_id=123)
        self.pfam1 = PfamFactory.create(pk=1, domain_id="domain1")
        self.domains1 = DomainsFactory.create(pk=1, pfam=self.pfam1)
        self.protein1 = ProteinFactory.create(pk=1, protein_id="protein1", taxonomy=self.taxa1)
        self.proteinDomainLink = ProteinDomainLinkFactory.create(protein=self.protein1, domains=self.domains1)
        self.protein1.domains.add(self.domains1)

        # urls (actions) to handle requests and responses for testing
        self.create_url = "/api/protein/"
        self.protein_details_url = reverse('protein_details_list', kwargs={'protein_id': "protein1"})
        self.pfam_details_url = reverse('pfam_details', kwargs={'domain_id': "domain1"})
        self.proteins_taxa_url = reverse('proteins_taxa_list', kwargs={'taxa_id': 123})
        self.domains_taxa_url = reverse('domains_taxa_list', kwargs={'taxa_id': 123})
        self.coverage_url = reverse('coverage', kwargs={'protein_id': "protein1"})
        self.bad_url = "/api/proteins/XXX/"

    # override
    def tearDown(self):
        # Sequence.objects.all().delete()
        # Taxonomy.objects.all().delete()
        # Pfam.objects.all().delete()
        # Domains.objects.all().delete()
        # Protein.objects.all().delete()
        SequenceFactory.reset_sequence(0)
        TaxonomyFactory.reset_sequence(0)
        PfamFactory.reset_sequence(0)
        DomainsFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)

    # ======================= SET OF ROUTE TESTS ===========================
    # ===================== comment out when necessary =====================
    # ======================================================================
    def test_CreateProtein(self): # only managed to test for GET
        response = self.client.get(self.create_url, format='json')
        self.assertEqual(response.status_code, 200) # response status PASS
        # FAIL TO TEST FOR POST HERE >>>>
        # response = self.client.post(self.create_url, self.protein1, format='json')
        # data = json.loads(response.content)
        # self.assertEqual(response.status_code, 200) # response status PASS
        

    # test [GET /api/protein/[PROTEIN ID] - return the protein sequence and all we know about it]
    # PASS
    def test_ProteinDetailsReturnsSuccess(self):
        response = self.client.get(self.protein_details_url, format='json') 
        response.render() 
        # check for correct arrived data
        data = json.loads(response.content) # arrived data
        # print(data)
        self.assertTrue('sequence' in data) # check for sequence(key) value 
        self.assertEqual(data['sequence'], '2SEQUENCE') # check for existing sequence value loaded
    
    # test [GET /api/pfam/[PFAM ID] - return the domain and it's description]
    # PASS
    def test_PfamDetailsReturnsSuccess(self):
        response = self.client.get(self.pfam_details_url, format='json') 
        response.render() 
        # check for correct arrived data
        data = json.loads(response.content) # arrived data
        self.assertTrue('domain_description' in data) # check for domain_description(key) value 
        self.assertEqual(data['domain_description'], 'pfam description') # check for existing sequence value loaded

    # test [GET /api/proteins/[TAXA ID] - return a list of all proteins for a given organism]
    # since it is a list, we only want the first item in the list: accessible by index [0]
    # PASS 
    def test_ProteinTaxaDetailsReturnsSuccess(self):
            response = self.client.get(self.proteins_taxa_url, format='json') 
            response.render() 
            # check for correct arrived data
            data = json.loads(response.content) # arrived data
            # print(data[0]['id'])
            self.assertTrue('id' in data[0]) # check for id key in data
            obj = Taxonomy.objects.get(id = data[0]['id']) # retrieve Taxonomy object based on pk
            self.assertEqual(obj.taxa_id, 123) # check for taxa_id match with factory model

    # test [GET /api/pfams/[TAXA ID] - return a list of domains pfam details based on taxa_id]   
    # since it is a list, we only want the first item in the list: accessible by index [0]
    # PASS
    def test_DomainsTaxaDetailsReturnsSuccess(self):
            response = self.client.get(self.domains_taxa_url, format='json') 
            response.render() 
            # check for correct arrived data
            data = json.loads(response.content) # arrived data
            self.assertTrue('pfam' in data[0]) # check for taxonomy_id key in data
            # print(data)
            taxa_obj = Taxonomy.objects.get(id = data[0]['pk']) # retrieve Taxonomy object based on pk
            protein_obj = Protein.objects.get(taxonomy = taxa_obj) # retrieve Protein object based on taxa_obj
            domain_obj = Domains.objects.get(protein = protein_obj) # retrieve Domain object based on protein_obj
            # print(domain_obj)
            self.assertEqual(domain_obj.pfam.domain_description, 'pfam description') # check for taxa_id match with factory model

    # TEST [GET /api/coverage/[PROTEIN ID] - return the domain coverage for a given protein]
    # PASS
    def test_CoverageReturnsSuccess(self):
        response = self.client.get(self.coverage_url, format='json') 
        # check for successful message status
        self.assertEqual(response.status_code, 200)
