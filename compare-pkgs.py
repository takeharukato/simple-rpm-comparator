#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Copyright 2011 Takeharu KATO. 
# All Rights Reserved. 
##

import sys, codecs, os, re, datetime
import ConfigParser
import csv
import rpm
import shutil
import subprocess
import datetime
import tempfile
from optparse import OptionParser
from StringIO import StringIO

#
#Set codecs for pipe (UTF-8)
#
sys.stdin  = codecs.getwriter('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stderr = codecs.getwriter('utf_8')(sys.stderr)

u"""
comparePkgs [options]
usage: comparePkgs -h -v 

options:
  --version                          print version
  -h, --help                         print simple help
  -v, --verbose                      set verbose mode(Not used)
  -f INDIR1,  --indir1=input directory rpm package directory1
  -s INDIR2,  --indir2=input directory rpm package directory2
"""

parser = OptionParser(usage="%prog [options]", version="%prog 1.0")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="set verbose mode")
parser.add_option("-f", "--indir1", action="store", type="string", dest="indir1", 
                  help="path for input-directory1")
parser.add_option("-s", "--indir2", action="store", type="string", dest="indir2", 
                  help="path for input-directory2")

class pkgList:
    def __init__(self, parent):
        self.nameDict = {}
        self.verDict = {}
        self.sumDict = {}
        self.archDict = {}
        self.grpDict = {}
        self.rpmdir=""
        self.suffixes=["-ohpc","-orch"]
        self.parent = parent
    def set_dir(self, name):
        self.rpmdir=name
    def conv_cname(self, name):
        for ptn in self.suffixes:
            if re.search("%s$" % (ptn), name):
                self.parent.dbg_msg("%s=>%s %s" % (name, re.sub(ptn,'',name), ptn) )
                return re.sub(ptn,'',name)
            else:
                self.parent.dbg_msg("%s does not contain %s" % (name,  ptn) )
                return name
    def set_cname(self, name):
        newname = self.conv_cname(name)
        self.nameDict[name]=newname
    def set_ver(self, name, version):
        self.verDict[name]=version
    def set_arch(self, name, arch):
        self.archDict[name]=arch
    def set_grp(self, name, grp):
        self.grpDict[name]=grp
    def set_summary(self, name, summary):
        self.sumDict[name]=summary
    def get_names(self):
        return self.verDict.keys()
    def has_pkg(self, name):
        cname = self.conv_cname(name)
        return cname in self.nameDict.values()
    def get_ver(self,name):
        if ( self.verDict.has_key(name) ):
            return self.verDict[name]
        else:
            return "None"
    def get_arch(self,name):
        if ( self.archDict.has_key(name) ):
            return self.archDict[name]
        else:
            return "None"
    def get_summary(self,name):
        if ( self.sumDict.has_key(name) ):
            return self.sumDict[name]
        else:
            return "None"
    def get_grp(self,name):
        if ( self.grpDict.has_key(name) ):
            return self.grpDict[name]
        else:
            return "None"
    def get_dir(self):
        return self.rpmdir
    def get_name(self):
        if ( self.nameDict.has_key(name) ):
            return self.nameDict[name]
        else:
            return "None"
class comparePkg:
    def __init__(self):
        self.cmdname = 'comparePkg'
        self.indir1 = None
        self.indir2 = None
        self.verbose = False
        self.configfile = None
        self.configbase = "%s.ini" % 'comparePkg'
        self.conf = ConfigParser.SafeConfigParser()
        self.config_dirs = ['/usr/local/etc',
                            '/etc',
                            os.path.join('/etc', self.cmdname),
                            os.path.join('/usr/local', self.cmdname, 'etc'),
                            os.getcwd()]
        self.msg_log = []
        self.war_log = []
        self.err_log = []
        self.dbg_log = []
        self.pkgList = []
        (self.options, self.args) = parser.parse_args()
        self.readConfig()
    def inf_msg(self, msg):
        print msg
        self.msg_log.append(msg)
    def war_msg(self, msg):
        sys.stderr.write(msg+"\n")
        self.war_log.append(msg)
    def err_msg(self, msg):
        sys.stderr.write(msg+"\n")
        self.err_log.append(msg)
    def dbg_msg(self, msg):
        if self.getVerbose():
            sys.stderr.write(msg+"\n")
            self.dbg_log.append(msg)
    def getIndir1(self):
        return self.indir1
    def getIndir2(self):
        return self.indir2
    def setVerbose(self):
        self.verbose = True
    def getVerbose(self):
        return self.verbose;
    def setConfigFile(self, file):
        self.configfile = file
    def getConfigFile(self):
        return self.configfile
    def getInfile(self):
        return self.infile
    def readRPMDir(self, dname):
        rpms = []
        newList = pkgList(self)
        for root, dirs, files in os.walk(dname):
            for name in files:
                filename = os.path.join(root, name)
                if re.search('.*\.rpm$', filename):
                    rpms.append(filename)
        rpms.sort()
        newList.set_dir(dname)
        for file in rpms:
            fd = os.open(file, os.O_RDONLY)
            ts = rpm.TransactionSet()
            h = ts.hdrFromFdno(fd)
            os.close(fd)
            newList.set_cname(h['name'])
            newList.set_ver(h['name'], h['version'])
            newList.set_arch(h['name'], h['arch'])
            newList.set_summary(h['name'], h['summary'])
            newList.set_grp(h['name'], h['group'])
        for name in newList.get_names():
            self.dbg_msg("arch: %s name:%s version:%s" % 
                         (newList.get_arch(name), name, newList.get_ver(name)) )
        
        self.pkgList.append( newList )
        return None
    def doCompare(self):
        if ( len(self.pkgList) < 2 ):
            return None
        self.inf_msg( u"Arch, name, version(%s), version(%s), difference, summary" % 
                      ( os.path.basename(self.pkgList[0].get_dir()), os.path.basename(self.pkgList[1].get_dir())))
        for name in self.pkgList[0].get_names():
            if self.pkgList[1].has_pkg(name):
                if self.pkgList[0].get_ver(name) > self.pkgList[1].get_ver(name):
                    compVal='>'
                elif self.pkgList[0].get_ver(name) < self.pkgList[1].get_ver(name):
                    compVal='>'
                else:
                    compVal='='
                self.inf_msg(u"%s,%s,%s,%s,%s,%s" % (self.pkgList[0].get_arch(name), 
                                    name,
                                    self.pkgList[0].get_ver(name),
                                    self.pkgList[1].get_ver(name),
                                    compVal,
                                    self.pkgList[0].get_summary(name)) )

        for name in self.pkgList[0].get_names():
            if not self.pkgList[1].has_pkg(name):
                self.inf_msg(u"%s,%s,%s,None,-,%s" % (self.pkgList[0].get_arch(name), 
                                    name,
                                    self.pkgList[0].get_ver(name),
                                    self.pkgList[0].get_summary(name)))

        for name in self.pkgList[1].get_names():
            if not self.pkgList[0].has_pkg(name):
                self.inf_msg(u"%s,%s,None,%s,-,%s" % (self.pkgList[1].get_arch(name), 
                                                      name,
                                                      self.pkgList[1].get_ver(name),
                                                      self.pkgList[1].get_summary(name)))
        return None
    def readConfig(self):

        if self.options.verbose:
            self.setVerbose()

        if self.options.indir1 and os.path.exists(self.options.indir1) and os.path.isdir(self.options.indir1):
            self.indir1 = self.options.indir1
        else:
            self.err_msg("Can not open the directory %s." % ( self.options.indir1 ) )

        if self.options.indir2 and os.path.exists(self.options.indir2) and os.path.isdir(self.options.indir2):
            self.indir2 = self.options.indir2
        else:
            self.err_msg("Can not open the directory %s." % ( self.options.indir2 ) )

if __name__ == '__main__':

    obj = comparePkg()
    obj.dbg_msg("dir1: %s dir2: %s" % ( obj.indir1, obj.indir2 ) )
    obj.readRPMDir(obj.indir1)
    obj.readRPMDir(obj.indir2)
    obj.doCompare()
