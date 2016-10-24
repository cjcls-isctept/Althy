from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'website'
urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^filter/$', views.filter_topic,name='filtro'),
    url(r'^trending/$', views.filter_trending,name='trending'),
    url(r'^new/$', views.filter_new,name='new'),
    url(r'^registo_user/$', views.registo_user, name="registo_user"),
    url(r'^grava_registo_user/$', views.grava_registo_user, name="grava_registo_user"),
    url(r'^(?P<post_id>[0-9]+)/(?P<comment_page>[0-9]+)/$',views.detalhe, name='detalhe'),
    url(r'^(?P<post_id>[0-9]+)/(?P<refresh_identifier>[0-9]+)/delete_post/$',views.delete_post, name='delete_post'),
    url(r'^create_post/$',views.create_post,name='create_post'),
    url(r'^grava_novo_post/$',views.grava_novo_post,name='grava_novo_post'),
    url(r'^show_login/$', views.show_log_in, name="show_log_in"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$',views.logout,name="logout"),
    url(r'^(?P<post_id>[0-9]+)/submit_comment/$',views.submit_comment,name="submit_comment"),
    url(r'^(?P<post_id>[0-9]+)/upvote_post/$',views.upvote_post,name="upvote_post"),
    url(r'^(?P<post_id>[0-9]+)/downvote_post/$',views.downvote_post,name="downvote_post"),
    url(r'^(?P<comment_id>[0-9]+)/upvote_comment/$',views.upvote_comment,name="upvote_comment"),
    url(r'^(?P<comment_id>[0-9]+)/downvote_comment/$',views.downvote_comment,name="downvote_comment"),
    url(r'^(?P<comment_id>[0-9]+)/(?P<post_id>[0-9]+)/delete_comment/$',views.delete_comment,name="delete_comment"),
    url(r'^(?P<comment_page>[0-9]+)/profile/$',views.profile, name='profile'),
    url(r'^back_home/$', views.back_home, name='back_home'),
    url(r'^grava_bio/$',views.grava_bio, name='grava_bio'),
    url(r'^change_data/$',views.change_data, name='change_data'),
    url(r'^(?P<user_id>[0-9]+)/(?P<comment_page>[0-9]+)/profile/$',views.others_profile,name="others_profile"),
    url(r'^(?P<comment_page>[0-9]+)/message_box/$', views.message_box, name='message_box'),
    url(r'^(?P<user_id>[0-9]+)/send_message/$',views.send_message,name='send_message'),
    url(r'^(?P<user_id>[0-9]+)/grava_nova_mensagem/$',views.grava_nova_mensagem,name='grava_nova_mensagem'),
    url(r'^(?P<actual_page>[0-9]+)/new/$',views.next_new_page, name='next_new_page'),
    url(r'^(?P<actual_page>[0-9]+)/new2/$',views.previous_new_page, name='previous_new_page'),
    url(r'^(?P<actual_page>[0-9]+)/trending/$',views.next_trending_page, name='next_trending_page'),
    url(r'^(?P<actual_page>[0-9]+)/trending2/$',views.previous_trending_page, name='previous_trending_page'),
    url(r'^(?P<actual_page>[0-9]+)/hot/$',views.next_hot_page, name='next_hot_page'),
    url(r'^(?P<actual_page>[0-9]+)/hot2/$',views.previous_hot_page, name='previous_hot_page'),
    url(r'^comment_listing_edit/$', views.comment_listing_edit, name="comment_listing_edit"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)