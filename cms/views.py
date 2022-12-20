from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from cms import promoters
from cms.forms import ArticleForm, UserForm
from cms.models import Article


class ArticleView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        post_data = request.POST
        article = Article.objects.create(body=post_data['body'],
                                         link=post_data['link'])
        marketer = promoters.Marketer(article)
        try:
            marketer.promote()
            message_type = messages.SUCCESS
            message_text = 'Продвижение статьи прошло успешно'
        except promoters.PromoteError as exc:
            message_type = messages.ERROR
            message_text = 'Произошла ошибка: %s' % str(exc)
        messages.add_message(request=request,
                             level=message_type,
                             message=message_text)
        return HttpResponseRedirect(reverse('new-article'))


@login_required
def new_article(request):
    article_form = ArticleForm()
    article_context = {
        'new_article_form': article_form
    }
    return render(request,
                  template_name='articles/new.html',
                  context=article_context)


class AuthenticationView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        auth_context = {
            'user_form': user_form,
        }
        return render(request,
                      'user/sign_in.html',
                      context=auth_context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user = authenticate(username=username,
                                          password=password)
        if authenticated_user is None:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Неправильное имя пользователя и/или пароль')
            return HttpResponseRedirect(reverse('authenticate'))
        else:
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Поздравляю, вы вошли успешно')
            login(request,
                  user=authenticated_user)
            return HttpResponseRedirect(reverse('new-article'))
