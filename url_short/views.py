from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django_user_agents.utils import get_user_agent
import random, string

from django.http import JsonResponse
from django.db.models import Q

from .forms import linkForm, jsUseragentForm
from .models import linksModel, pythonUseragentModel, jsUseragentModel



def create(request):
    short = ''
    already_exists = False
        # Reciving the POST request

    if request.method =='POST':
        form = linkForm(request.POST)
        if form.is_valid():
            windows = form.cleaned_data['windowsURL']
            android = form.cleaned_data['androidURL']
            mac = form.cleaned_data['macURL']
            ios = form.cleaned_data['iosURL']
            other = form.cleaned_data['otherURL']
            short = request.POST.get('shortURL')

        
            if linksModel.objects.filter(shortURL=short).count() == 0:

                if short == "" or short == None:
                    short = create_token()
                    if linksModel.objects.filter(shortURL=short).count() != 0:
                        short = create_token()

            # to not have an empty field saved to db
                if other == '' or other ==' ':  
                    other = 'https://google.com'
                    
                if android == '':
                    android = other
                
                if mac == '':
                    mac = other
                
                if ios == '':
                    ios = other

                if windows =='':
                    windows = other
                

                save_to_db = linksModel(windowsURL=windows,shortURL=short,androidURL=android,macURL=mac,iosURL=ios,otherURL=other)
                save_to_db.save()
            else: 
                short = 'Already There'
                already_exists = True

        else:
            short = 'an error happened!'
            # form = linkForm()

    context = {
        'form':linkForm(),
        'message':short,
        'exists':already_exists
    }
    return render(request, "url_short/create_url.html", context)
    
   # nice !

def view(request): 

    searchingLink=''
    searchingPy = '' 
    searchingJs = ''

    if 'srchLink' in request.GET:
        srchLink = request.GET['srchLink']
        multiSearchLink = Q(Q(shortURL__icontains=srchLink) | Q(created_time__icontains=srchLink))
        linkData = linksModel.objects.filter(multiSearchLink)

        searchingLink = 'Searching... Clear the fliter for all of the results'        

    else:
        linkData = linksModel.objects.all()
    


    if 'srchPy' in request.GET:
        srchPy = request.GET['srchPy']
        multiSearchPy = Q(Q(ip__icontains=srchPy) | Q(os_type__icontains=srchPy))
        pyData = pythonUseragentModel.objects.filter(multiSearchPy)
        searchingPy = 'Searching... Clear the fliter for all of the results'

    else:
        pyData = pythonUseragentModel.objects.all()

    
    if 'srchJs' in request.GET:
        srchJs = request.GET['srchJs']
        multiSearchJs = Q(Q(browser_version__icontains=srchJs))
        jsData = jsUseragentModel.objects.filter(multiSearchJs)
        searchingJs = 'Searching... Clear the fliter for all of the results'

    else:
        jsData = jsUseragentModel.objects.all()

    

    context={
        'links': linkData,
        'pythonInfo':pyData,
        'jsInfo':jsData,
        'searchingLink':searchingLink,
        'searchingPy':searchingPy,
        'searchingJs':searchingJs,
    }
    
    return render(request, "main_view.html",context) 

   

# idd is id
def edit(request,idd):
    link = linksModel.objects.get(id=idd)
    return render(request,'url_short/edit_url.html',{'link':link})

def update(request,idd):
    link = linksModel.objects.get(id=idd)
    form = linkForm(request.POST,instance=link)
    msg = ''
    already_exists = False

    if form.is_valid():
        shortie = request.POST.get('short_url')
        windows = request.POST.get('windows_url')
        android = request.POST.get('android_url')
        mac = request.POST.get('mac_url')
        ios = request.POST.get('ios_url')
        other = request.POST.get('other_url')


        if linksModel.objects.filter(shortURL=shortie).count() == 0 or shortie == link.shortURL:
            if other == '' or other ==' ':
                other = 'https://google.com'
                
            if android == '':
                android = other
            
            if mac == '':
                mac = other
            
            if ios == '':
                ios = other

            if windows =='':
                windows = other
                
            if shortie == "" or shortie == ' ':
                shortie = link.shortURL


            link.shortURL = shortie
            link.windowsURL = windows
            link.androidURL = android
            link.macURL = mac
            link.iosURL = ios
            link.otherURL = other

            link.save()
            return redirect('urls:view')
        
        else:
            msg = 'already there'
            already_exists = True

    context = {
        'link':link,
        'msg' : msg,
        'exists' : already_exists,
    }

    return render(request,'url_short/edit_url.html',context)

def delete(request,idd):
    link = linksModel.objects.get(id=idd)
    link.delete()
    return redirect('urls:view')


def redirector(request,token):

    if linksModel.objects.filter(shortURL=token).count() == 0:
        urls = linksModel.objects.first()
        redirected_url = "https://google.com"

    else:

        urls = linksModel.objects.filter(shortURL = token)[0]

        os = str(request.user_agent.os.family)
        redirected_url = ""

        if os.lower() == 'windows':
            redirected_url = urls.windowsURL

        if os.lower() == 'android':
            redirected_url = urls.androidURL

        if os.lower() == 'mac os x':
            redirected_url = urls.macURL

        if os.lower() == 'ios':
            redirected_url = urls.iosURL
        else: 
            redirected_url = urls.otherURL

        # taking the information from userData function and saving it to pythonUseragentModel 
    userInfo = userData(request)

    save_to_db = pythonUseragentModel(incoming_link=urls,ip=userInfo['ip'],browser_type=userInfo['browser_type'],browser_version=userInfo['browser_version'],os_type=userInfo['os_type'],os_version=userInfo['os_version'],device_family=userInfo['device_family'],)
    save_to_db.save()
        
    # sending the link to HTML to redirect there || doing that to be able to run the javascript file to get the javascript useragent info   
    return render(request, 'jsinfo.html',{'redirect_url':redirected_url},)

def userData(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    device_type = request.user_agent.device.family
    context = {
        "ip": ip,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version":os_version,
        "device_family": device_type
    }
    return context


def create_token():
    token_size = 5
    letters = string.ascii_letters
    return "".join (random.choice(letters)for i in range (token_size))


def receive_js(request):
    form = jsUseragentForm(request.POST or None)

    if is_ajax(request = request):
        if form.is_valid():
            browser_codeName= form.cleaned_data['browser_codeName']
            browser_version= form.cleaned_data['browser_version']
            browser_language= form.cleaned_data['browser_language']
            cookies_enabled= form.cleaned_data['cookies_enabled']
            platform= form.cleaned_data['platform']
            user_agent_header= form.cleaned_data['user_agent_header']
            timezone_utc= form.cleaned_data['timezone_utc']
            timezone_place= form.cleaned_data['timezone_place']
            screen_size= form.cleaned_data['screen_size']
            battery_level= form.cleaned_data['battery_level']

            pyID = request.POST.get('pyID')

            if pyID =="None":
                pyinfo = pythonUseragentModel.objects.last()
            else:
                pyinfo = pythonUseragentModel.objects.filter(id = pyID).first()

            save_to_db = jsUseragentModel(browser_codeName=browser_codeName,browser_version=browser_version,browser_language=browser_language,cookies_enabled=cookies_enabled,platform=platform,user_agent_header=user_agent_header,timezone_utc=timezone_utc,timezone_place=timezone_place,screen_size=screen_size,battery_level=battery_level,pyID=pyinfo)
            save_to_db.save()
            return "" 
        return ""


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'