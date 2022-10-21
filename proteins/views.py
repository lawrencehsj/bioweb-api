from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    proteins = Protein.objects.all()
    return render(request, 'proteins/index.html', {'proteins': proteins})

def protein(request, pk):
    protein = Protein.objects.get(protein_id=pk)
    return render(request, "proteins/protein.html", {'protein': protein})

