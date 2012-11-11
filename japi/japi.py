#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2
import simplejson as json
from debug import debug

class Phonty():
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        )

    def __init__(self):
        self.url = "http://phonty.com/japi/"
        self.opener.addheaders = [('User-agent', 'Phonty-Android-Client')]
        self.error = None

    def login(self, login, password):
        url = self.url + "login/"
        try:
            data = urllib.urlencode(
                                {'username': str(login),
                                 'password': str(password)})
        except:
            data = None
        request = urllib2.Request(url, data)
        response = self.send(request)
        if response == "AUTH_OK":
            return True
        else:
            self.error = response
            return False

    def balance(self,locale ="US"):
        url = self.url + "balance/"
        data = urllib.urlencode({'locale': locale})
        request = urllib2.Request(url,data)
        try:
            response = json.loads(self.send(request))["balance"]
        except KeyError,e:
            response = '0.0'
        return response

    def version(self):
        url = self.url + "version/"
        request = urllib2.Request(url)
        try:
            response = json.loads(self.send(request))["version"]
        except KeyError,e:
            response = '0.0.0'
        return response


    def direction_cost(self,phone,locale):
        url = self.url + "directioncost/"
        data = urllib.urlencode({'phone':str(phone),'locale': locale})
        request = urllib2.Request(url, data)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = '0.0'
        return response

    def send(self,request):
        response = None
        try:
            handle = self.opener.open(request)
            response = handle.read()

        except IOError, e:
            print 'We failed to open '
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "The error object has the following 'reason' attribute :", e.reason
                print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
        return response
