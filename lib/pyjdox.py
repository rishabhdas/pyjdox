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

    def args(self, obj):
        args = []
        try:
            arginfo = inspect.getargspec(obj)
        except TypeError:
            pass
        args = arginfo[0]
        if args:
            if args[0] == 'self':
                args.pop(0)
        return args

    def describe_function(self, obj, mname, method=False):
        """ Describe a function or method. Return function doc-string, function
        arguments and function type as list """

        fdesc = {}
        fdoc = ''
        if obj.__doc__:
            fdoc = obj.__doc__

        fdesc['namespace'] = mname
        fdesc['doc'] = fdoc
        fdesc['args'] = self.args(obj)
        if not method:
            fdesc['type'] = 'Function'
        return fdesc

    def describe_class(self, obj, mname):
        """ Describe class object, list down class methods and return the class
        documentation as a list """
        cname = obj.__name__
        cmethods = {}
        mname = "%s.%s" % (mname, cname)
        for name in obj.__dict__:
            med = getattr(obj, name)
            if inspect.ismethod(med):
                method = med.__name__
                method = '%s' % (method)
                cmethods[method] = self.describe_function(med, mname, True)
        return cmethods

    def describe(self, module, modloc):
        """ Get class, corresponding methods and function details of a given
        module object """
        module_doc = {}
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj):
                class_name = '%s.%s' % (module.__name__, obj.__name__)
                if class_name not in module_doc:
                    module_doc.update(
                        {
                            class_name: {
                                "namespace": module.__name__,
                                "doc": obj.__doc__,
                                "loc": modloc,
                                "type": "Class",
                                "methods": [
                                    self.describe_class(
                                        obj,
                                        module.__name__)]}})

            elif inspect.isfunction(obj):
                function_name = "%s.%s" % (module.__name__, obj.__name__)
                module_doc[function_name] = self.describe_function(
                    obj, module.__name__)
        return module_doc
