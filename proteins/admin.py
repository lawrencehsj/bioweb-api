from django.contrib import admin
from .models import *

# Register your models here.
class ProteinAdmin(admin.ModelAdmin):
    list_display = ('protein_id', 'sequence', 'taxonomy', 'length', )

# admin site to track database entries
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Domains)
admin.site.register(ProteinDomainLink)
