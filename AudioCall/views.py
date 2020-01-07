from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
from twilio.rest import Client
import smtplib
from .models import CallDetail
from .forms import ContactForm
from django.views.decorators.csrf import csrf_exempt


BASE_URL = 'https://mkrnaqeebi.herokuapp.com'

account_sid = "xxx"
auth_token = "xxx"
client = Client(account_sid, auth_token)
eric = '+31615660356'  # my client I have build this thing for 

num_sendCallTo = eric

EMAIL_USER = 'kamranlhr94@gmail.com'
EMAIL_PASSWORD = 'xxx'
EMAIL_RECIPIENT = ['kamranlhr94@gmail.com', 'EricCBonet@gmail.com']   # second enmail my client I have build this thing for 

# Create your views here.


def contact_us(request):
    """
    Handle and submit contact form with POST
    """
    form = ContactForm(request.POST, None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    template = loader.get_template('contact.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


def my_box(request):
    """
    Show 5 call details
    """
    calls_detail = CallDetail.objects.all()
    if len(calls_detail) > 5:
        calls_detail = calls_detail[:5]
    template = loader.get_template('box.html')
    context = {
        'calls_detail': calls_detail
    }
    return HttpResponse(template.render(context, request))


def index(request):
    """
    Render index page
    """
    template = loader.get_template('index.html')
    context = {
        'title': "Home",
    }
    return HttpResponse(template.render(context, request))


def send_email(subject, body):
    """
    Send Email

    :param string subject: Subject of email
    :param string body: body of email
    """
    FROM = EMAIL_USER
    TO = EMAIL_RECIPIENT if type(EMAIL_RECIPIENT) is list else [EMAIL_RECIPIENT]
    SUBJECT = subject
    TEXT = body

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(FROM, TO, message)
    server.close()


@csrf_exempt
def no_answer(request):
    """
    If bussiness owner is busy and could not able to receive call send hime email so he can call later
    and play message no answer
    """
    call_sid = None
    if request.method == 'POST':
        call_sid = request.POST.get('myCallSid', None)
    if request.method == 'GET':
        call_sid = request.GET.get('myCallSid', None)
    my_call = client.calls(call_sid).fetch()
    subject = 'You missed a call from ' + my_call.from_
    body = 'You missed a call on ' + my_call.to + ' from ' + my_call.from_ + ' at ' + str(my_call.end_time)
    send_email(subject, body)
    resp = VoiceResponse()
    resp.play('http://roelofvandijk.com/mp33/IVR/NoAnswer.mp3')
    resp.hangup()
    return HttpResponse(str(resp))


@csrf_exempt
def conference_status(request, call_sid):
    """
    Get or send conference status
    """
    resp = VoiceResponse()
    call_status = None
    if request.method == 'POST':
        call_status = request.POST.get('CallStatus', None)
    if request.method == 'GET':
        call_status = request.GET.get('CallStatus', None)
    if call_status == 'completed':
        client.calls.hangup(call_sid)
    if call_status == 'no-answer' or call_status == 'busy' or call_status == 'failed':
        call = client.calls(call_sid).update(
            method="POST",
            url=BASE_URL + "/NoAnswer?myCallSid="+call_sid
        )
        print(call.to)
    return HttpResponse(str(resp))


@csrf_exempt
def join_conference(request, conference_name):
    """
    If request comes in join coinference
    """
    resp = VoiceResponse()
    resp.dial(hangupOnStar=True).conference(conference_name)
    return HttpResponse(str(resp))


@csrf_exempt
def add_drop(request):
    """
    Add or drop from call a participant
    """
    call_sid = None
    call_status = None
    if request.method == 'POST':
        call_sid = request.POST.get('CallSid', None)
        call_status = request.POST.get('StatusCallbackEvent', None)
    if request.method == 'GET':
        call_sid = request.GET.get('CallSid', None)
        call_status = request.GET.get('StatusCallbackEvent', None)
    resp = VoiceResponse()
    if call_status == 'conference-end':
        client.calls.hangup(call_sid)
    resp.play('http://roelofvandijk.com/mp33/IVR/NoAnswer.mp3')
    return HttpResponse(str(resp))


@csrf_exempt
def voice_four(request):
    """
    Play voice 4 and do actions accordingly
    """
    call_sid = None
    choice = None
    call_from = None
    if request.method == 'POST':
        call_sid = request.POST.get('CallSid', None)
        choice = request.POST.get('Digits', None)
        call_from = request.POST.get('From', None)
    if request.method == 'GET':
        call_sid = request.GET.get('CallSid', None)
        choice = request.GET.get('Digits', None)
        call_from = request.GET.get('From', None)
    twiml = VoiceResponse()
    if choice:
        call_detail = CallDetail.objects.get(call_sid=call_sid)
        call_detail.went_conference = True
        call_detail.save()
        if int(choice) == 1:
            client.calls.create(to=num_sendCallTo, from_=num_sendCallTo, url=BASE_URL + '/Conference/' + call_sid,
                                status_callback=BASE_URL+'/ConferenceStatus/' + call_sid,
                                status_callback_method='POST', status_callback_event=["completed", "no-answer", "busy",
                                                                                      "failed"])
            dial = Dial()
            dial.conference(call_sid, wait_url='http://roelofvandijk.com/mp33/IVR/CallingInformation.mp3',
                            status_callback=BASE_URL+'/AddDrop?CallSid=' + call_sid + '&From='+call_from,
                            status_callback_method='POST', status_callback_event=['start', 'join', 'end'],
                            end_conference_on_exit=True, max_participants=2, start_conference_on_enter=True)
            twiml.append(dial)
            return HttpResponse(str(twiml))
        twiml.hangup()
        return HttpResponse(str(twiml))
    return HttpResponse(str(twiml))


@csrf_exempt
def voice_three(request):
    """
    Play voice 3 and do actions accordingly
    """
    call_sid = None
    recording_url = None
    if request.method == "POST":
        call_sid = request.POST.get('CallSid', None)
        recording_url = request.POST.get('RecordingUrl', None)
    if request.method == "GET":
        call_sid = request.GET.get('CallSid', None)
        recording_url = request.GET.get('RecordingUrl', None)

    if recording_url:
        call_detail = CallDetail.objects.get(call_sid=call_sid)
        call_detail.comment = recording_url
        call_detail.save()
    twiml = VoiceResponse()
    gather = Gather(num_digits=1, action='/VoiceFour')
    gather.play('http://roelofvandijk.com/mp33/IVR/PNGK-speakOrEndCall.mp3')
    twiml.append(gather)
    return HttpResponse(str(twiml))


@csrf_exempt
def voice_two(request):
    """
    Play voice 2 and do actions accordingly
    """
    call_sid = None
    recording_url = None

    if request.method == "POST":
        call_sid = request.POST.get('CallSid', '')
        recording_url = request.POST.get('RecordingUrl', None)
    if request.method == "GET":
        call_sid = request.GET.get('CallSid', '')
        recording_url = request.GET.get('RecordingUrl', None)
    if recording_url:
        call_detail = CallDetail.objects.get(call_sid=call_sid)
        call_detail.country_name = recording_url
        call_detail.save()
    resp = VoiceResponse()
    resp.play('http://roelofvandijk.com/mp33/IVR/ThanksComments.mp3')
    resp.record(method='GET', max_length=10, action='/VoiceThree', timeout=15)
    return HttpResponse(str(resp))


@csrf_exempt
def voice(request):
    """
    Play voice where are you from and save voice
    """
    call_sid = None
    call_from = None
    if request.method == "POST":
        call_sid = request.POST.get('CallSid', None)
        call_from = request.POST.get('From', None)
    elif request.method == "GET":
        call_sid = request.GET.get('CallSid', None)
        call_from = request.GET.get('From', None)
    if call_from:
        call_detail = CallDetail(call_sid=call_sid, call_from=call_from)
        call_detail.save()
    resp = VoiceResponse()
    resp.play('http://roelofvandijk.com/mp33/IVR/PNGK-whereAreYouFrom.mp3')
    resp.record(method='GET', max_length=5, action='/VoiceTwo', timeout=15)
    # resp.play('http://roelofvandijk.com/mp33/IVR/Thank-You-IVR.mp3')
    return HttpResponse(str(resp))
