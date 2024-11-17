from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.conf import settings
from .forms import ContactForm

def index(request):
    return render(request, 'home/home.html')

def contact(request):
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Compose the email
            subject = 'Contact Form Submission'
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            from_email = settings.EMAIL_HOST_USER
            to_email = settings.EMAIL_HOST_USER

            # Set a success message to be displayed on the page
            try:
                send_mail(subject, body, from_email, [to_email])
                success_message = "Thank you for your message! We will get back to you shortly."
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f"An error occurred while sending the email: {str(e)}")
        else:
            print(form.errors)

    # clear the form
    form = ContactForm()
    return render(request, 'home/contact.html', {'form': form, 'success_message': success_message})
