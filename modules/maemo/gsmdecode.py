#!/usr/bin/python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 and higer.
##
## Martin Grimme (martin.grimme # gmail.com) 2010
## Guseynov Alexey (kibergus # gmail.com) 2010

LANG_DE = 0x0
LANG_EN = 0x1
LANG_IT = 0x2
LANG_FR = 0x3
LANG_ES = 0x4
LANG_NL = 0x5
LANG_SE = 0x6
LANG_DA = 0x7
LANG_PO = 0x8
LANG_FI = 0x9
LANG_NO = 0xa
LANG_GR = 0xb
LANG_TR = 0xc
LANG_UNSPECIFIED = 0xf


GSM_DEFAULT_ALPHABET = [
    u"@",
    u"\u00a3",
    u"$",
    u"\u00a5",
    u"\u00e8",
    u"\u00e9",
    u"\u00f9",
    u"\u00ec",
    u"\u00f2",
    u"\u00c7",
    u"\n",
    u"\u00d8",
    u"\u00f8",
    u"\r",
    u"\u00c5",
    u"\u00e5",
    
    u"\u0394",
    u"_",
    u"\u03a6",
    u"\u0393",
    u"\u039b",
    u"\u03a9",
    u"\u03a0",
    u"\u03a8",
    u"\u03a3",
    u"\u0398",
    u"\u039e",
    u" ",
    u"\u00c6",
    u"\u00e6",
    u"\u00df",
    u"\u00c9",
    
    u" ",
    u"!",
    u"\"",
    u"#",
    u"\u00a4",
    u"%",
    u"&",
    u"'",
    u"(",
    u")",
    u"*",
    u"+",
    u",",
    u"-",
    u".",
    u"/",
    
    u"0",
    u"1",
    u"2",
    u"3",
    u"4",
    u"5",
    u"6",
    u"7",
    u"8",
    u"9",
    u":",
    u";",
    u"<",
    u"=",
    u">",
    u"?",
    
    u"\u00a1",
    u"A",
    u"B",
    u"C",
    u"D",
    u"E",
    u"F",
    u"G",
    u"H",
    u"I",
    u"J",
    u"K",
    u"L",
    u"M",
    u"N",
    u"O",
    
    u"P",
    u"Q",
    u"R",
    u"S",
    u"T",
    u"U",
    u"V",
    u"W",
    u"X",
    u"Y",
    u"Z",
    u"\u00c4",
    u"\u00d6",
    u"\u00d1",
    u"\u00dc",
    u"\u00a7",

    u"\u00bf",
    u"a",
    u"b",
    u"c",
    u"d",
    u"e",
    u"f",
    u"g",
    u"h",
    u"i",
    u"j",
    u"k",
    u"l",
    u"m",
    u"n",
    u"o",

    u"p",
    u"q",
    u"r",
    u"s",
    u"t",
    u"u",
    u"v",
    u"w",
    u"x",
    u"y",
    u"z",
    u"\u00e4",
    u"\u00f6",
    u"\u00f1",
    u"\u00fc",
    u"\u00e0"
]

 
def octify(str):
        '''     
        Returns a list of octet bytes representing
        each char of the input str.               
        '''                                       
 
        bytes = map(ord, str)
        bitsconsumed = 0     
        referencebit = 7     
        octets = []          
 
        while len(bytes):
                byte = bytes.pop(0)
                byte = byte >> bitsconsumed
 
                try:                       
                        nextbyte = bytes[0]
                        bitstocopy = (nextbyte & (0xff >> referencebit)) << referencebit
                        octet = (byte | bitstocopy)                                     
 
                except:
                        octet = (byte | 0x00)
 
                if bitsconsumed != 7:
                        octets.append(byte | bitstocopy)
                        bitsconsumed += 1               
                        referencebit -= 1               
                else:                                   
                        bitsconsumed = 0                
                        referencebit = 7                
 
        return octets
 
def semi_octify(stri):
        '''          
        Expects a string containing two digits.
        Returns an octet -                     
        first nibble in the octect is the first
        digit and the second nibble represents 
        the second digit.                      
        '''                                    
        try:                                   
                digit_1 = int(stri[0])          
                digit_2 = int(stri[1])          
                octet = (digit_2 << 4) | digit_1
        except:                                 
                octet = (1 << 4) | digit_1      
 
        return octet
 
 
def deoctify(arr):
 
        referencebit = 1
        doctect = []    
        bnext = 0x00    
 
        for i in arr:
 
                bcurr = ((i & (0xff >> referencebit)) << referencebit) >> 1
                bcurr = bcurr | bnext                                      
 
                if referencebit != 7:
                        doctect.append( bcurr )
                        bnext = (i & (0xff << (8 - referencebit)) ) >> 8 - referencebit
                        referencebit += 1                                              
                else:                                                                  
                        doctect.append( bcurr )                                        
                        bnext = (i & (0xff << (8 - referencebit)) ) >> 8 - referencebit
                        doctect.append( bnext )                                        
                        bnext = 0x00                                                   
                        referencebit = 1                                               
 
        return ''.join([chr(i) for i in doctect])
 
 
def createPDUmessage(number, msg):
        '''                       
        Returns a list of bytes to represent a valid PDU message
        '''                                                     
        numlength = len(number)                                 
        if (numlength % 2) == 0:                                
                rangelength = numlength                         
        else:                                                   
                number = number + 'F'                           
                rangelength = len(number)                       
 
        octifiednumber = [ semi_octify(number[i:i+2]) for i in range(0,rangelength,2) ]
        octifiedmsg = octify(msg)                                                      
        HEADER = 1                                                                     
        FIRSTOCTETOFSMSDELIVERMSG = 10                                                 
        ADDR_TYPE = 129 #unknown format                                                
        number_length = len(number)                                                    
        msg_length = len(msg)                                                          
        pdu_message = [HEADER, FIRSTOCTETOFSMSDELIVERMSG, number_length, ADDR_TYPE]    
        pdu_message.extend(octifiednumber)                                             
        pdu_message.append(0)                                                          
        pdu_message.append(0)                                                          
        pdu_message.append(msg_length)                                                 
        pdu_message.extend(octifiedmsg)                                                
        return pdu_message                                                             
 
 


def decode(s, n):
    """
    Decodes the given string using the given cell broadcast data coding scheme.
    
    @param s: string to decode
    @param n: GSM cell broadcast data coding scheme
    @return: UTF-8 string
    """

    # separate into nibbles
    hbits = (n & 0xf0) >> 4
    lbits = (n & 0x0f)
    
    if (hbits == 0x0):
        # language
        return _decode_language(s, lbits)

    elif (0x1 <= hbits <= 0x3):
        # reserved language
        return s
        
    elif (0x4 <= hbits <= 0x7):
        # general data coding indication
        return _decode_general_data_coding(s, hbits, lbits)
        
    elif (0x8 <= hbits <= 0xe):
        # reserved coding group
        return s
        
    elif (hbits == 0xf):
        # data coding / message handling
        return s


def _decode_language(s, lang):

    return _decode_default_alphabet(s)


def _decode_default_alphabet(s):
    
    # ought to be all in the 7 bit GSM character map
    # modem is in 8 bit mode, so it makes 7 bit unpacking itself
    chars = [ GSM_DEFAULT_ALPHABET[ord(c)] for c in s ]
    u_str = "".join(chars)
    return u_str.encode("utf-8")


def _decode_hex(s):

    return s.decode("hex")


def _decode_usc2(s):

    return s.decode("hex").decode("utf-16-be").encode("utf-8")


def _decode_general_data_coding(s, h, l):

    is_compressed = (h & 0x2)
    
    alphabet = (l & 0xc) >> 2

    if (alphabet == 0x0):
        # default alphabet
        return _decode_default_alphabet(s)
        
    elif (alphabet == 0x1):
        # 8 bit
        # actually, encoding is user-defined, but let's assume hex'd ASCII
        # for now
        return _decode_hex(s)
        
    elif (alphabet == 0x2):
        # USC2 (16 bit, BE)
        return _decode_usc2(s)
    elif (alphabet == 0x3):
        # reserved
        return s

def decode_number(number):
    dnumber = ""
    for i in number:
        if i & 0xf < 10:
            dnumber += str(int((i & 0xf)))
        if (i & 0xf0) >> 4 < 10:
            dnumber += str(int((i & 0xf0) >> 4))
    return dnumber

def decode_timestamp(timestamp):
    res = {}
    res['year'] =  str(timestamp[0] & 0xf) + str((timestamp[0] & 0xf0) >> 4)
    res['month'] = str(timestamp[1] & 0xf) + str((timestamp[1] & 0xf0) >> 4)
    res['day'] = str(timestamp[2] & 0xf) + str((timestamp[2] & 0xf0) >> 4)
    res['hour'] = str(timestamp[3] & 0xf) + str((timestamp[3] & 0xf0) >> 4)
    res['minute'] = str(timestamp[4] & 0xf) + str((timestamp[4] & 0xf0) >> 4)
    res['second'] = str(timestamp[5] & 0xf) + str((timestamp[5] & 0xf0) >> 4)
    res['timezone'] = str(timestamp[6] & 0xf) + str((timestamp[6] & 0xf0) >> 4)
    return res

def decode_pdu (pdumsg):
    pdu = {}
    pdu['type'] = int(pdumsg[0])
    if pdu['type'] & 0x3 == 0x0:
        pdu['address_len'] = int(pdumsg[1])
        pdu['type_of_address'] = int(pdumsg[2])
        base = 3+(pdu['address_len']+1)/2
        pdu['sender'] = decode_number(pdumsg[3:base])
        pdu['pid'] = int(pdumsg[base])
        pdu['dcs'] = int(pdumsg[base+1])
        pdu['timestamp'] = decode_timestamp (pdumsg[base+2:base+9]);
        pdu['udl'] = int(pdumsg[base+9])
        pdu['user_data'] = pdumsg[base+10:len(pdumsg)]

        alphabet = (pdu['dcs'] & 0xc) >> 2
        if alphabet == 0x0:
            # This is 7-bit data. Taking of only pdu['udl'] bytes is important because we can't distinguish 0 at the end from @ if only one bit is used in last bite
            pdu['user_data'] = _decode_default_alphabet(deoctify(pdu['user_data']))[0:pdu['udl']]
        elif alphabet == 0x1:
            # actually, encoding is user-defined, but let's assume ASCII
            pdu['user_data'] = ''.join([chr(i) for i in pdu['user_data']])
        elif (alphabet == 0x2):
            # USC2 (16 bit, BE)
            pdu['user_data'] = (''.join([chr(i) for i in pdu['user_data'][6:len(pdu['user_data'])]])).decode("utf-16-be").encode("utf-8")
        elif (alphabet == 0x3):
            # reserved
            pdu['user_data'] = ''.join([chr(i) for i in pdu['user_data']])

        if pdu['type'] & 0x4 == 0:
            pdu['part'] = True
        else:
            pdu['part'] = False
    else:
        # TODO support other types of messages
        # This is not incoming message
        # pdu['type'] & 0x3 == 2 means delivery report
        return None

    return pdu
