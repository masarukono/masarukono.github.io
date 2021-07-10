#!/usr/bin/env python
# -*- coding: utf-8 -*-
# program start.py
import cgitb
import tags, myipc
cgitb.enable()

#tags.Pagetop('DSpin Start Page', '../js/alertorgo.js')
tags.Pagetop('DSpin Start Page')
tags.Header('Choose What to Do', 2)
here = 'start.py'

# obtain Query_String from ENV and form request to server
qstr = myipc.QueryString()
qstr.addreq('status', '0')		# to know the current status
qdict = qstr.qdict()
request = qstr.comstring()
clsays = '\n'.join(request)

# send request to server and obtain reply
host = qstr.qdicval('host', 'localhost')
port = 65432
chat = myipc.Chatonce(host, port, clsays)
answer = chat.lines

# Status of DSpin
dso = chat.termof('status', 1, 0, 0)
if dso == None:
    dso = 0
#print('(dso=', dso, ')')

# create table containing form-button pairs.
h1 = tags.Tabhead('Command', 100)
h2 = tags.Tabhead('Target/Effect', 120)
h3 = tags.Tabhead('Submit', 140)
thd = [h1, h2, h3]

a3 = tags.Alertyn(dso, 0, 'ports', 'Open DSpin before jump.')
a4 = tags.Alertyn(dso, 0, 'switch', 'Open DSpin before jump.')
a5 = tags.Alertyn(dso, 0, 'param', 'Open DSpin before jump.')
s6 = tags.Select("exec", ['', 'ls', 'date', "uname -a", 'who'])
a6 = tags.Alertyn(dso, 0, 'run', 'Open DSpin before jump.')
a7 = tags.Alertyn(dso, 1, 'quit', 'Close DSpin before jump.')
s8 = tags.yorn(dso, 'Open', 'Closed')

l1 = tags.Formrow(here, ['Open', 'Open DSpin', tags.Submit('open')])
l2 = tags.Formrow(here, ['Close', 'Close DSpin', tags.Submit('close')])
l3 = tags.Formrow('pioport.py', ['Ports', 'PIO Ports', a3])
l4 = tags.Formrow('switch.py', ['Switches', 'PIO Switches', a4])
l5 = tags.Formrow('bcdset.py', ['Params', 'BCD Numbers', a5])
l6 = tags.Formrow(here, ['Command', s6, a6])
l7 = tags.Formrow('../index.html', ['Quit', 'Back to Home', a7])
l8 = tags.Formrow(here, ['Status', str(dso), s8])
tdt = [l1, l2, l3, l4, l5, l6, l7]

tab = tags.Tagtable('Choose DSpin Test or Quit', thd, tdt)
tab.render()

tags.Pageend('End of: DSpin start page')

print('Client says: ', clsays, '<br>')
print('Server says: ', answer, '<br>')
print('Client asks: ', qdict, '<br>')
