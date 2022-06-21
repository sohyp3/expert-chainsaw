from django.db import models

class linksModel(models.Model):
    shortURL = models.CharField(max_length=10,unique=True)
    windowsURL = models.URLField("Windows", blank= True)
    macURL = models.URLField("Mac OS", blank= True)
    androidURL = models.URLField("Android", blank= True)
    iosURL = models.URLField("IOS", blank= True)
    otherURL = models.URLField("Others", blank= True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
          return f'short url : {self.shortURL} \nwindows link {self.windowsURL}\nandroid link {self.androidURL}\nmac link {self.macURL}\nios link {self.iosURL}\nothers {self.otherURL} '

class pythonUseragentModel(models.Model):
    ip = models.CharField(max_length=20)
    browser_type = models.CharField(max_length=50)
    browser_version = models.CharField(max_length=50)
    os_type = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50)
    device_family = models.CharField(max_length=50)
    incoming_link = models.ForeignKey(linksModel, on_delete=models.PROTECT,related_name="pythonInfo")
    created_time = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"{self.ip} , {self.incoming_link}"
    
class jsUseragentModel(models.Model):
    browser_codeName = models.CharField(max_length=200)
    browser_version = models.CharField(max_length=200)
    browser_language = models.CharField(max_length=200)
    cookies_enabled = models.CharField(max_length=200)
    platform = models.CharField(max_length=200)
    user_agent_header = models.CharField(max_length=200)
    timezone_utc = models.CharField(max_length=10)
    timezone_place = models.CharField(max_length=50)
    screen_size = models.CharField(max_length = 15)
    battery_level = models.CharField(max_length=5,blank=True)
    
    
    pyID = models.ForeignKey(pythonUseragentModel, on_delete=models.PROTECT,related_name="jsInfo",blank=True)

    # incoming_link = models.ForeignKey(linksModel, on_delete=models.PROTECT,related_name="jsInfoo",blank=True)
    created_time = models.DateTimeField(auto_now_add=True,)


    
    def __str__(self):
        return f"{self.user_agent_header}"
    
