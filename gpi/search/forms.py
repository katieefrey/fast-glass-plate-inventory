# from django import forms
# from django.forms import ModelMultipleChoiceField
# #from uploads.core.models import Document
# from .models import Component, Item, Cleaning, Checking

# from django.forms.models import ModelForm
# from django.forms.widgets import CheckboxSelectMultiple

# class BarcodeForm(forms.Form):
#     inputBarcode = forms.CharField(label='Check Item & Proceedures', max_length=100)


# class ModifyDevice(ModelForm):
    
#     class Meta:
#         model = Item
#         fields = ("components","cleaning","checking","location")
             
#     def __init__(self, *args, **kwargs):
        
#         super(ModifyDevice, self).__init__(*args, **kwargs)
        
#         self.fields["components"].widget = CheckboxSelectMultiple()
#         #self.fields["components"].queryset = Component.objects.all()
#         self.fields["cleaning"].widget = CheckboxSelectMultiple()
#         #self.fields["cleaning"].queryset = Cleaning.objects.all()
#         self.fields["checking"].widget = CheckboxSelectMultiple()
#         #self.fields["checking"].queryset = Checking.objects.all()
    

# class DevComp(ModelForm):
    
#     class Meta:
#         model = Item
#         fields = ("components",)
#         labels = {
#             'components': '<strong>Device Components</strong>',
#         }
             
#     def __init__(self, *args, **kwargs):
        
#         super(DevComp, self).__init__(*args, **kwargs)
        
#         self.fields["components"].widget = CheckboxSelectMultiple()


# class DevClean(ModelForm):
    
#     class Meta:
#         model = Item
#         fields = ("cleaning",)
#         labels = {
#             'cleaning': '<strong>Things to Clean</strong>',
#         }

             
#     def __init__(self, *args, **kwargs):
        
#         super(DevClean, self).__init__(*args, **kwargs)
        
#         self.fields["cleaning"].widget = CheckboxSelectMultiple()
    


# class DevCheck(ModelForm):
    
#     class Meta:
#         model = Item
#         fields = ("checking",)
#         labels = {
#             'checking': '<strong>Things to Check</strong>',
#         }
             
#     def __init__(self, *args, **kwargs):
        
#         super(DevCheck, self).__init__(*args, **kwargs)
        
#         self.fields["checking"].widget = CheckboxSelectMultiple()    
    

# class DevLoc(ModelForm):
    
#     class Meta:
#         model = Item
#         fields = ("location","notes")
#         labels = {
#             'location': '<strong>Location</strong>',
#             'notes': '<strong>Notes</strong>',
#         }

#     def __init__(self, *args, **kwargs):
        
#         super(DevLoc, self).__init__(*args, **kwargs)             

#         self.fields['notes'].widget = forms.Textarea(attrs={'rows': 4})




# class ChoiceForm(ModelForm):
#     class Meta:
#         model = Item
#         fields = ("components",)
#         labels = {
#             'components': '<strong>Device Components</strong>',
#         }

#     def __init__(self, *args, **kwargs):
        
#         super(ChoiceForm, self).__init__(*args, **kwargs)

#         self.fields['components'] =  ModelMultipleChoiceField(queryset=Component.objects.all())
#         self.fields['components'].widget.attrs['size']='10'













    # def __init__(self, *args, **kwargs):
        
    #     super(DevLoc, self).__init__(*args, **kwargs)
        
    #     self.fields["components"].widget = CheckboxSelectMultiple()
    #     #self.fields["components"].queryset = Component.objects.all()
    #     self.fields["cleaning"].widget = CheckboxSelectMultiple()
    #     #self.fields["cleaning"].queryset = Cleaning.objects.all()
    #     self.fields["checking"].widget = CheckboxSelectMultiple()
    #     #self.fields["checking"].queryset = Checking.objects.all()


# class ModifyDevice(forms.Form):
#     class Meta:
#         model = Item
#     components = forms.ModelMultipleChoiceField(queryset=Component.objects.all())



# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('description', 'document', )


# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()


# class UploadImageForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     img = forms.ImageField()