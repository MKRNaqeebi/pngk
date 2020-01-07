from django.conf.urls import url
from AudioCall import views


urlpatterns = [
    url(r'^PRBox$', views.my_box, name='PRBox'),
    url(r'^Contact$', views.contact_us, name='Contact'),
    url(r'^$', views.index, name='index'),
    url(r'^NoAnswer$', views.no_answer, name='NoAnswer'),
    url(r'^ConferenceStatus/(?P<call_sid>[-\w]+)$', views.conference_status, name=''),
    url(r'^Conference/(?P<conference_name>[-\w]+)$', views.join_conference, name=''),
    url(r'^AddDrop$', views.add_drop, name=''),
    url(r'^VoiceFour$', views.voice_four, name=''),
    url(r'^VoiceThree$', views.voice_three, name=''),
    url(r'^VoiceTwo$', views.voice_two, name=''),
    url(r'^voice$', views.voice, name='voice'),
]
