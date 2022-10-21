from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('protein/<str:pk>', views.protein, name='protein'),
    # path('api/protein/', api.CreateProtein.as_view(), name="create_protein"), # testf
    path('api/protein/', api.CreateProtein, name="create_protein"), # endpoint 1, tesf
    path('api/protein/<str:protein_id>', api.ProteinDetailsList.as_view(), name="protein_details_list"), # endpoint2, tested
    path('api/pfam/<str:domain_id>', api.PfamDetails.as_view(), name="pfam_details"), # endpoint 3, tested
    path('api/proteins/<int:taxa_id>', api.ProteinTaxaList, name="proteins_taxa_list"), # endpoint 4, tested
    path('api/pfams/<int:taxa_id>', api.DomainsTaxaList, name="domains_taxa_list"), # endpoint 5, tested
    path('api/coverage/<str:protein_id>', api.Coverage, name="coverage"), # endpoint 6, tested
]