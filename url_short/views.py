from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django_user_agents.utils import get_user_agent

from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import random, string
import csv

from django.http import JsonResponse
from django.db.models import Q

from .forms import linkForm, jsUseragentForm
from .models import linksModel, pythonUseragentModel, jsUseragentModel


@login_required(login_url='urls:login')
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
            notes = form.cleaned_data['notes']
            short = request.POST.get('shortURL')
            password = request.POST.get('urlPass')
            rangeSlider = request.POST.get('rangeSlider')

            rangeSlider = int(rangeSlider)
            max_len = 5
            if rangeSlider <= 50 and rangeSlider >0:
                max_len = rangeSlider
                print('h')

            if linksModel.objects.filter(shortURL=short).count() == 0:
                if short == "" or short == None:                        
                    short = create_token(max_len)
                    if linksModel.objects.filter(shortURL=short).count() != 0:
                        short = create_token(max_len)
                        if linksModel.objects.filter(shortURL=short).count() != 0:
                            short = create_token(max_len)                        


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

                save_to_db = linksModel(windowsURL=windows,shortURL=short,androidURL=android,macURL=mac,iosURL=ios,otherURL=other,notes=notes,password=password)
                save_to_db.save()
            else: 
                short = 'Already There'
                already_exists = True

        else:
            short = 'an error happened!'
# nice !

    context = {
        'form':linkForm(),
        'message':short,
        'exists':already_exists
    }
    return render(request, "url_short/create_url.html", context)
    

@login_required(login_url='urls:login')
def view(request): 

    searchingLink=''
    searchingPy = '' 
    searchingJs = ''

    if 'srchLink' in request.GET:
        srchLink = request.GET['srchLink']
        multiSearchLink = Q(Q(shortURL__icontains=srchLink) | Q(created_time__icontains=srchLink) | Q(notes__icontains=srchLink))
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
@login_required(login_url='urls:login')
def edit(request,idd):
    link = linksModel.objects.get(id=idd)
    return render(request,'url_short/edit_url.html',{'link':link})

@login_required(login_url='urls:login')
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
        notes = request.POST.get('notes')


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
            # return redirect('urls:view')
            

    context = {
        'link':link,
        'msg' : msg,
        'exists' : already_exists,
    }

    return render(request,'url_short/edit_url.html',context)
@login_required(login_url='urls:login')
def delete(request,idd):
    link = linksModel.objects.get(id=idd)
    link.delete()
    return redirect('urls:view')


def redirector(request,token):
    passworded = False

    if linksModel.objects.filter(shortURL=token).count() == 0:
        redirected_url = "https://google.com"
        current_id = 0
        

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

        if urls.password:
            passworded= True

        save_to_db = pythonUseragentModel(incoming_link=urls,ip=userInfo['ip'],browser_type=userInfo['browser_type'],browser_version=userInfo['browser_version'],os_type=userInfo['os_type'],os_version=userInfo['os_version'],device_family=userInfo['device_family'],)
        save_to_db.save()
        current_id = save_to_db.id


    if not passworded:
            # sending the link to HTML to redirect there || doing that to be able to run the javascript file to get the javascript useragent info   
        return render(request, 'jsinfo.html',{'redirect_url':redirected_url,'cID':current_id},)
    else:
        return render(request, 'jsinfowP.html',{'cID':current_id,'pswd':'p'})


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



def loginn(request):
    if request.user.is_authenticated:
        return redirect('urls:view')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username= username,password=password)
            if user is not None:
                login(request, user)
                return redirect('urls:view')
            else:
                messages.info(request, 'wrong creds')
        return render(request,'login.html')


def logoutt(request):
    logout(request)
    return redirect('urls:login')


def create_token(size):
    token_size = size
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
        return JsonResponse({'data':'done'},status=200)


def receive_p(request):
    if is_ajax(request=request):
        pswd = request.POST.get('pswd')
        pyID = request.POST.get('pyID')
        entry = pythonUseragentModel.objects.get(id=pyID)

        dbPswd = entry.incoming_link.password
        if pswd == dbPswd:
            entry.knowPassword = True
            entry.save()
            
            redirected_url = ""
            os = str(request.user_agent.os.family)

            if os.lower() == 'windows':
                redirected_url = entry.incoming_link.windowsURL

            if os.lower() == 'android':
                redirected_url = entry.incoming_link.androidURL

            if os.lower() == 'mac os x':
                redirected_url = entry.incoming_link.macURL

            if os.lower() == 'ios':
                redirected_url = entry.incoming_link.iosURL
            else: 
                redirected_url = entry.incoming_link.otherURL

            # redirecting in js
            return JsonResponse({'data':redirected_url},status=200)
            
        else:
            entry.knowPassword = False
            entry.save()
            return JsonResponse({'data':'fail'},status=200)

        


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='urls:login')
def export(request):
    linkData = linksModel.objects.all()
    pyData = pythonUseragentModel.objects.all()
    jsData = jsUseragentModel.objects.all()

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    writer.writerow(['id','shortURL','windowsURL','macURL','androidURL','iosURL','otherURL','created_time','notes'])
    for link in linkData:
        writer.writerow([link.id, link.shortURL,link.windowsURL,link.macURL,link.androidURL,link.iosURL,link.otherURL,link.created_time,link.notes])


    writer.writerow(['','','','','','','','','','','','','','']) #14
    writer.writerow(['','','','','','','','','','','','','','']) #14
    writer.writerow(['','','','','','','','','','','','','','']) #14
   
    writer.writerow(['id','ip','browser_type','browser_version','os_type','os_version','device_family','incoming_link','created_time'])
    for pinfo in pyData:
        writer.writerow([pinfo.id,pinfo.ip, pinfo.browser_type, pinfo.browser_version,pinfo.os_type,pinfo.os_version,pinfo.device_family,pinfo.incoming_link.shortURL,pinfo.created_time])


    writer.writerow(['','','','','','','','','','','','','','']) #14
    writer.writerow(['','','','','','','','','','','','','','']) #14
    writer.writerow(['','','','','','','','','','','','','','']) #14
   
    writer.writerow(['id','Browser Name ','Browser Version','Browser Language','Cookies Enabled','Operating System','Useragent Header','UTC TimeZone','TZ Place','Screen Size','Battery Level','PreTable Connection','incoming link','Clicking Time'])
    for jinfo in jsData:
        writer.writerow([jinfo.id,jinfo.browser_codeName,jinfo.browser_version,jinfo.browser_language,jinfo.cookies_enabled,jinfo.platform,jinfo.user_agent_header,jinfo.timezone_utc,jinfo.timezone_place,jinfo.screen_size,jinfo.battery_level,jinfo.pyID.id,jinfo.pyID.incoming_link.shortURL,jinfo.created_time])


    response ['Content-Disposition'] = 'attachment; filename= "data.csv"'
    return response
@login_required(login_url='urls:login')
def nuke(request):
    jsUseragentModel.objects.all().delete()
    pythonUseragentModel.objects.all().delete()
    linksModel.objects.all().delete()
    return redirect('urls:view')

