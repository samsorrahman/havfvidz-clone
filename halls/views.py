from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.contrib.auth import authenticate, login
from django.http import Http404
import urllib
from django.forms.utils import ErrorList
# Create your views here.


YOUTUBE_API_KEY = 'AIzaSyAkzDHgx5-ntQ50jRpXcFQheN6YwZ2zK-8'

def home(request):
    return render(request, 'halls/home.html')


def dashboard(request):
    return render(request, 'halls/dashboard.html')



def add_video(request, pk):
    form= VideoForm()
    
    search_form= SearchForm()
    hall= Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404
    if request.method == 'POST':
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video= Video()
            video.hall= hall
            video.url = filled_form.cleaned_data['url']
            parsed_url= urllib.parse.urlparse(video.url)
            video_id= urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                video.title =
                video.save()
    context={
        'form': form,
        'search_form': search_form,
        'hall': hall,
    }
    
    return render(request, 'halls/add_video.html', context)
    


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view
    
    
    
class CreateHall(generic.CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('dashboard')
    

class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'
    

class UpdateHall(generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')
    

class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')