from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm, LoginForm
from django.contrib import messages
from .serializers import DocumentSerializer
import os
from django.http import HttpResponse, Http404
from django.views import generic
from fileupload.settings import MEDIA_ROOT

class GetDocumentViewSet(generic.ListView):
    model = Document
    template_name = 'listing.html'

    def get_queryset(self):
        return Document.objects.all()

class DetailView(generic.DetailView):
    model = Document
    template_name = 'detail.html'
    def get_context_data(self, **kwargs):
        obj = kwargs.get('object',None)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if obj:
            docObj = Document.objects.get(pk=obj.id)
            if docObj:            
                import pandas as pd
                context['fname'] = str(docObj.document) 
                docFile = MEDIA_ROOT+"/"+str(docObj.document)
                df = pd.read_csv(docFile)
                # Add in a QuerySet of all the books
                context['doc_content'] = df
        return context


def login(request):    
    return render(request, 'login.html')

def home(request):
    if  isloggedin(request):
        documents = Document.objects.all()
        return render(request, 'home.html')
    else:
        return redirect('login')

def download_file(request,path): 
    file_path = os.path.join(settings.MEDIA_ROOT, 'example-input-file.txt') 
    if os.path.exists(file_path):    
        with open(file_path, 'rb') as fh:    
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")    
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)  
            messages.info(request, "File  download success!")  
            return response
    return None


def model_form_upload(request):
    if request.method == 'POST':
        try:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request, "File upload Success!")
            else:
                messages.error(request, repr(form.errors))
        except Exception as e:
            pass
        return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })

def login(request):
    messages.error(request, "") 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username == password == 'admin':
                request.session['user'] = username
                return redirect('home')
            else:
                messages.error(request, "Invalid Credential.") 
         

    form = LoginForm()
    return render(request, 'login.html', {
        'form': form
    })

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    messages.info(request, "Logout Success!")
    return redirect('login')

def isloggedin(request):
    return True if 'user' in request.session else False
