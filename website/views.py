from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import User
from .models import Comment
from django.core.urlresolvers import reverse
import json
from .models import Message
import re


def index(request):
    context = {}
    if 'filter' not in request.session:
        latest_post_list = Post.objects.filter(upvotes__gte=10).order_by('-post_date')[:10]
        if (len(Post.objects.filter(upvotes__gte=10)) > ((1) * 10)):
            context['has_enough_hot_posts'] = True
    else:
        filter = request.session.get('filter')
        if filter == 'All':
            latest_post_list = Post.objects.filter(upvotes__gte=10).order_by('-post_date')[:10]
            if (len(Post.objects.filter(upvotes__gte=10).filter(topic=filter)) > ((1) * 10)):
                context['has_enough_hot_posts'] = True
        else:
            latest_post_list = Post.objects.filter(upvotes__gte=10).filter(topic=filter).order_by('-post_date')[:10]
            if (len(Post.objects.filter(upvotes__gte=10).filter(topic=filter)) > ((1) * 10)):
                context['has_enough_hot_posts'] = True
    context['latest_post_list'] = latest_post_list
    context['actual_page'] = 0
    return buildHomePage(request, context, latest_post_list)


def filter_topic(request):
    filter = request.POST.get('list')
    request.session['filter'] = filter
    return HttpResponseRedirect(reverse('website:index'))


def filter_trending(request):
    context = {}
    if 'filter' not in request.session:
        latest_post_list = Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10).order_by('-post_date')[:10]
        if (len(Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10)) > 10):
            context['has_enough_trending_posts'] = True
    else:
        filter = request.session.get('filter')
        if filter == 'All':
            latest_post_list = Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10).order_by('-post_date')[:10]
            if (len(Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10)) > 10):
                context['has_enough_trending_posts'] = True
        else:
            latest_post_list = Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10).filter(topic=filter).order_by(
                'post_date')[:10]
    context['latest_post_list'] = latest_post_list
    context['actual_page'] = 0
    return buildHomePage(request, context, latest_post_list)


def filter_new(request):
    context = {}
    if 'filter' not in request.session:
        latest_post_list = Post.objects.filter(upvotes__lt=5).order_by('-post_date')[:10]
        if (len(Post.objects.filter(upvotes__lt=5)) > 10):
            context['has_enough_new_posts'] = True
    else:
        filter = request.session.get('filter')
        if filter == 'All':
            latest_post_list = Post.objects.filter(upvotes__lt=5).order_by('-post_date')[:10]
            if (len(Post.objects.filter(upvotes__lt=5)) > 10):
                context['has_enough_new_posts'] = True
        else:
            latest_post_list = Post.objects.filter(upvotes__lt=5).filter(topic=filter).order_by('-post_date')[:10]
            if (len(Post.objects.filter(upvotes__lt=5).filter(topic=filter)) > 10):
                context['has_enough_new_posts'] = True
    context['latest_post_list'] = latest_post_list
    context['actual_page'] = 0
    return buildHomePage(request, context, latest_post_list)


def next_new_page(request, actual_page):
    actual_page = int(actual_page) + 1
    context = {}
    if 'filter' not in request.session:
        latest_post_list = Post.objects.filter(upvotes__lt=5).order_by('-post_date')[
                           actual_page * 10:(actual_page * 10) + 10]
        if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
            context = {'has_enough_new_posts': True}
    else:
        filter = request.session.get('filter')
        if filter == 'All':
            latest_post_list = Post.objects.filter(upvotes__lt=5).order_by('-post_date')[
                               actual_page * 10:(actual_page * 10) + 10]
            if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
                context = {'has_enough_new_posts': True}
        else:
            latest_post_list = Post.objects.filter(upvotes__lt=5).filter(topic=filter).order_by('-post_date')[
                               actual_page * 10:(actual_page * 10) + 10]
            if (len(Post.objects.filter(topic=filter).filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
                context = {'has_enough_new_posts': True}

    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    if (actual_page > 0):
        context['has_previous_new_posts'] = True

    return buildHomePage(request, context, latest_post_list)


def previous_new_page(request, actual_page):
    actual_page = int(actual_page) - 1
    context = {}
    if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
        context = {'has_enough_new_posts': True}
    if (actual_page == 0):
        return HttpResponseRedirect(reverse('website:new'))
        # actual_page = int(actual_page) + 1
    if (actual_page > 0):
        context['has_previous_new_posts'] = True
    latest_post_list = Post.objects.filter(upvotes__lt=5).order_by('-post_date')[
                       actual_page * 10:(actual_page * 10) + 10]
    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    return buildHomePage(request, context, latest_post_list)


def next_trending_page(request, actual_page):
    actual_page = int(actual_page) + 1
    context = {}
    if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
        context = {'has_enough_trending_posts': True}
        # actual_page = int(actual_page) + 1
    latest_post_list = Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10).order_by('-post_date')[
                       actual_page * 10:(actual_page * 10) + 10]
    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    if (actual_page > 0):
        context['has_previous_trending_posts'] = True

    return buildHomePage(request, context, latest_post_list)


def previous_trending_page(request, actual_page):
    actual_page = int(actual_page) - 1
    context = {}
    if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
        context = {'has_enough_trending_posts': True}
    if (actual_page == 0):
        return HttpResponseRedirect(reverse('website:trending'))
        # actual_page = int(actual_page) + 1
    if (actual_page > 0):
        context['has_previous_trending_posts'] = True
    latest_post_list = Post.objects.filter(upvotes__gte=5).filter(upvotes__lt=10).order_by('-post_date')[
                       actual_page * 10:(actual_page * 10) + 10]
    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    return buildHomePage(request, context, latest_post_list)


def next_hot_page(request, actual_page):
    actual_page = int(actual_page) + 1
    context = {}
    if 'filter' not in request.session:
        latest_post_list = Post.objects.filter(upvotes__gte=10).order_by('-post_date')[
                           actual_page * 10:(actual_page * 10) + 10]
        if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
            context = {'has_enough_hot_posts': True}
    else:
        filter = request.session.get('filter')
        if filter == 'All':
            latest_post_list = Post.objects.filter(upvotes__gte=10).order_by('-post_date')[
                               actual_page * 10:(actual_page * 10) + 10]
            if (len(Post.objects.filter(upvotes__lt=5)) > ((actual_page + 1) * 10)):
                context = {'has_enough_hot_posts': True}
        else:
            latest_post_list = Post.objects.filter(upvotes__gte=10).filter(topic=filter).order_by('-post_date')[
                               actual_page * 10:(actual_page * 10) + 10]
            if (len(Post.objects.filter(topic=filter).filter(upvotes__gte=10)) > ((actual_page + 1) * 10)):
                context = {'has_enough_hot_posts': True}

    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    if (actual_page > 0):
        context['has_previous_hot_posts'] = True

    return buildHomePage(request, context, latest_post_list)


def previous_hot_page(request, actual_page):
    actual_page = int(actual_page) - 1
    context = {}
    if (len(Post.objects.filter(upvotes__gte=10).filter(topic=filter)) > ((actual_page + 1) * 10)):
        context = {'has_enough_hot_posts': True}
    if (actual_page == 0):
        return HttpResponseRedirect(reverse('website:index'))
    if (actual_page > 0):
        context['has_previous_hot_posts'] = True
    latest_post_list = Post.objects.filter(upvotes__gte=10).filter(topic=filter).order_by('-post_date')[
                       actual_page * 10:(actual_page * 10) + 10]
    context['actual_page'] = actual_page
    context['latest_post_list'] = latest_post_list
    return buildHomePage(request, context, latest_post_list)


def buildHomePage(request, context, latest_post_list):
    template = loader.get_template('website/index.html')
    if 'utilizador_id' not in request.session:
        return HttpResponse(template.render(context, request))
    else:
        context['id'] = request.session.get('utilizador_id')
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        context['user'] = user
        username = user.username
        for post in latest_post_list:
            jsonDec = json.decoder.JSONDecoder()
            upvoteList = None
            downvoteList = None
            if (post.upvoteList != None):
                upvoteList = jsonDec.decode(post.upvoteList)
            if (post.downvoteList != None):
                downvoteList = jsonDec.decode(post.downvoteList)

            if (username in upvoteList):
                post.was_upvoted = 1
            elif (username in downvoteList):
                post.was_downvoted = 1
        list = []
        context['unread_comments'] = []
        context['message_list'] = []
        post_list = Post.objects.filter(user_id=user.id).order_by('post_date')
        context['message_list'] = Message.objects.filter(receiver_user_id=user.id).filter(was_read=0)
        for p in post_list:
            list.append(Comment.objects.filter(post_id=p.id))
        for c in list:
            for l in c:
                if not (l.was_read):
                    context['unread_comments'].append(c)
    return HttpResponse(template.render(context, request))


def delete_post(request, post_id, refresh_identifier):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    if (int(refresh_identifier) == 0):
        return HttpResponseRedirect(reverse('website:index'))
    else:
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))


def detalhe(request, post_id, comment_page):
    loged_user = None
    if request.POST.get('load_button'):
        comment_page = int(comment_page) + 1
    valor = 0
    post = get_object_or_404(Post, pk=post_id)
    if 'utilizador_id' in request.session:
        loged_id = request.session.get('utilizador_id')
        loged_user = get_object_or_404(User, pk=loged_id)
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (post.upvoteList != None):
            upvoteList = jsonDec.decode(post.upvoteList)
        if (post.downvoteList != None):
            downvoteList = jsonDec.decode(post.downvoteList)
        if (loged_user.username in upvoteList):
            post.was_upvoted = 1
        elif (loged_user.username in downvoteList):
            post.was_downvoted = 1

    context = {'post': post}
    if (loged_user == None):
        valor = 20 + int(comment_page) * 20
        comment_list = Comment.objects.filter(post=post_id).order_by('-upvotes')[:valor]
        if request.POST.get('comment_filter_list'):
            comment_list = filter_commentList(request, post_id, comment_page, valor)
        if (len(Comment.objects.filter(post=post_id).order_by('-upvotes')[valor:valor + 20]) > 0):
            context['load_button'] = True
    else:
        if (int(loged_user.comment_listing) == 0):
            comment_list = Comment.objects.filter(post=post_id).order_by('-upvotes')
            if request.POST.get('comment_filter_list', True):
                comment_list = filter_commentList(request, post_id, comment_page, 0)
        else:
            valor = loged_user.comment_listing + int(comment_page) * int(loged_user.comment_listing)
            comment_list = Comment.objects.filter(post=post_id).order_by('-upvotes')[:valor]
            if request.POST.get('comment_filter_list', True):
                comment_list = filter_commentList(request, post_id, comment_page, loged_user.comment_listing)
            if (len(Comment.objects.filter(post=post_id).order_by('-upvotes')[
                    valor:valor + int(loged_user.comment_listing)]) > 0):
                context['load_button'] = True
    id = getattr(post, 'user_id')
    post_creator = get_object_or_404(User, pk=id)

    for comment in comment_list:
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (comment.upvoteList != None):
            upvoteList = jsonDec.decode(comment.upvoteList)
        if (comment.downvoteList != None):
            downvoteList = jsonDec.decode(comment.downvoteList)
        if (loged_user != None):
            if (loged_user.username in upvoteList):
                comment.was_upvoted = 1
            elif (loged_user.username in downvoteList):
                comment.was_downvoted = 1
    if 'utilizador_id' in request.session:
        context['id'] = loged_user.id
    context['comment_list'] = comment_list
    context['poster'] = post_creator
    context['youtube_url'] = getattr(post, 'youtube_url')
    context['comment_page'] = int(comment_page)
    if (post.image != 'notFound.png'):
        context['postWithImage'] = 'true'
    request.session['current_post'] = post_id
    template = loader.get_template('website/detalhe.html')
    return HttpResponse(template.render(context, request))


def filter_commentList(request, post_id, comment_page, preferences):
    valor = 0
    if (int(preferences) == 0):
        valor = 1000000000
    else:
        valor = int(preferences) + int(comment_page) * 20
    if (request.POST.get('comment_filter_list') == 'Newest comments'):
        return Comment.objects.filter(post=post_id).order_by('-comm_date')[:valor]
    elif (request.POST.get('comment_filter_list') == 'Most Downvoted'):
        return Comment.objects.filter(post=post_id).order_by('upvotes')[:valor]
    elif (request.POST.get('comment_filter_list') == 'Oldest comments'):
        return Comment.objects.filter(post=post_id).order_by('comm_date')[:valor]
    else:
        return Comment.objects.filter(post=post_id).order_by('-upvotes')[:valor]


def registo_user(request):
    return render(request, 'website/registo_user.html')


def grava_registo_user(request):
    template = loader.get_template('website/registo_user.html')
    if User.objects.filter(username=request.POST['username']).exists():
        context = {'username_ja_existente': 'true'}
        return HttpResponse(template.render(context, request))
    if User.objects.filter(username=request.POST['email']).exists():
        context = {'email_ja_existente': 'true'}
        return HttpResponse(template.render(context, request))
    else:
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        reg_date = timezone.now()
        validate = 0
        passwordConfirmation = request.POST['passwordConfirmation']
        bio = "My Bio"
        if not (len(email) > 6 and len(email) < 40):
            context = {'email_bad_size': 'true'}
            return HttpResponse(template.render(context, request))
            validate = validate + 1
        if not (len(username) > 5 and len(username) < 20):
            context = {'username_bad_size': 'true'}
            return HttpResponse(template.render(context, request))
            validate = validate + 1
        if not (len(password) > 8 and len(password) < 20):
            context = {'password_bad_size': 'true'}
            return HttpResponse(template.render(context, request))
            validate = validate + 1
        if not (password == passwordConfirmation):
            context = {'password_missmatch': 'true'}
            return HttpResponse(template.render(context, request))
            validate = validate + 1
        if (validate == 0):
            u = User(email=email, username=username, password=password, reg_date=reg_date, bio=bio,
                     avatar='user/noAvatar.png', comment_listing=20)
            u.save()
            return HttpResponseRedirect(reverse('website:index'))
        if (validate != 0):
            return HttpResponseRedirect(reverse('website:registo_user'))


def login(request):
    if User.objects.filter(username=request.POST['username']).exists():
        m = User.objects.get(username=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['utilizador_id'] = m.id
            return HttpResponseRedirect(reverse('website:index'))
        else:
            return render(request, 'website/login.html')
    else:
        return render(request, 'website/login.html')


def create_post(request):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        return render(request, 'website/create_post.html')


def comment_listing_edit(request):
    if (request.POST.get('comment_listing') == '20'):
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        user.comment_listing = 20
        user.save()
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))
    elif (request.POST.get('comment_listing') == '50'):
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        user.comment_listing = 50
        user.save()
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))
    elif (request.POST.get('comment_listing') == '100'):
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        user.comment_listing = 100
        user.save()
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))
    else:
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        user.comment_listing = 0
        user.save()
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))


def grava_novo_post(request):
    user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
    post = Post(user=user, title=request.POST['Title'], text=request.POST['Text'], post_date=timezone.now(), upvotes=0,
                topic=request.POST['Topic'], downvoteList=[], upvoteList=[], was_downvoted=0, was_upvoted=0,
                image='notFound.png', youtube_url="", preview_text=request.POST['Text'][:200], video_preview=0)
    if(len(request.POST['Text'])>200):
        post.preview_text=post.preview_text+"..."
    if request.method == 'POST':
        if request.POST.get('Imagem', True):
            post.image = request.FILES['Imagem']
        if request.POST.get('url', True):
            possible_url = request.POST['url']
            if (possible_url.startswith('<iframe width=')):
                url = re.search('src="(.+?)"', possible_url).group(1)
                post.youtube_url = url
                post.video_preview = 1
    post.save()
    return HttpResponseRedirect(reverse('website:index'))


def show_log_in(request):
    return render(request, 'Website/login.html')


def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('website:index'))


def submit_comment(request, post_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        post = get_object_or_404(Post, pk=post_id)
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        comment = Comment(user=user, post=post, text=request.POST['text'], comm_date=timezone.now(), upvotes=0,
                          downvoteList=[], upvoteList=[], was_downvoted=0, was_upvoted=0, post_title=post.title,
                          was_read=0, poster_username=user.username)
        comment.save()
        url = reverse('website:detalhe', kwargs={'post_id': post_id, 'comment_page': 0})
        return HttpResponseRedirect(url)


def upvote_post(request, post_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        username = user.username
        post = get_object_or_404(Post, pk=post_id)
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (post.upvoteList != None):
            upvoteList = jsonDec.decode(post.upvoteList)
        if (post.downvoteList != None):
            downvoteList = jsonDec.decode(post.downvoteList)
        user_existed = False
        if (downvoteList != None and downvoteList != []):
            if (username in downvoteList):
                user_existed = True
                iterador = 0
                for i in downvoteList:
                    if (i == username):
                        del downvoteList[iterador]
                        break
                    iterador = iterador + 1
        if ((upvoteList == None or upvoteList == []) and user_existed == False):
            upvoteList = [username]
            post.upvotes = post.upvotes + 1
        else:
            if ((upvoteList == None or upvoteList == []) and user_existed == True):
                upvoteList = [username]
                post.upvotes = post.upvotes + 2
            else:
                if (username in upvoteList):
                    post.upvotes = post.upvotes - 1
                    iterador = 0
                    for i in upvoteList:
                        if (i == username):
                            del upvoteList[iterador]
                            break
                        iterador = iterador + 1
                else:
                    if (user_existed == False):
                        post.upvotes = post.upvotes + 1
                    else:
                        post.upvotes = post.upvotes + 2
                    upvoteList.append(username)

    post.downvoteList = json.dumps(downvoteList)
    post.upvoteList = json.dumps(upvoteList)
    post.save()
    return HttpResponse(post.upvotes)


def downvote_post(request, post_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        username = user.username
        post = get_object_or_404(Post, pk=post_id)
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (post.upvoteList != None):
            upvoteList = jsonDec.decode(post.upvoteList)
        if (post.downvoteList != None):
            downvoteList = jsonDec.decode(post.downvoteList)
        user_existed = False
        if (upvoteList != None and upvoteList != []):
            if (username in upvoteList):
                user_existed = True
                iterador = 0
                for i in upvoteList:
                    if (i == username):
                        del upvoteList[iterador]
                        break
                    iterador = iterador + 1
        if ((downvoteList == None or downvoteList == []) and user_existed == False):
            downvoteList = [username]
            post.upvotes = post.upvotes - 1
        else:
            if ((downvoteList == None or downvoteList == []) and user_existed == True):
                downvoteList = [username]
                post.upvotes = post.upvotes - 2
            else:
                if (username in downvoteList):
                    post.upvotes = post.upvotes + 1
                    iterador = 0
                    for i in downvoteList:
                        if (i == username):
                            del downvoteList[iterador]
                            break
                        iterador = iterador + 1
                else:
                    if (user_existed == False):
                        post.upvotes = post.upvotes - 1
                    else:
                        post.upvotes = post.upvotes - 2
                    downvoteList.append(username)

    post.downvoteList = json.dumps(downvoteList)
    post.upvoteList = json.dumps(upvoteList)
    post.save()
    return HttpResponse(post.upvotes)


def upvote_comment(request, comment_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        username = user.username
        comment = get_object_or_404(Comment, pk=comment_id)
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (comment.upvoteList != None):
            upvoteList = jsonDec.decode(comment.upvoteList)
        if (comment.downvoteList != None):
            downvoteList = jsonDec.decode(comment.downvoteList)
        user_existed = False
        if (downvoteList != None and downvoteList != []):
            if (username in downvoteList):
                user_existed = True
                iterador = 0
                for i in downvoteList:
                    if (i == username):
                        del downvoteList[iterador]
                        break
                    iterador = iterador + 1
        if ((upvoteList == None or upvoteList == []) and user_existed == False):
            upvoteList = [username]
            comment.upvotes = comment.upvotes + 1
        else:
            if ((upvoteList == None or upvoteList == []) and user_existed == True):
                upvoteList = [username]
                comment.upvotes = comment.upvotes + 2
            else:
                if (username in upvoteList):
                    comment.upvotes = comment.upvotes - 1
                    iterador = 0
                    for i in upvoteList:
                        if (i == username):
                            del upvoteList[iterador]
                            break
                        iterador = iterador + 1
                else:
                    if (user_existed == False):
                        comment.upvotes = comment.upvotes + 1
                    else:
                        comment.upvotes = comment.upvotes + 2
                    upvoteList.append(username)

    comment.downvoteList = json.dumps(downvoteList)
    comment.upvoteList = json.dumps(upvoteList)
    comment.save()
    post_id = request.session.get('current_post')
    url = reverse('website:detalhe', kwargs={'post_id': post_id, 'comment_page': 0})
    return HttpResponse(comment.upvotes)


def downvote_comment(request, comment_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        username = user.username
        comment = get_object_or_404(Comment, pk=comment_id)
        jsonDec = json.decoder.JSONDecoder()
        upvoteList = None
        downvoteList = None
        if (comment.upvoteList != None):
            upvoteList = jsonDec.decode(comment.upvoteList)
        if (comment.downvoteList != None):
            downvoteList = jsonDec.decode(comment.downvoteList)
        user_existed = False
        if (upvoteList != None and upvoteList != []):
            if (username in upvoteList):
                user_existed = True
                iterador = 0
                for i in upvoteList:
                    if (i == username):
                        del upvoteList[iterador]
                        break
                    iterador = iterador + 1
        if ((downvoteList == None or downvoteList == []) and user_existed == False):
            downvoteList = [username]
            comment.upvotes = comment.upvotes - 1
        else:
            if ((downvoteList == None or downvoteList == []) and user_existed == True):
                downvoteList = [username]
                comment.upvotes = comment.upvotes - 2
            else:
                if (username in downvoteList):
                    comment.upvotes = comment.upvotes + 1
                    iterador = 0
                    for i in downvoteList:
                        if (i == username):
                            del downvoteList[iterador]
                            break
                        iterador = iterador + 1
                else:
                    if (user_existed == False):
                        comment.upvotes = comment.upvotes - 1
                    else:
                        comment.upvotes = comment.upvotes - 2
                    downvoteList.append(username)

    comment.downvoteList = json.dumps(downvoteList)
    comment.upvoteList = json.dumps(upvoteList)
    comment.save()
    post_id = request.session.get('current_post')
    url = reverse('website:detalhe', kwargs={'post_id': post_id, 'comment_page': 0})
    return HttpResponse(comment.upvotes)


def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    if (int(post_id) != 0):
        url = reverse('website:detalhe', kwargs={'post_id': post_id, 'comment_page': 0})
    else:
        return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))
    return HttpResponseRedirect(url)


def profile(request, comment_page):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        if (request.POST.get('load_button')):
            comment_page = int(comment_page) + 1
        template = loader.get_template('website/profile.html')
        user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
        context = {'user': user}
        if (int(user.comment_listing) == 0):
            comment_list = Comment.objects.filter(user_id=user.id).order_by('-comm_date')
            posts_list = Post.objects.filter(user_id=user.id).order_by('-post_date')
        else:
            valor = int(user.comment_listing) + int(comment_page) * int(user.comment_listing)
            comment_list = Comment.objects.filter(user_id=user.id).order_by('-comm_date')[:valor]
            posts_list = Post.objects.filter(user_id=user.id).order_by('-post_date')[:valor]
            if (len(Comment.objects.filter(user_id=user.id).order_by('-comm_date')[
                    valor:valor + int(user.comment_listing)]) > 0):
                context['load_comments_button'] = True
            if (len(Post.objects.filter(user_id=user.id).order_by('-post_date')[
                    valor:valor + int(user.comment_listing)]) > 0):
                context['load_posts_button'] = True
        context['comment_page'] = comment_page
        context['posts_list'] = posts_list
        context['comments_list'] = comment_list
        return HttpResponse(template.render(context, request))


def back_home(request):
    return HttpResponseRedirect(reverse('website:index'))


def grava_bio(request):
    user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
    user.bio = request.POST['bio']
    user.save()
    return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))


def change_data(request):
    user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
    if request.method == 'POST':
        if request.POST.get('Avatar', True):
            user.avatar = request.FILES['Avatar']
    if request.POST['email']:
        user.email = request.POST['email']
    user.save()
    return HttpResponseRedirect(reverse('website:profile', kwargs={'comment_page': 0}))


def others_profile(request, user_id, comment_page):
    template = loader.get_template('website/others_profile.html')
    loged_user = None
    comments_list = []
    posts_list = []
    if request.POST.get('load_button'):
        comment_page = int(comment_page) + 1
    valor = 0
    if 'utilizador_id' in request.session:
        loged_id = request.session.get('utilizador_id')
        loged_user = get_object_or_404(User, pk=loged_id)
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    if (loged_user == None):
        valor = 20 + int(comment_page) * 20
        comments_list = Comment.objects.filter(user_id=user_id).order_by('-comm_date')[:valor]
        posts_list = Post.objects.filter(user_id=user_id).order_by('-post_date')[:valor]
        if request.POST.get('comment_list_filter'):
            dict = filter_otherProfile(request, user_id, comment_page, valor)
            comments_list = dict['comments_list']
            posts_list = dict['posts_list']
        if (len(Comment.objects.filter(user_id=user_id)[valor:valor + 20]) > 0):
            context['load_button'] = True
        if (len(Post.objects.filter(user_id=user_id)[valor:valor + 20]) > 0):
            context['load_post_button'] = True
    else:
        if (int(loged_user.comment_listing) == 0):
            comments_list = Comment.objects.filter(user_id=user_id).order_by('-comm_date')
            posts_list = Post.objects.filter(user_id=user_id).order_by('-post_date')
            if request.POST.get('comment_list_filter'):
                dict = filter_otherProfile(request, user_id, comment_page, 0)
                posts_list = dict['posts_list']
                comments_list = dict['comments_list']
        else:
            valor = loged_user.comment_listing + int(comment_page) * int(loged_user.comment_listing)
            comments_list = Comment.objects.filter(user_id=user_id).order_by('-comm_date')[:valor]
            posts_list = Post.objects.filter(user_id=user_id).order_by('-post_date')[:valor]
            if request.POST.get('comment_list_filter'):
                dict = filter_otherProfile(request, user_id, comment_page, valor)
                posts_list = dict['posts_list']
                comments_list = dict['comments_list']
            if (len(Comment.objects.filter(user_id=user_id)[valor:valor + int(loged_user.comment_listing)]) > 0):
                context['load_button'] = True
            if (len(Post.objects.filter(user_id=user_id)[valor:valor + int(loged_user.comment_listing)]) > 0):
                context['load_post_button'] = True
    context['comment_page'] = comment_page
    context['user_id'] = user_id
    context['comments_list'] = comments_list
    context['posts_list'] = posts_list
    return HttpResponse(template.render(context, request))


def filter_otherProfile(request, user_id, comment_page, preferences):
    valor = 0
    if (int(preferences) == 0):
        valor = 1000000000
    else:
        valor = int(preferences) + int(comment_page) * 20
    if (request.POST.get('comment_list_filter') == 'Newest'):
        dict = {'comments_list': Comment.objects.filter(user_id=user_id).order_by('-comm_date')[:valor]}
        dict['posts_list'] = Post.objects.filter(user_id=user_id).order_by('-post_date')[:valor]
        return dict
    elif (request.POST.get('comment_list_filter') == 'Most downvoted'):
        dict = {'comments_list': Comment.objects.filter(user_id=user_id).order_by('upvotes')[:valor]}
        dict['posts_list'] = Post.objects.filter(user_id=user_id).order_by('upvotes')[:valor]
        return dict
    elif (request.POST.get('comment_list_filter') == 'Oldest'):
        dict = {'comments_list': Comment.objects.filter(user_id=user_id).order_by('comm_date')[:valor]}
        dict['posts_list'] = Post.objects.filter(user_id=user_id).order_by('post_date')[:valor]
        return dict
    else:
        dict = {'comments_list': Comment.objects.filter(user_id=user_id).order_by('-upvotes')[:valor]}
        dict['posts_list'] = Post.objects.filter(user_id=user_id).order_by('-upvotes')[:valor]
        return dict


def message_box(request, comment_page):
    template = loader.get_template('website/message_box.html')
    user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
    if (request.POST.get('load_button')):
        comment_page = int(comment_page) + 1
    context = {'user': user}
    context['response_list'] = []
    context['response_list_final'] = []
    context['unread_response_list'] = []
    context['unread_message_list'] = []
    post_list = Post.objects.filter(user_id=user.id).order_by('-post_date')
    if (int(user.comment_listing) == 0):
        message_list = Message.objects.filter(receiver_user_id=user.id).order_by('-mess_date')
    else:
        valor = int(user.comment_listing) + int(comment_page) * int(user.comment_listing)
        message_list = Message.objects.filter(receiver_user_id=user.id).order_by('-mess_date')[:valor]
        if (len(Message.objects.filter(receiver_user_id=user.id).order_by('-mess_date')[
                valor:valor + int(user.comment_listing)]) > 0):
            context['load_messages_button'] = True
    valor = int(user.comment_listing) + int(comment_page) * int(user.comment_listing)
    for p in post_list:
        context['response_list'].append(Comment.objects.filter(post_id=p.id).order_by('-comm_date'))
    for l in context['response_list']:
        for c in l:
            m = get_object_or_404(Comment, pk=c.id)
            if (m.was_read == 0):
                context['unread_response_list'].append(c)
                m.was_read = 1
                m.save()
    for l in context['response_list']:
        done = False
        for c in l:
            m = get_object_or_404(Comment, pk=c.id)
            context['response_list_final'].append(m)
            valor = valor - 1
            if (valor == 0):
                context['load_responses_button'] = True
                done = True
                break
        if (done == True):
            break
    context['message_list'] = message_list
    context['comment_page'] = comment_page
    for m in context['message_list']:
        if (m.was_read == 0):
            context['unread_message_list'].append(m)
            m.was_read = 1
            m.save()
    return HttpResponse(template.render(context, request))


def send_message(request, user_id):
    if 'utilizador_id' not in request.session:
        return render(request, 'website/login.html')
    else:
        template = loader.get_template('website/send_message.html')
        context = {'user_receiver_id': user_id}
        return HttpResponse(template.render(context, request))


def grava_nova_mensagem(request, user_id):
    loged_user = get_object_or_404(User, pk=request.session.get('utilizador_id'))
    target_user = get_object_or_404(User, pk=user_id)
    context = {'loged_user': loged_user}
    context['target_user'] = target_user
    m = Message(receiver_user_id=target_user.id, subject=request.POST['Subject'], text=request.POST['Text'],
                mess_date=timezone.now(), sender_user_id=loged_user.id, was_read=0,
                sender_user_username=loged_user.username)
    m.save()
    return HttpResponseRedirect(reverse('website:index'))
