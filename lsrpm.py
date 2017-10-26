#!/usr/bin/python
# -*- coding: utf-8 -*-

## begin Copyright
#  Copyright Takeharu KATO 2009
## end  Copyright

import rpm
import os
import os.path
import sys
import re
import stat

def show_rpm_info(file):
    """
    Print rpm package information.
    """
    fd = os.open(file, os.O_RDONLY)

    ts = rpm.TransactionSet()

    h = ts.hdrFromFdno(fd)
    os.close(fd)

    print '"%s","%s","%s","%s","%s","%s","%s"' % (h['arch'], h['name'], h['group'], h['version'], h['summary'], h['license'], h['size'])

    return None

def show_rpm_list(file_list):
    """
    Show rpm package information in the list.
    """
    for file in file_list:
        show_rpm_info(file)
    return None

def get_rpm_file_in_dir(path):
    """
    Search rpm files in the specified directory and return the file-list.
    """
    rpms = []
    for root, dirs, files in os.walk(path):
        for name in files:
            filename = os.path.join(root, name)
            if re.search('.*\.rpm$', filename):
                rpms.append(filename)
    rpms.sort()
    return rpms

def main(argv=None):
    """
    main function.
    """
    if argv is None:
        argv = sys.argv

    print "Target, name, group, version, summary, license, size"
    for file_arg in argv[1:]:
        if stat.S_ISDIR( os.stat( file_arg )[stat.ST_MODE] ):
            file_list = get_rpm_file_in_dir(file_arg)
        else:
            file_list = [file_arg]
        show_rpm_list(file_list)

if __name__ == "__main__":
    sys.exit(main())
