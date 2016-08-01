from django.shortcuts import render, redirect
from django.conf import settings

from uploads.core.models import Document
from uploads.core.forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST':
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']

            path = u'{0}/{1}'.format(settings.MEDIA_ROOT, myfile.name)
            with open(path, 'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)

            uploaded_file_url = u'{0}{1}'.format(settings.MEDIA_URL, myfile.name)
            return render(request, 'core/simple_upload.html', { 'uploaded_file_url': uploaded_file_url })

    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
