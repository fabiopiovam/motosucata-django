# -*- coding: utf-8 -*-

from django import forms

class ContactForm(forms.Form):
    name    = forms.CharField(label=u'Nome', max_length=50, required=True)
    email   = forms.EmailField(label=u'e-mail', max_length=80, required=False)
    phone   = forms.CharField(label=u'Telefone(s)', max_length=50, required=False)
    message = forms.CharField(label=u'Mensagem', widget=forms.Textarea)
    
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        if (str(email).strip() == "" and str(phone).strip()==""):
            self._errors["email"] = self.error_class([u"Informe um e-mail ou telefone para contato"])
            
            del cleaned_data["email"]
        
        return cleaned_data