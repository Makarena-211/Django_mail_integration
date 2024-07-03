from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, MessageForm
from .email_parser import EmailParser
from django.http import JsonResponse
from django.shortcuts import redirect
import json

def main_view(request):
    return render(request, 'main.html')




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email", "Undefined")
            password = request.POST.get("password", "Undefined")
            messages = message_view(email, password)
            if messages != 'Невозможно подключиться':
                form.save()
                return render(request, 'main.html', {'messages': messages})
            else:
                return render(request, 'login.html', {'error': 'Невозможно подключиться. Проверьте учетные данные или настройки IMAP.'})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



def message_view(email, password):
    data = EmailParser.fetch_all_emails(email, password)
    if data != 'Невозможно подключиться':
        print(data)
        for message in data:
            if 'body' not in message or not message['body']:
                message['body'] = 'Пустое сообщение'

            if 'attachments' not in message or not message['attachments']:
                message['attachments'] = []
            result = [i['filename'] for i in message['attachments']] if message['attachments'] else ['Пустое сообщение']

            form = MessageForm({
                'email':message.get('email'),
                'topic': message.get('topic', '1'),
                'date_sent':message.get('date_sent'),
                'date_recieved':message.get('date_recieved'),
                'body': message.get('body'),
                'attachments':result
            })
            if form.is_valid():
                form.save()
            else:
                print(f"Invalid form data: {form.errors}")
        return data
    else:
        return 'Невозможно подключиться'



        
# Create your views here.
