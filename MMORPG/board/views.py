from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from dajngo.contrib.auth.models import User,Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .model import  Post, Author, Reply
from .forms import ReplyForm, PostForm 
from django.shortcuts import redirect
from .tasks import notify_new_replay, notify_accept_replay
from django.urls import reverse_lazy

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'boardhtml/Profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile
    template_name = 'boardhtml/Profile/create_profile.html'
    fields = ['profile_pic', 'bio']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = 'password_change_done'

class PostListView(ListView):
    model = Post
    template_name = 'boardhtml/post.html'
    context_object_name = 'post'
    ordering = ['-dateCreation']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['posts_count'] = Post.objectc.all().count()
        return context


class PostDetailView(DetailView, CreateView):
    model = Post
    form_class = ReplyForm
    template_name = 'boardhtml/Post_list/post_detail.html'
    context_object_name = 'post'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = User.objects.get(id=self.request.user.id)
        reply.post = Post.objects.get(id=self.kwargs.get('pk'))
        reply.save()
        notify_new_replay(reply.id)
        return redirect('board:posts')

class PostListView(ListView):
    model = Post
    template_name = 'boardhtml/Post_list/post.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 3

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['posts_count'] = Post.objects.all().count()
        return context

class PostCreateView(CreateView):
    template_name = 'boardhtml/Post_list/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.used.id)
        post.save()
        return redirect('board:posts')

class PostUpdateView(UpdateView):
    template_name = 'boardhtml/Post_list/post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
            id_pk = self.kwargs.get('pk')
            return Post.objects.get(pk=id_pk)

    def dispatch(self, request, *args, **kwargs):
            if self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
                return super().dispatch(request,*args, **kwargs)
            else:
                return HttpResponse('<h3>¬нимание!</h3>»змен€ть или удал€ть можно только свои объ€влени€!')


class PostDeleteView(DeleteView):
    template_name = 'boardhtml/Post_list/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('board:posts')
    permission_required = ('board.delete_post')

    def dispatch(self, request, *args, **kwargs):
            if self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
                return super().dispatch(request,*args, **kwargs)
            else:
                return HttpResponse('<h3>¬нимание!</h3>»змен€ть или удал€ть можно только свои объ€влени€!')

class CategoryDetailView(ListView):
    model = Post
    template_name = 'boardhtml/Post_list/post.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 3

    def get_queryset(self):
        cat_key = self.kwargs['cat_key']
        queryset = Post.objects.filter(category=cat_key)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_key = self.kwargs['cat_key']
        cat_display = self.kwargs['cat_disp']
        context['category'] = cat_display
        context['posts_count'] = Post.objects.filter(category=cat_key).count()  
        context['time_now'] = timezone.localtime(timezone.now()) 
        return context


class AuthorPostsListView(ListView):
    model = Post
    template_name = 'boardhtml/Post_list/post.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 3

    def get_queryset(self):
        author_pk = self.kwargs['author_pk']
        queryset = Post.objects.filter(author_id=author_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_pk = self.kwargs['author_pk']
        context['author'] = User.objects.get(pk=author_pk)
        context['posts_count'] = Post.objects.filter(author_id=author_pk).count()  
        context['time_now'] = timezone.localtime(timezone.now()) 
        return context