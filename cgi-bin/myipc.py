#!/usr/bin/python
# -*- coding: utf-8 -*-
# module myipc
import socket, re, time
import cgi, html

class Comaddr:
    def __init__(self):
        self.cdic = { "open":0, "motor":0x440, "direc":0x480,
                      "blower":0x640, "armfld":0x680,
                      "gain":[0x43c, 0x404, 0x408, 0x410, 0x420],
                      "spinafd":[0x403,0x401,0x402],
                      "afdset_h":0x630, "afdset_t":0x60f, "afdset_o":0x5f0,
                      "afdhold":0x70f, "afdgrad":0x7f0,
                      "automan":0x001, "cartin":0x002, "photo_n":0x004,
                      "photo_t":0x008, "photo_s":0x010, "afd_busy":0x020,
                      "afdget_h":0x203, "afdget_t":0x1f0, "afdget_o":0x10f,
                      "piowrite":0, "pioread":0,
                      "pallclr":0, "pallget":0, "close":0, "status":0, 
                      "exec":0, "ls":0, "date":0,
                      "submit":0
        }
    def keys(self):
        return self.cdic.keys()
    def cdic(self):
        return self.cdic
    def addr(self, name):
        if name in self.cdic.keys():
            return self.cdic[name]
        return []

class Chatonce:
    '''
    Open client socket and ask server some command.
    Receive reply from server and close the connection.
    .deco returns decoded string, .lines are split by newline.
    '''
    def __init__(self, host='localhost', port='65432', asks='', sep='==>'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self.lines = ['']
        if asks == '':
            return
        sock.sendall(asks.encode('utf-8'))
        MSGLEN = 4096
        reply = sock.recv(MSGLEN)
        sock.close()
        self.comaddr = Comaddr()
        self.idic = {}
        self.odic = {}
        self.words = {}
        deco = reply.decode('utf-8')
        #if not deco:
        #return
        self.lines = deco.split('\n')
        self.sep = sep
        for line in self.lines:
            if line == '':
                continue
            item = line.split()
            self.words[item[0]] = item
            div = line.split(self.sep)
            com = div[0].strip().split()
            ret = div[1].strip().split()
            self.words[com[0]] = [com, ret]
            self.idic[com[0]] = com[1].strip()
            self.odic[com[0]] = div[1].strip()
    def wordslist(self):
        print('active words=', self.words)
        return self.words
    def active(self, comd):
        cstr = re.sub('\d$', '', comd)
        if cstr in self.words:
            return True
        else:
            return False
    def comhex(self, name):
        return self.comaddr.addr(name)
    def chatname(self, comd):
        cstr = re.sub('\d$', '', comd)
        if cstr in self.words:
            return cstr
        else:
            None
    def comarg(self, comd, n=0):
        if self.idic.has_key(comd):
            arg = idic[comd].split()
            if len(arg) > 1:
                return arg
            else:
                return odic[comd]
        return ''
        for line in self.lines:
            word = line.strip()
            if word[0] == comd:
                return int(word[1])
        return None
    def bothof(self, comd):
        cstr = re.sub('\d$', '', comd)
        both = self.words.get(cstr, None)
        #print('(bothof,...::', comd, cstr, both, ')')
        return both
    def sideof(self, comd, side=1):
        both = self.bothof(comd)
        if both == None or side < 0 or side > 1:
            side = None
        else:
            side = both[side]
        #print('(sideof,comd,side', comd, side, ')')
        return side
    def termof(self, comd, side=1, pos=0, end=0):
        side = self.sideof(comd, side)
        if side == None or pos < 0 or pos > len(side):
            term = ''
        elif pos >= end:
            term = side[pos]
        else:
            term = side[pos:end]
        #print('(termof,comd,...->', comd, side, pos, end, term, ')')
        return term
    def byteof(self, comd, side=1, pos=0):
        term = self.termof(comd, side, pos)
        valu = int(float.fromhex(term)) & 0xff
        return format(valu, 'x')
    def nibbleof(self, comd, side=1, pos=0, nib=0):
        term = self.termof(comd, side, pos)
        valu = word = None
        if term == None or pos < 0 or pos > len(term):
            return None
        valu = word = int(float.fromhex(term))
        if nib >= 0:
            word = (valu >> (4*nib)) & 0xf
        print('(nibbleof:c,t,v,w',comd,side,term,valu,hex(word),')')
        return format(word, 'x')
    def bytematch(self, comd, side=1, pos=0, byte=-1):
        data = self.nibbleof(comd, side, pos, byte)
        
    def listof(self, comd, side=1, pos=0, end=0):
        item = self.words.get(comd, [])		# item is length 2
        if len(item) <= 0:
            return ''
        if side < 2 and pos < len(item[side]):
            cora = item[side]
            if pos >= end:
                return cora[pos]
            else:
                return cora[pos:end]
        else:
            return ''
    def wordof(self, comd, side=1, pos=0, byte=-1):
        '''
        side: command (0) or answer (1)
        pos:	start position of digit (BCD)
        end:	end position or just one digit (pos >= end)
        '''
        #comd = re.sub('\d$', comd, '')
        item = self.words.get(comd, [])		# item is length 2
        if byte >= 0:
            print('(wordof:com,item,ca,byte', comd, item, comans, byte, ')')
        if len(item) <= 0:
            print('(wordof:com,item,ca', comd, item, comans, ')')
            return ''
        if comans < 2 and pos < len(item[comans]):
            cora = item[comans]
            if byte < 0:
                return cora[pos]
            else:
                mask = 0x0f << byte
                #print('wordof:pos,byte', pos, byte, cora[pos] & mask)
                return int(float.fromhex(cora[pos])) & mask
        else:
            return ''
    def replyto(self, comd):
        rep = self.odic.get(comd)#, 'comd '+ comd +' not found')
        if rep != None:
            arr = rep.split()
            if len(arr) > 1:
                return arr
            else:
                return rep
        return ''
"""        
class TCPsocket(socket.socket):
    '''
    create a socket for a client
    and some basic functions for the client
    '''
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        self.sock = socket.socket(family, type)

    def connect(self, host='localhost', port=54321):
        conn = self.sock.connect((host, port))
        return conn

    def close(self):
        self.sock.close()
        #socket.socket.close(self.sock)

    def send(self, line):
        msg = line.encode()
        self.sock.send(msg)

    def collectlines(self):
        bulk = []
        while (1):
            line = input()
            code = self.wordmatch(line)
            bulk.append(line)
            if code > 0:
                break
        #print('bulk lines\n', bulk)
        return bulk
    
    def bulksend(self, bulk, pr=1):		# server to stdout
        if pr > 0:
            print('---- bulk to server')
        for line in bulk:
            if pr > 0:
                print(line)
            code = self.wordmatch(line)
            if not '\n' in line:
                line = line + '\n'
            self.linesend(line)
            if code > 0:
                return code
        return 0
    
    def allsend(self, lines, pr=1):		# server to stdout
        if pr > 0:
            print('---- allsend to server')
        for i in range(len(lines)+1):
            if i < len(lines):
                line = lines[i]
            else:
                line = 'over'
            if pr > 0:
                print(line)
            self.send(line)
            time.sleep(1)
            if self.wordmatch(line) > 0:
                break
    
    def wordmatch(self, line):
        word=['', 'over', 'bye']
        for i in range(1, len(word)):
            if line == word[i] or line == (word[i]+'\n'):
                return i
        return 0

    def linesend(self, line=None, pr=1):
        if line[len(line)-1] == '\n':	# line should not include nl
            line = line[:len(line)]-1
        msg = line + '\n'		# msg ends with a newline
        self.sock.send(msg.encode())
        return self.wordmatch(line)

    def sendlines(self, pr=1):
        if pr > 0:
            print('---- to server')
        while True:
            line = input()
            ret = self.linesend(line)
            if (ret > 0):
                break
        return ret

    def recv(self, llen=256):
        msg = self.sock.recv(llen)
        line = msg.decode()
        mlen = len(line)
        print(line, len(line))
        if line[mlen-1] == '\x00' or line[mlen-1] == '\n':
            line = line[:mlen-1]
        #line = msg.decode().replace('\n', '\x00')
        return line

    def linerecv(self, llen=256, pr=1):	# server to stdout
        msg = self.sock.recv(llen)
        line = msg.decode()
        if line[len(line)-1] == '\n':
            line = line[:len(line)-1]
        if pr > 0:
            print(line)
        ret = self.wordmatch(line)
        return (line, ret)

    def recvlines(self, llen=256, pr=1):
        if pr > 0:
            print('---- from server')
        while True:
            line, ret = self.linerecv()
            if (ret > 0):
                break
        return ret
"""
class QueryString:
    '''
    Read the QUERY_STRING from FieldStorage, and store the 
    key-val pairs in a dictionary.
    '''
    def __init__(self, form=None):
        if (form == None):
            form = cgi.FieldStorage()
        #print('(QueryString form:', form, ')')
        self.qdic = {}
        self.comaddr = Comaddr()
        if not form:
            return
        keys = form.keys()
        #print('form', form)#, 'keys', keys)
        for k in keys:
            key = html.escape(k)
            if form[k]:
                val = form.getvalue(key)
            else:
                val = ''
            self.qdic[key] = val
            #self.qdic[key] = html.escape(val)
        #print('(QueryString qdic:', self.qdic, ')')
        # qdic is dictionary of command:answer pairs
    def argplus(self, comd, clist=[]):
        '''
        clist contains list of command parameters such as ['2', '3']
        which are collected to form an additional arg for comd.
        '''
        if comd not in self.qdic:
            return
        args = self.qdic[comd] + ' '
        for i in range(len(clist)):
            word = comd + clist[i]
            qv = self.qdicval(word)
            if qv:
                args = args + qv
            else:
                args = args + '0'
        self.qdic[comd] = args
    def qdicval(self, key, val=''):
        if self.qdic != None and key in self.qdic:
            return self.qdic[key]
        else:
            return val
    def choice(self, com, opt=[]):	# label is not command
        dic = self.qdic
        if com in dic.keys():
            for i in range(len(opt)):
                if opt[i] == dic[com]:
                    dic[com] = str(i)
                    #print('(choice,i,val', com, i, dic[com], ')')
    def addreq(self, key, val='0'):
        if not key in self.qdic:
            self.qdic[key] = val
    def remove(self, pair={}):
        for key, val in pair.items():
            if key in self.qdic.keys():
                if self.qdic[key] == val:
                    del self.qdic[key]
    def comarg(self):
        comd = self.qdicval("comd")
        if comd:
            self.qdic[comd] = ""
            del self.qdic["comd"]
            args = self.qdicval("args")
            if args:
                self.qdic[comd] = args
                del self.qdic["args"]
            #print("<br>command is this.", comd, args)
    def commatch(self, com, key):
        j = -1
        lenk = len(key)
        if key.startswith(com):
            lenc = len(com)
            if lenk == lenc:
                return 0			# command itself
            elif lenk == lenc+1 and type(key[lenc]) == int:
                return key[lenc]		# arg number
        return j
    def comstring(self, upgr=[]):
        #comd = list(self.cdic.keys())
        comd = list(self.comaddr.keys())
        comstr = []
        for i in range(len(comd)):
            for key, val in self.qdic.items():
                if comd[i] == key:
                    if val == key:
                        val = '0'
                    line = key + ' ' + val
                    comstr.append(line)
        return comstr
    def qdict(self):
        return self.qdic
"""
class TalkOnce:
    def __init__(self, host="localhost", port="65432", lines=""):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.sock = s
    def close(self):
        self.sock.close()
    def send(self, lines="", msg=""):
        self.sock.sendall(bytes(lines, 'utf-8'))

    def receive(self, MSGLEN=4096):
        #self.rec = str(self.sock.recv(128), 'utf-8')
        rec = self.sock.recv(MSGLEN)
        nch = len(rec)
        self.rec = str(rec)
        sch = len(self.rec)
        dec = rec.decode('utf-8')
        dch = len(dec)
        print('Server replied ({} bytes): {}<br>'.format(dch, dec))
        '''
        '''
"""
