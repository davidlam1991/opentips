from django.views import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Prefetch
import json

from .models import Post, Comment
from .forms import PostForm, CommentForm, ReportForm
from .filters import PostFilter

# Create your views here.


class AllPostsView(ListView):
    template_name = "posts/index.html"
    model = Post
    # ordering = ["-release_date"]
    context_object_name = "all_posts"

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset=queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_queryset = self.filterset.qs

        unique_addresses = (
            Post.objects.values('address')
            .annotate(address_count=Count('address'))
        )
        first_addresses = [filtered_queryset.filter(address=addr['address']).order_by("-date").first() for addr in unique_addresses]

        no_repeated_posts = sorted(
            [post for post in first_addresses if post is not None],
            key=lambda x: (x.date, x.release_date),
            reverse=True,
        )

        # Pagination for no_repeated_posts
        p_no_repeated_posts = Paginator(no_repeated_posts, 15)
        page_no_repeated = self.request.GET.get("page")
        paginated_no_repeated_posts = p_no_repeated_posts.get_page(page_no_repeated)

        context["no_repeated_posts"] = paginated_no_repeated_posts
        context["filter"] = self.filterset

        return context


class CreatePostView(FormView):
    template_name = "posts/create-post.html"
    form_class = PostForm
    success_url = reverse_lazy("post-main-page")

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.creator = self.request.user
        new_post.release_date = timezone.now()

        new_post.save()
        messages.success(self.request, "Post has been saved successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context['view'] = 'create'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SinglePostView(DetailView):
    template_name = "posts/post-detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        post = self.get_object()

        initial_post = Post.objects.filter(address=post.address).order_by("-date").first()

        # Set up Pagination
        p_reviews = Paginator(Post.objects.filter(address=post.address).order_by("-date"), 4)
        page_reviews = self.request.GET.get("page-reviews")
        all_posts = p_reviews.get_page(page_reviews)

        parent_comments = Comment.objects.filter(CommentPost=post, parent=None).order_by("-date_posted")
        nested_replies = Comment.objects.filter(parent__isnull=False).order_by("date_posted")
        comments = parent_comments.prefetch_related(Prefetch("replies", queryset=nested_replies))
        p_comments = Paginator(comments, 1)
        page_comments = self.request.GET.get("page-comments")
        comments = p_comments.get_page(page_comments)

        context = {
            "initial_post": initial_post,
            "all_posts": all_posts,
            "comments": comments,
            "comment_form": CommentForm(),
            "report_form": ReportForm(),
        }

        # context["initial_post"] = initial_post
        # context["all_posts"] = all_posts
        # context["comments"] = comments
        # context["comment_form"] = CommentForm()
        # context["report_form"] = ReportForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']

            parent_id = request.POST.get('parent_id')
            parent = Comment.objects.get(id=parent_id) if parent_id else None

            new_comment = Comment(
                content=content,
                author=request.user,
                CommentPost=self.get_object(),
                parent=parent,
            )
            new_comment.save()
            return redirect(request.path_info)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


@method_decorator(csrf_exempt, name='dispatch')
class EditCommentView(View):
    def post(self, request, comment_id):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            data = json.loads(request.body)
            comment.content = data.get('content', comment.content)
            comment.save()
            return JsonResponse({'success': True})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'}, status=404)


class EditPostView(UpdateView):
    model = Post
    template_name = "posts/create-post.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'edit'
        return context

    def get_success_url(self):
        return reverse("post-detail", kwargs={"slug": self.object.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ReportView(FormView):
    # template_name = "posts/post-detail.html"
    form_class = ReportForm
    success_url = reverse_lazy("post-detail")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.reported_by = request.user
            new_report.date_reported = timezone.now()
            new_report.content = request.POST.get('reported_comment', None)
            new_report.link = request.POST.get('reported_link', None)
            new_report.save()
            messages.success(request, 'Report submitted successfully.')
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        slug = self.request.POST.get('slug')
        return reverse('post-detail', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteCommentView(UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('post-main-page')

    def test_func(self):
        # comment = self.get_object()
        return self.request.user.is_staff

    def get_success_url(self):
        post = self.object.CommentPost
        return reverse_lazy('post-detail', kwargs={'slug': post.slug})


class DeletePostView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-main-page')

    def test_func(self):
        # post = self.get_object()
        return self.request.user.is_staff

    def get_success_url(self):
        # post = self.object.CommentPost
        return reverse_lazy('post-main-page')