import re
from unicodedata import category
from django.shortcuts import redirect, render
from .models import Catagory, Photo
from .forms import AddNewPhoto, AddNewCategory

from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms

# Create your views here.
class GalleryList(LoginRequiredMixin, ListView):
    model = Photo
    context_object_name = 'categories'
    template_name = "photos/gallery.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["photos"] = self.photos
        context['categories'] = Catagory.objects.all()
        context['photos'] = context['photos'].filter(user=self.request.user)
       # print(context)
        return context

    
    def get(self, request):
        data = request.GET

        category = request.GET.get('category')
        if category == None:
            self.photos = Photo.objects.all()
        else:
            self.photos = Photo.objects.filter(category__name=category)

        return super().get(request)


class PhotoDetail(LoginRequiredMixin, DetailView):
    model = Photo
    context_object_name = "photo"
    template_name = "photos/photo.html"

'''def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
    
    categories = Catagory.objects.all() 
    context = {'photos':photos,'categories':categories}
    return render(request, "photos/gallery.html", context)'''

'''def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, "photos/photo.html", {'photo': photo})'''

class AddPhoto(LoginRequiredMixin, CreateView):
    model = Photo
   # fields = ['category','description','image']
    fields = ['category','title', 'description', 'image']
    success_url = reverse_lazy('gallery')
   # form_class = AddNewPhoto
    category = None

    def get_context_data(self, **kwargs):
        print('context')
        context =  super().get_context_data(**kwargs)
        context['form'] = AddNewPhoto()
        return context


    def form_valid(self, form):
        print('form valid')
        form.instance.user = self.request.user
        form.instance.category = self.category
        return super(AddPhoto, self).form_valid(form)



    def post(self, request):
        data = request.POST

        self.category, created = Catagory.objects.get_or_create(id=data['category'])
      #  else:
          #  raise forms.ValidationError('Provide either a date and time or a timestamp')

        return super().post(request)

'''def addPhoto(request):
    category = Catagory.objects.all()
    
    if request.method == "POST":
        data = request.POST
        image =  request.FILES.get('image')
        if data['category'] != 'none':
            category = Catagory.objects.get(id=data['category'])
        elif  data['category_new'] != '':
            category, created = Catagory.objects.get_or_create(name=data['category_new'])
        else:
            category = None
        
        photo = Photo.objects.create(
            category = category,
            description = data['description'],
            image = image
        )
        return redirect("gallery")

    context = {'categories':category}
    return render(request, "photos/add.html", context)'''

class AddNewCategory(LoginRequiredMixin, CreateView):
    model = Catagory
   # fields = ['category','description','image']
    success_url = reverse_lazy('gallery')
    form_class = AddNewCategory
    #category = None

    def get_context_data(self, **kwargs):
        print('context')
        
        context =  super().get_context_data(**kwargs)
        #context['form'] = AddNewCategory()
        return context

class CustomLoginView(LoginView):
    template_name = "photos/login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('gallery')

class RegisterPage(FormView):
    template_name = "photos/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
       # print("register: ",dir(form),'\n')
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('gallery')
        return super(RegisterPage, self).get(*args, **kwargs)

class PhotoUpdate(LoginRequiredMixin,UpdateView):
    model = Photo 
    fields = ['category','title', 'description', 'image']
    success_url = reverse_lazy('gallery')
    template_name = "photos/photo_update.html"

class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo 
    fields = '__all__'
    success_url = reverse_lazy('gallery')
    template_name = "photos/photo_delete.html"