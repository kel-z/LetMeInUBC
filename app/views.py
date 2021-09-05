import app
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CourseForm

from rest_framework import status
from rest_framework.response import Response

from .controller.data_manager import App

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

app = App()

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():

            # formatting the data
            form_data = {
                'course': " ".join([form.cleaned_data['session'], form.cleaned_data['year'], form.cleaned_data['dept'], form.cleaned_data['course'], form.cleaned_data['section']]).upper(),
                'only_general': form.cleaned_data['only_general'],
                'contact': {
                    'sms': form.cleaned_data['sms'],
                    'email': form.cleaned_data['email']
                }
            }

            try:
                app.handle_form_data(form_data)
                return HttpResponse('Add success: ' + " ".join([form_data['course'], str(form_data['only_general']), form_data['contact']['sms'], form_data['contact']['email']]), status=status.HTTP_200_OK)
            except Exception as e:
                return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

    form = CourseForm()
    return render(request, 'form.html', {'form': form})
