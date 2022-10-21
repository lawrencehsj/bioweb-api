import json
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_supported_language_variant #default Response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, query

#rest api packages
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response #rest Response, better for development
from rest_framework import status

#packages for easier logic to handle CRUD
from rest_framework import generics
from rest_framework import mixins
# permissions
from rest_framework.permissions import IsAuthenticated

#package for appending querysets
from itertools import chain

from .models import *
from .serializers import *

# # add new protein on 'api/protein/' path
# # need to convert data to JSON to render on html
# # or overwrite the post method to save the data seperately
# class CreateProtein(generics.ListCreateAPIView): #ListCreateAPIView
#     queryset = Protein.objects.filter(protein_id="A0A016S8J7")
#     serializer_class = ProteinSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(serializer)
#         serializer = self.get_serializer(instance=instance)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def perform_create(self, serializer):
#         return serializer.create(validated_data=serializer.validated_data)

# ENDPOINT 1: add new protein on 'api/protein/' path 
@api_view(['GET','POST'])
def CreateProtein(request): 
    # display one protein for reference
    if request.method == 'GET':
        protein = Protein.objects.filter(protein_id="A0A016S8J7")
        serializer = ProteinSerializer(protein, many=True)
        return Response(serializer.data)

    # insert via json data
    if request.method == 'POST':
        # get json data based on POST request
        # assign to ProteinSerializer and render in page if valid
        json_data = json.loads(request.body.decode(encoding='utf-8'))
        # taxonomy_serializer = TaxonomySerializer(data=json_data['taxonomy'])
        # for domain in json_data['domains']:
        #     domain_serializer = DomainsSerializer(data=domain)
        #     if domain_serializer.is_valid():
        #         domain_serializer.save()
        #     pass
        # protein_serializer = ProteinSerializer(protein_id=json_data['protein_id'], sequence=json_data['sequence'], taxonomy=taxonomy_serializer, length=json_data['length'])
        # # if taxonomy_serializer.is_valid():
        # #     return HttpResponse('algith')
        # # return HttpResponse(s)
        protein_serializer = ProteinSerializer(data=json_data)
        # check for valid data
        # if valid, save the data and display it to the user
        if protein_serializer.is_valid():
            # protein_serializer.save()
            return Response(protein_serializer.data,status=status.HTTP_201_CREATED)
        return Response(protein_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# ENDPOINT 2: view protein details based on protein_id on 'api/protein/<protein_id>' path
class ProteinDetailsList(mixins.RetrieveModelMixin, generics.GenericAPIView): # generic API view
    # lookup_field based on the input appended to the url
    lookup_field = 'protein_id'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# ENDPOINT 3: get pfam object details based on pfam_id on 'api/pfam/<pfam_id>'
class PfamDetails(mixins.RetrieveModelMixin, generics.GenericAPIView): # generic API view
    lookup_field = 'domain_id' #aka pfam_id
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# ENDPOINT 4: get protein_id and id based on taxa_id on 'api/proteins/<taxa_id>'
@api_view(['GET'])
def ProteinTaxaList(request, taxa_id): #takes in taxa_id upon request in url
    if request.method == 'GET':
        # retrieve Taxonomy object, then Protein objects based on taxa_id
        taxa_object = Taxonomy.objects.get(taxa_id = taxa_id)
        protein_id_objects = Protein.objects.filter(taxonomy = taxa_object)
        serializer = ProteinTaxaIDSerializer(protein_id_objects, many=True)
        return Response(serializer.data)

# ENDPOINT 5: get domains pfam details based on taxa_id on 'api/pfams/<taxa_id>'
@api_view(['GET'])
def DomainsTaxaList(request, taxa_id): #takes in taxa_id upon request in url
    # local var to store multiple domains id upon query
    domains_id_list = []
    if request.method == 'GET':
        # retrieve Taxonomy object, then Protein objects based on taxa_id
        taxa_object = Taxonomy.objects.get(taxa_id = taxa_id)
        protein_objects = Protein.objects.filter(taxonomy = taxa_object)
        # loop through respective objects in protein_objects that matched with taxa_id
        for protein in protein_objects:
            # look for all matching Domains objects with protein_objects
            domains_objects = Domains.objects.filter(protein = protein)
            # getting the domain_pk 
            for domains in domains_objects:
                domains_id_list.append(domains.pk)

        # retrive domains objects basd on pk
        result = Domains.objects.filter(pk__in = domains_id_list)
        serializer = DomainsTaxaIDSerializer(result, many=True)
        return Response(serializer.data)

# ENDPOINT 6: get coverage details
@api_view(['GET'])
def Coverage(request, protein_id): #takes in protein_id upon request in url
    if request.method == 'GET':
        sum=0
        # retrieve protein object based on protein_id
        protein = Protein.objects.get(protein_id = protein_id)
        # retrive domains objects based on protein object retrieved (might have > 1)    
        domains_objects = Domains.objects.filter(protein = protein)
        # loop thru domains_objects to calculate the values
        for domain in domains_objects:
            sum = sum + domain.start-domain.stop
        cal = sum / protein.length
        return HttpResponse("coverage:    " + str(cal))

