from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, MessageForm
from .email_parser import EmailParser
from django.http import JsonResponse
from django.shortcuts import redirect


def main_view(request):
    return render(request, 'main.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email", "Undefined")
            password = request.POST.get("password", "Undefined")
            form.save()
            message_view(email, password)
            return redirect("/", {'email':email, 'password':password})
    else:
        form = LoginForm()
    return render(request, 'login.html')



def message_view(email, password):
    data = EmailParser.fetch_all_emails(email, password)
    print(data)
    for message in data:
        form = MessageForm({
            'email_account':message.get('email'),
            'topic': message.get('topic', []),
            'date_sent':message.get('date_sent'),
            'date_recieved':message.get('date_recieved'),
            'body': message.get('body', []),
            'attacments': message.get('attachments', [])
        })
        if form.is_valid():
            form.save()
        else:
            print(f"Invalid form data: {form.errors}")
# Create your views here.
