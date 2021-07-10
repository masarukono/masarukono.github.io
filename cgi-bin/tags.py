#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module tags
import util

def concat(top, item, end):
    if type(item) == 'str':
        return top + item + end
    elif type(item) == 'list' and len(item) <= 0:
        return top + end
    else:
        return [top, item, end]

def endtag(tag):
    return '</' + tag + '>'

def fromto(n0, nmax, blank=0, step=1):
    cases = []
    if blank:
        cases.append('')
    for i in range(n0, nmax+1, step):
        cases.append(format(i, 'x'))
    #print('(Cases:', cases, ')')
    return cases

def paramtag(tag, param={}):
    s = '<' + tag
    if param:
        for key, val in param.items():
            s = s + ' ' + key + '="' + val + '"'
    s = s + '>'
    return s

def recurse(obj, lev=0):
    tab = ['', '  ', '    ', '      ', '        ', '          ']
    if isinstance(obj, list):
        for i in range(len(obj)):
            recurse(obj[i], lev+1)
    elif isinstance(obj, str):
        print(tab[lev] + obj)
    elif hasattr(obj, 'render'):
        obj.render()
    else:
        print(obj, type(obj), 'is else', hasattr(obj, 'render'), '\n')
        pass

def yorn(cond, positive, negative):
    if cond == None:
        return negative
    if type(cond) == str:
        cond = int(float.fromhex(cond))
    if cond > 0:
        return positive
    else:
        return negative

class Alert:
    def __init__(self, label, mesg):
        self.l = '<input type="button" value="' + label
        self.l = self.l + '" onClick="window.alert(\'' + mesg + '\')">'
    def render(self, lev=0):
        recurse(self.l, lev)

class Alertyn:
    def __init__(self, cond, yorn, label, mesg, option=[]):
        if type(cond) == str:
            cond = int(float.fromhex(cond))
        if (cond > 0 and yorn > 0) or (cond <= 0 and yorn <= 0):
            self.l = Alert(label+'?', mesg)
        else:
            self.l = Submit(label)
    def render(self, lev=0):
        recurse(self.l, lev)

class Form:
    """
    Creation of HTML form.  start() and finish() should enclose
    individual form elements.
    """
    def __init__(self, action, cont=[]):
        self.f = '<form action="'+action+'" method="post">'
        self.e = '</form>'
        self.l = [self.f, cont, self.e]
    def start(self):
        print(self.f)
    def finish(self):
        print('</form>')
    def render(self, lev=0):
        recurse(self.l, lev)

class Formrow(Form):
    def __init__(self, action, cont=[]):
        self.f = '<form action="'+action+'" method="post">'
        self.e = '</form>'
        self.l = ['<tr>' + self.f]
        for i in range(len(cont)):
            if type(cont[i]) == 'str':
                self.l.append('<td>'+ cont[i]+'</td>')
            else:
                self.l.append(Tagplus('td', cont[i]))
        self.l.append(self.e + '</tr>')
    def render(self, lev=0):
        recurse(self.l, lev)

class Header:
    def __init__(self, text, level=4):
        self.text = text
        self.level = level
        self.l = '<h'+str(level)+'>'+text+'</h'+str(level)+'>'
        #print('Start:', self.l, '<p>')
        self.render()
    def render(self, lev=0):
        recurse(self.l, lev)

class Pagetop:
    def __init__(self, title='', jsfile='', comment=''):
        print('Content-Type: text/html')
        print()                             # blank line, end of headers
        print('<html>')
        print()                             # blank line, end of headers
        print('<head>')
        print('<meta http-equiv="Content-Type" '
              'content="text/html; charset=UTF-8">')
        print('<meta http-equiv="Content-Script-Type" '
              'content="text/javascript">')
        '''
        '''
        print('<title>' + title + '</title>')
        if jsfile:
            print('<script type="text/javascript">')
            print('<!--')
            f = open(jsfile, 'r')
            for line in f:
                print(line, '')
            print('//-->')
        print('</head>\n<body>\n')
        if comment:
            print(comment)

class Pageend:
    def __init__(self, comment=''):
        if comment:
            print('', comment)
        print('<br>\n</body>\n</html>\n<br>\n')
class Submit:
    def __init__(self, label, name=''):
        if name:
            l = '<input type="submit" name="'+name+'" value="'+label+'">'
        else:
            l = '<input type="submit" name="'+label+'" value="'+label+'">'
        self.l = l
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagtop:
    def __init__(self, tag, param={}):
        self.s = paramtag(tag, param)
        self.e = endtag(tag)
    def render(self, lev=0):
        recurse(self.s, lev)
        
class Tagsand:
    '''
    Table entry in a single line.
    '''
    def __init__(self, tag, string='', param={}):
        self.l = paramtag(tag, param) + string + endtag(tag)
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagplus:
    '''
    Table entry in multiple lines.  Contents can be appended later.
    ''' 
    def __init__(self, tag, cont=[], param={}):
        self.s = paramtag(tag, param)
        self.c = cont
        self.e = endtag(tag)
        self.l = [self.s, self.c, self.e]
    def add(self, obj):
        self.c.append(obj)
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagform(Tagplus):
    def __init__(self, name, action, cont=[]):
        param = {'name':name, 'method':'post', 'action':action}
        super().__init__('form', cont, param)
        self.c = cont
        self.l = concat(self.s, self.c, self.e)
    def append(self, item):
        self.c.append(item)
    def render(self, lev=0):
        recurse(self.l, lev)

class Select:
    def __init__(self, name, opt=[], chat=None, cora=1, pos=0, nib=-1):
        '''
        cora: command or answer
        pos:  position of nibble (BCD)
        '''
        #print('[[Sel,..', name, cora, pos, nib, ']]')
        self.l = ['<select name="' + name + '">']
        if not chat or not chat.active(name):
            data = ''
        elif nib >= 0:
            data = chat.nibbleof(name, cora, pos, nib)
        else:
            data = chat.termof(name, cora, pos)
        for i in range(len(opt)):
            if str(data) == opt[i]:
                sel = ' selected'
                #print('name, data', name, data)
            else:
                sel = ''
            self.s = '<option' + sel + '>' + str(opt[i]) + '</option>'
            self.l.append(self.s)
            self.data = data
        self.l.append('</select>')
    def render(self, lev=0):
        recurse(self.l, lev)

class Xorsel:
    def __init__(self, name, opt=[], chat=None, cora=0, pos=1, byte=-1):
        #print('[xor: name cora pos byte:', name, cora, pos, byte, ']')
        self.l = ['<select name="' + name + '">']
        if not chat or not chat.active(name):
            data = None
        else:
            data = chat.byteof(name, cora, pos)
            print('[xor,cora,pos,data', name, cora, pos, data, ']')
        for i in range(len(opt)):
            if data and data == str(i):
                sel = ' selected'
                print('(i,data,<=>',i, data, data==str(i), ')')
            else:
                sel = ''
            self.s = '<option' + sel + '>' + str(opt[i]) + '</option>'
            self.l.append(self.s)
            self.data = data
        self.l.append('</select>')
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagtable:
    def __init__(self, caption='', thead=[], tdata=[]):
        #cap = Tagsand('caption', caption)
        cap = '<caption><font size="4"><b>' + caption
        cap = cap + '</b></font></caption>'
        thd = Tagplus('tr', thead)
        tdt = tdata
        top = Tagtop('table')
        self.l = [top.s, cap, thd, tdt, top.e]
    def addparts(self, head=[], data=[]):
        if head:
            self.thd = head
        if data:
            self.tdt = data
    def render(self, lev=0):
        recurse(self.l, 0)
        print('<br>')

class Button(Tagtop):
    def __init__(self, label, name, oncl='submit()'):
        param = {'type':'button', 'name':name, 'value':label, 'onclick':oncl}
        super().__init__('input', param)
    def render(self, lev=0):
        recurse(self.s, lev)

class Tabhead(Tagsand):
    '''
    One item in the table head line.  Multiple Tabheads can appear
    appear between <tr> and </tr>, delimited by </th>...</th>.
    '''
    def __init__(self, title, wid=100, hal='left', val='middle'):
        param = {'width':str(wid), 'align':hal, 'valign':val}
        super().__init__('th', title, param)
    def render(self, lev=0):
        recurse(self.l, lev)

class TabBCD:
    def __init__(self, name, pandb=[], pioval=[], chat=None):
        mod = ['_h','_t','_o']		# modifiers for unit
        keta = len(pandb)		# No. of options to choose from
        self.l = ['<tr><td>'+name+'</td>', '<td>']
        self.val = 0
        line = []
        for k in range(keta):
            nameit = name
            if keta > 1:
                nameit = name+(mod[k])
            line = ['<select name="' + nameit + '">']
            port = pandb[k] >> 8
            pval = int(float.fromhex(pioval[port]))
            if (pandb[k] & 0xff) < 0x10:
                bits = (pandb[k] & 0x0f)
                stat = pval & bits
            else:
                bits = (pandb[k] & 0xf0) >> 4
                stat = (pval >> 4) & bits
            self.val = self.val*10 + stat
            imax = min(bits, 9)
            print('(pval,...', hex(pval),hex(bits),stat,imax,self.val, ')')
            isl = -1
            opt = fromto(0,imax,1)
            if not chat or not chat.active(name):
                data = ''
            else:
                data = str(stat)
            #for i in range(imax):
            for i in range(len(opt)):
                if opt[i] == data:
                    sel = " selected"
                    isl = i
                else:
                    sel = ""
                si = opt[i]
                line.append('<option value="'+si+'"'+sel+'>'+si+'</option>')
            line.append('</select>')
            self.l.append(line)
        self.l.append('</td>')
        #if comment:
        #    self.l.append('<td>'+comment+'</td>')
        self.l.append('</tr>')
    def value(self):
        return self.val
    def render(self, lev=0):
        recurse(self.l, lev)

class Tablerow:
    def __init__(self, cont=[], col=0, span=0):
        #self.l = ['<tr valign="top">']
        self.l = ['<tr>']
        for i in range(len(cont)):
            if span > 1 and col == i:
                tag = '<td colspan="' + str(span) + '">'
                par = {'colspan':str(span)}
            else:
                tag = '<td>'
                par = {}
            if type(cont[i]) == 'str':
                self.l.append(tag + cont[i] + '</td>')
            if type(cont[i]) == 'int':
                self.l.append(tag + str(cont[i]) + '</td>')
            else:
                self.l.append(Tagplus('td', cont[i], par))
        self.l.append('</tr>')
    def render(self, lev=0):
        recurse(self.l, lev)

class Radio:
    def __init__(self, name, cases=[], chat=None):
    #def __init__(self, name, cases=[], val=0, td='', sel=-1):
        """
        cases contain labels applied to the selection.
        """
        if chat:
            addr = chat.comhex(name)
            port = addr >> 8
            bits = addr & 0xff
            #print('((radio:', name, hex(addr), port, hex(bits), '))')
        else:
            print('(((chat not found', name, ')))')
            return
        curr = 0
        valu = chat.termof('pallget', 1, port)
        curr = int(float.fromhex(valu))
        stat = curr & bits
        match = 0			# default
        if stat == bits:		# On/Off switch
            match = 1
        self.l = ['<tr><td>' + name + '</td>']
        for i in range(len(cases)):
            if i == int(match):
                ck = " checked"
            else:
                ck = ""
            s1 = '<td> <input type ="radio" name="' + name + '"' + \
            ' value="' + str(i) + '"' + ck + '>' + cases[i] + '</td>'
            self.l.append(s1)
            #print(s1)
        self.l.append('</tr>\n')
    def render(self, lev=0):
        recurse(self.l, lev)

class Radioform:
    def __init__(self, name, action, cases=[], chat=None):
        """
        cases contain labels applied to the selection.
        """
        if chat:
            addr = chat.comhex(name)
            port = addr >> 8
            bits = addr & 0xff
            #print('((radio:', name, hex(addr), port, hex(bits), '))')
        else:
            print('(((chat not found', name, ')))')
            return
        curr = 0
        valu = chat.termof('pallget', 1, port)
        curr = int(float.fromhex(valu))
        stat = curr & bits
        match = 0			# default
        if stat == bits:		# On/Off switch
            match = 1
        self.l = ['<tr><form action="'+action+'" method="post">']
        self.l.append('<td>' + name + '</td>')
        for i in range(len(cases)):
            if i == int(match):
                ck = " checked"
            else:
                ck = ""
            s1 = '<td> <input type ="radio" name="' + name + '"' + \
            ' value="' + str(i) + '"' + ck + '>' + cases[i] + '</td>'
            self.l.append(s1)
            #print(s1)
        sub = Submit('Go')
        self.l.append(Tagplus('td', sub))
        
        self.l.append('</form></tr>\n')
    def render(self, lev=0):
        recurse(self.l, lev)
'''
class Tabradio:
    def __init__(self, name, narg=0, pandb=[], cases=[], pioval=[]):
        """
        cases contain labels applied to the selection.
        """
        opt = len(pandb)		# No. of options to choose from
        port = pandb[0] >> 8
        bits = pandb[0] & 0xff
        curr = 0
        if pioval:
            curr = int(float.fromhex(pioval[port]))
        #curr = int(hex(pioval[port]))
        stat = (curr) & bits
        match = 0			# default
        if opt == 1 and stat == bits:	# On/Off switch
            match = 1
        elif opt > 1:
            for i in range(1, opt):
                bits = pandb[i] & 0xff
                if (curr & bits) == bits:
                    match = i
                    #print(pioval[port], i, "bits", hex(bits), '<br>\n')
        self.l = ['<tr><td>' + name + '</td>']
        for i in range(len(cases)):
            if i == int(match): # and ro == "":
                ck = " checked"
            else:
                ck = ""
            s1 = '<td> <input type ="radio" name="' + name + '"' + \
            ' value="' + str(i) + '"' + ck + '>' + cases[i] + '</td>'
            self.l.append(s1)
            #print(s1)
        self.l.append('</tr>\n')
    def render(self, lev=0):
        recurse(self.l, lev)
'''
class Tabsubmit:
    def __init__(self, label, name='', action='', cont=[]):
        butt = Button(label, name)
        form = Tagform(name, action, [butt])
        #hact = qhide(action)
        f = Tagplus('td', form)
        n = Tagsand('td', name, {'valign':'top'})
        a = Tagsand('td', action, {'valign':'top'})
        self.l = Tagplus('tr', [f, n, a])
    def render(self, lev=0):
        recurse(self.l, lev)

"""

def printable(obj):
    if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return True
    else:
        return False

def qhide(msg, char='?'):
    #remove the part starting with the character '?'.
    pos = msg.find(char)
    if pos >= 0:
        msg = msg[0:pos]
    return msg

def hasattr(obj, method):
    try:
        ga = getattr(obj, method)
    except:
        return False
    else:
        return True

class Radio:
    def __init__(self, name, cases=[], val=0, td='', sel=-1):
        self.l = []
        for i in range(len(cases)):
            ck = ifchecked(i+val, sel)
            line = '<input type ="radio" name="' + name + '"' + \
                    ' value="' + cases[i] + '"' + ck + '>' + cases[i]
            if td:
                line = '<td> ' + line + ' </td>'
            self.l.append(line)
    def render(self, lev=0):
        recurse(self.l, lev)
"""   
"""        
class Tagitem(Tagtop):
    '''
    One item in a table, delimited by <td>...</td>.
    Multiple Tagitems can appear between <tr> and </tr>.
    '''
    def __init__(self, item, hal='', val=''):
        param = {'align':hal, 'valign':val}
        super().__init__('td', param)
        self.l = concat(self.s, item, self.e)
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagdata(Tagtop):
    def __init__(self, tag, cont=[], param={}):
        super().__init__(tag, param)
        self.l = concat(self.s, cont, self.e)
    def render(self, lev=0):
        recurse(self.l, lev)

class Tagtext(Tagtop):
    def __init__(self, name, value='', size='4', title=''):
        param = {'type':'text', 'name':name, 'value':value, 'size':size}
        super().__init__('input', param)
        self.l = title + self.s
    def render(self, lev=0):
        recurse(self.l, lev)
    
class Tagrow:
    def __init__(self, cont=[]):
        self.l = ['<tr>']
        for i in range(len(cont)):
            if type(cont[i]) == 'str':
                self.l.append('<td>'+ cont[i]+'</td>')
            else:
                self.l.append(Tagplus('td', cont[i]))
                #self.l.append('</tr>')
    def render(self, lev=0):
        recurse(self.l, lev)
"""            
"""
def ifchecked(i, sel, word='checked'):
    if (int(i) == int(sel)):
        return ' ' + word
    else:
        return ''
        
class Tabcell(Tagtop):
    '''
    One item in a table, delimited by <td>...</td>.
    Multiple Tagcells can appear between <tr> and </tr>.
    '''
    def __init__(self, cell='', param={}):
        super().__init__('td', param)
        self.l = self.s + cell + self.e
    def render(self, lev=0):
        recurse(self.l, lev)
        
class Tabline(Tagtop):
    '''
    One Tab line with multiple columns, delimited by <tr>...</tr>.
    '''
    def __init__(self, cell='', param={}):
        super().__init__('td', param)
        self.l = self.s + cell + self.e
    def render(self, lev=0):
        recurse(self.l, lev)

def dicval(key, val=0, dic=None):
    if dic != None and key in dic:
        return dic[key]
    else:
        return val
"""
"""
class Formline(Tagplus):
    def __init__(self, name, action, cont=[]):
        param = {'name':name, 'method':'post', 'action':action}
        super().__init__('form', cont, param)
        self.c = cont
        self.l = ['<tr>' + self.s, self.c, self.e + '</tr>']
        #self.l.append(cont)
        #self.l.append('</form> </tr>')
    def render(self, lev=0):
        recurse(self.l, lev)
"""
"""

class Onclick:
    def __init__(self, label, func, arg=[], iors=[]):
        l = '<input type="button" value="' +label +'" onClick="' +func +'('
        for i in range(len(arg)):
            if iors[i] == 0:
                l = l + arg[i]
            else:
                l = l + '\'' + arg[i] + '\''
            if i < len(arg)-1:
                l = l + ', '
        l = l + ')">'
        self.l = l
    def render(self, lev=0):
        recurse(self.l, lev)
"""        
"""
# PIO port data table
class Portdata:
    def __init__(self, pdata=[]):
        thd = [Tabhead('Port', 55)]
        tdt = ['<tr>', '<td>Data</td>']
        for i in range(8):
            thd.append(Tabhead(str(i), 45))
            if pdata:
                tdt.append('<td>'+pdata[i]+'</td>')
        tdt.append('</tr>')
        tab = Tagtable('PIO Port Data', thd, tdt)
        tab.render()

# DSpin status table
class DSstatus:
    def __init__(self, pdata=0):
        item = ['PIO', 'ADC', 'Spin', 'AFdem']
        thd = [Tabhead('Work', 55)]
        tdt = ['<tr>'+'<td>Stat</td>']
        bit = 1
        #print('StatDS: pdata', pdata)
        if pdata and len(pdata) > 0:
            for i in range(4):
                stat = int(pdata[0]) & bit
                thd.append(Tabhead(item[i], 45))
                tdt.append('<td>'+str(stat)+'</td>')
                bit = bit << 1
        tdt.append('</tr>')
        tab = Tagtable('DSpin Status', thd, tdt)
        tab.render()
"""    
"""

class Tabexor:
    def __init__(self, name, pandb=[], cases=[], pioval=[]):
    '''
        cases contain labels applied to the selection.
    '''
        nopt = len(pandb)		# No. of options to choose from
        port = pandb[0] >> 8
        bits = pandb[0] & 0xff
        curr = int(float.fromhex(pioval[port]))
        #curr = int(hex(pioval[port]))
        stat = (curr) & bits
        match = 0			# default
        for i in range(1, nopt):
            bits = pandb[i] & 0xff
            if (curr & bits) == bits:
                match = i
        self.l = ['<tr><td>' + name + '</td>']
        for i in range(len(cases)):
            if i == int(match): # and ro == "":
                sel = " selected"
            else:
                sel = ""
            s1 = '<td> <input type ="radio" name="' + name + '"' + \
            ' value="' + str(i) + '"' + sel + '>' + cases[i] + '</td>'
            self.l.append(s1)
            #print(s1)
        self.l.append('</tr>\n')
    def render(self, lev=0):
        recurse(self.l, lev)
"""
