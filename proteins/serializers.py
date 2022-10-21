from rest_framework import serializers 
from rest_framework.fields import ListField
from .models import *

# ============= Serializers that corresponds to Model objects ===================
# ===============================================================================
class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']

class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']

class DomainsSerializer(serializers.ModelSerializer):
    pfam = PfamSerializer()
    class Meta:
        model = Domains
        fields = ['pfam', 'description', 'start', 'stop']

# ModelSerializer is more dynamic and straightforward
class ProteinSerializer(serializers.ModelSerializer):
    taxonomy = TaxonomySerializer()
    domains = DomainsSerializer(many=True)
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']
        depth = 1
    
    # creating domains object and proteins object based on their many-to-many relation
    def create(self, validated_data):
        # domains_data = validated_data.pop('domains')
        # protein = Protein.objects.create(**validated_data)
        # Domains.objects.create(protein=protein, **domains_data)
        # return Protein
        return Protein.objects.create(**validated_data)

class ProteinDomainLinkSerializer(serializers.ModelSerializer):
    protein = ProteinSerializer()
    domains = DomainsSerializer(many=True)
    class Meta:
        model = ProteinDomainLink
        fields = ['protein', 'domains']

# ================== Serializers to cater for API Views =========================
# ===============================================================================
# for ENDPOINT 4
class ProteinTaxaIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['id','protein_id']

# for ENDPOINT 5
class DomainsTaxaIDSerializer(serializers.ModelSerializer):
    pfam = PfamSerializer()
    class Meta:
        model = Domains
        fields = ['pk','pfam']
