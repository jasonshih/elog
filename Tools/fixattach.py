#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

# update note field for datafiles to include attachments

import sys
sys.path.append('/auto/share/lib/elog')

import string
import types
import datetime, time

# from elog
import HTML, elogapi


if __name__ == '__main__':
    db = elogapi.getdb()

    (ok, rows) = db.q("""SELECT dfileID, attachlist, note """
                      """ FROM dfile """
                      """ WHERE attachlist IS NOT NULL""")
     
    for r in rows:
        if len(r['attachlist']) > 0:
            n = r['note']
            newnote = r['note'][:]
            if len(newnote) > 0 and newnote[-1] != '\n':
                newnote = newnote + '\n'
            update = 0
            for n in r['attachlist'].split(','):
                if len(n):
                    id = int(n)
                    newnote = newnote + '<elog:attach=%d>\n' % (id,)
                    update = 1
            if update:
                (ok,xxx) = db.q("""UPDATE dfile SET note="%s" """
                                """ WHERE dfileID=%d""" % \
                        (newnote, int(r['dfileID'],)))
                if not ok:
                    sys.stderr.write('failed on dfileID=%s\n' % r['dfileID'])
                    sys.exit(1)