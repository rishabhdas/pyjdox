#!/usr/bin/python

# Rishabh Das <rishabh5290@gmail.com>
#
# This program is a free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the license, or(at your option) any
# later version. See http://www.gnu.org/copyleft/gpl.html for the full text of
# the license.


import inspect
import os
import imp
import sys
import json
import pydoc


class pyjdox:
    """ Contains functions to document python code and return JSON """

    def describe_function(self, obj, method=False):
        """ Describe a function or method. Return function doc-string, function
        arguments and function type as list """
        fdesc = {}
        fdoc = ''
        if obj.__doc__:
            fdoc = obj.__doc__
        try:
            arginfo = inspect.getargspec(obj)
        except TypeError:
            pass
        args = arginfo[0]
        if args:
            if args[0] == 'self':
                args.pop(0)
        fdesc['doc'] = fdoc
        fdesc['args'] = args
        if method:
            fdesc['type'] = 'Method'
        else:
            fdesc['type'] = 'Function'
        return fdesc

    def describe_class(self, obj):
        """ Describe class object, list down class methods and return the class
        documentation as a list """
        cname = obj.__name__
        cmethods = {}
        for name in obj.__dict__:
            med = getattr(obj, name)
            if inspect.ismethod(med):
                method = med.__name__
                method = '%s.%s' % (cname, method)
                cmethods[method] = self.describe_function(med, True)
        return cmethods

    def describe(self, module, modloc):
        """ Get class, corresponding methods and function details of a given
        module object """
        json_doc = {}
        cdict = mdict = {}
        module_doc = {}
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj):
                cdict = self.describe_class(obj)
                json_doc.update(cdict)
            elif (inspect.ismethod(obj) or inspect.isfunction(obj)):
                mdict[obj.__name__] = self.describe_function(obj)
                json_doc.update(mdict)
        for key in json_doc.keys():
            json_doc[key]['loc'] = modloc
            if json_doc[key]['type'] == 'Function':
                napikey = '%s.%s' % (module.__name__, key)
                namespace = napikey.rsplit('.', 1)[0]
                module_doc[napikey] = json_doc[key]
                module_doc[napikey]['namespace'] = namespace
            else:
                napikey = '%s' % (key)
                class_name, function_name = napikey.split('.')
                class_full_name = '%s.%s' % (module.__name__, class_name)

                if class_full_name not in module_doc:
                    module_doc.update({class_full_name: {"namespace": module.__name__,
                                                         "loc": modloc,
                                                         "type": "Class",
                                                         "methods": [{function_name: json_doc[key]}]}})
                else:
                    module_doc[class_full_name]["methods"].append(
                        {function_name: json_doc[key]})
            json_doc.pop(key)
        return module_doc
