
""" HTTP Content-Type header tools. """

from handywsgi import headers

'''
excerpt from: http://www.w3.org/Protocols/rfc1341/4_Content-Type.html

    Content-Type := type "/" subtype *[";" parameter] 

    type :=          "application"     / "audio" 
              / "image"           / "message" 
              / "multipart"  / "text" 
              / "video"           / x-token 

    x-token := <The two characters "X-" followed, with no 
               intervening white space, by any token> 

    subtype := token 

    parameter := attribute "=" value 

    attribute := token 

    value := token / quoted-string 

    token := 1*<any CHAR except SPACE, CTLs, or tspecials> 

    tspecials :=  "(" / ")" / "<" / ">" / "@"  ; Must be in 
               /  "," / ";" / ":" / "\" / <">  ; quoted-string, 
               /  "/" / "[" / "]" / "?" / "."  ; to use within 
               /  "="                        ; parameter values

'''


# Common charater sets i deem worth having variables for.
UTF8 = 'utf-8'
ASCII = 'us-ascii'
# Valid charset options
# http://www.iana.org/assignments/character-sets/character-sets.xhtml

# Type
TEXT = 'text'
MULTIPART = 'multipart'
MESSAGE = 'message'
IMAGE = 'image'
APPLICATION = 'application'
AUDIO = 'audio'
VIDEO = 'video'
# x-token: will be added when i need them


# Subtype
## text
PLAIN = 'plain'
HTML = 'html'

## multipart
MIXED = 'mixed'
ALTERNATIVE = 'alternative'  # "for representing the same data in multiple formats"
PARALLEL = 'parallel'  # "for parts intended to be viewed simultaneously"
DIGEST = 'digest'  # "for multipart entities in which each part is of type 'message'"

## message
RFC822 = 'rfc822'
PARTIAL = 'partial'  # "for partial messages, to permit the fragmented transmission of bodies that are thought to be too large to be passed through mail transport facilities."
EXTERNAL_BODY = 'External-body'  # "for specifying large bodies by reference to an external data source."

## image
EXAMPLE = 'example'  # image/example, [RFC4735]
G3FAX = 'g3fax'  # image/g3fax, [RFC1494]
GIF = 'gif'  # , [RFC2045][RFC2046]
IEF = 'ief'  # , Image Exchange Format, [RFC1314]
JP2 = 'jp2'  # image/jp2, [RFC3745]
JPEG = 'jpeg'  # , [RFC2045][RFC2046]
JPM = 'jpm'  # image/jpm, [RFC3745]
JPX = 'jpx'  # image/jpx, [RFC3745]
NAPLPS = 'naplps'  # image/naplps, [Ilya_Ferber]
PNG = 'png'  # image/png, [Glenn_Randers-Pehrson]
PWG_RASTER = 'pwg-raster'  # image/pwg-raster, [Michael_Sweet]
SVG_XML = 'svg+xml'  # image/svg+xml, [W3C][http://www.w3.org/TR/SVG/mimereg.html]
TIFF = 'tiff'  # image/tiff, Tag Image File Format, [RFC3302]

## application
ATOM_XML = "atom+xml"  # application/atom+xml, [RFC4287][RFC5023]
ATOMCAT_XML = "atomcat+xml"  # application/atomcat+xml, [RFC5023]
ATOMDELETED_XML = "atomdeleted+xml"  # application/atomdeleted+xml, [RFC6721]
AUTH_POLICY_XML = "auth-policy+xml"  # application/auth-policy+xml, [RFC4745]
BEEP_XML = "beep+xml"  # application/beep+xml, [RFC3080]
CALENDAR_JSON = "calendar+json"  # application/calendar+json, [RFC7265]
CALENDAR_XML = "calendar+xml"  # application/calendar+xml, [RFC6321]
CALL_COMPLETION = "call-completion"  # application/call-completion, [RFC6910]
CONFERENCE_INFO_XML = "conference-info+xml"  # application/conference-info+xml, [RFC4575]
CPL_3XML = "cpl+xml"  # application/cpl+xml, [RFC3880]
CSRATTRS = "csrattrs"  # application/csrattrs, [RFC7030]
CSTA_XML = "csta+xml"  # application/csta+xml, [Ecma_International_Helpdesk]
DASH_XML = "dash+xml"  # application/dash+xml, [Thomas_Stockhammer][ISO-IEC_JTC1]
DAVMOUNT_XML = "davmount+xml"  # application/davmount+xml, [RFC4709]
ENCAPRTP = "encaprtp"  # application/encaprtp, [RFC6849]
EPUB_ZIP = "epub+zip"  # application/epub+zip, [International_Digital_Publishing_Forum][William_McCoy]
EXI = "exi"  # , [W3C][http://www.w3.org/TR/2009/CR-exi-20091208/#mediaTypeRegistration]
GZIP = "gzip"  # application/gzip, [RFC6713]
H224 = "H224"  # application/H224, [RFC4573]
HELD_XML = "held+xml"  # application/held+xml, [RFC5985]
HTTP = "http"  # application/http, [RFC7230]
INDEX = "index"  # application/index, [RFC2652]
INDEX_CMD = "index.cmd"  # application/index.cmd, [RFC2652]
INDEX_OBJ = "index.obj"  # application/index-obj, [RFC2652]
INDEX_RESPONSE = "index.response"  # application/index.response, [RFC2652]
INDEX_VND = "index.vnd"  # application/index.vnd, [RFC2652]
INKML_XML = "inkml+xml"  # application/inkml+xml, [Kazuyuki_Ashimura]
JAVASCRIPT = "javascript"  # application/javascript, [RFC4329]
JSON = "json"  # application/json, [RFC7158]
MEDIA_CONTROL_XML = "media_control+xml"  # application/media_control+xml, [RFC5168]
MEDIA_POLICY_DATASET_XML = "media-policy-dataset+xml"  # application/media-policy-dataset+xml, [RFC6796]
MEDIASERVERCONTROL_XML = "mediaservercontrol+xml"  # application/mediaservercontrol+xml, [RFC5022]
MP21 = "mp21"  # application/mp21, [RFC6381][David_Singer]
MP4 = "mp4"  # application/mp4, [RFC4337][RFC6381]
MPEG4_GENERIC = "mpeg4-generic"  # application/mpeg4-generic, [RFC3640]
MPEG4_IOD = "mpeg4-iod"  # application/mpeg4-iod, [RFC4337]
MPEG4_IOD_XMT = "mpeg4-iod-xmt"  # application/mpeg4-iod-xmt, [RFC4337]
NSS = "nss"  # application/nss, [Michael_Hammer]
OGG = "ogg"  # application/ogg, [RFC5334]
PDF = "pdf"  # application/pdf, [RFC3778]
PGP_ENCRYPTED = "pgp-encrypted"  # application/pgp-encrypted, [RFC3156]
PGP_KEYS = "pgp-keys"  # , [RFC3156]
PGP_SIGNATURE = "pgp-signature"  # application/pgp-signature, [RFC3156]
PKCS10 = "pkcs10"  # application/pkcs10, [RFC5967]
PKCS7_MIME = "pkcs7-mime"  # application/pkcs7-mime, [RFC5751][RFC7114]
PKCS7_SIGNATURE = "pkcs7-signature"  # application/pkcs7-signature, [RFC5751]
PKCS8 = "pkcs8"  # application/pkcs8, [RFC5958]
PKCS12 = "pkcs12"  # application/pkcs12, [IETF]
PKIX_ATTR_CERT = "pkix-attr-cert"  # application/pkix-attr-cert, [RFC5877]
PKIX_CERT = "pkix-cert"  # application/pkix-cert, [RFC2585]
PKIX_CRL = "pkix-crl"  # application/pkix-crl, [RFC2585]
PKIX_PKIPATH = "pkix-pkipath"  # application/pkix-pkipath, [RFC6066]
PKIXCMP = "pkixcmp"  # application/pkixcmp, [RFC2510]
POSTSCRIPT = "postscript"  # application/postscript, [RFC2045][RFC2046]
PSKC_XML = "pskc+xml"  # application/pskc+xml, [RFC6030]
RDF_XML = "rdf+xml"  # application/rdf+xml, [RFC3870]
RTF = "rtf"  # application/rtf, [Paul_Lindner]
RTPLOOPBACK = "rtploopback"  # application/rtploopback, [RFC6849]
RTX = "rtx"  # application/rtx, [RFC4588]
SGML = "sgml"  # application/SGML, [RFC1874]
SOAP_XML = "soap+xml"  # application/soap+xml, [RFC3902]
SQL = "sql"  # application/sql, [RFC6922]
VCARD_JSON = "vcard+json"  # application/vcard+json, [RFC7095]
VCARD_XML = "vcard+xml"  # application/vcard+xml, [RFC6351]
WIDGET = "widget"  # , [W3C][Steven_Pemberton][ISO/IEC 19757-2:2003/FDAM-1]
X_WWW_FORM_URLENCODED = "x-www-form-urlencoded"  # application/x-www-form-urlencoded, [W3C][Robin_Berjon]
XENC_XML = "xenc+xml"  # application/xenc+xml, [Joseph_Reagle][XENC_Working_Group]
XHTML_XML = "xhtml+xml"  # application/xhtml+xml, [W3C][Robin_Berjon]
XML = "xml"  # application/xml, [RFC7303]
XML_DTD = "xml-dtd"  # application/xml-dtd, [RFC7303]
XML_EXTERNAL_PARSED_ENTITY = "xml-external-parsed-entity"  # application/xml-external-parsed-entity, [RFC7303]
XML_PATCH_XML = "xml-patch+xml"  # application/xml-patch+xml, [RFC7351]
XMPP_XML = "xmpp+xml"  # application/xmpp+xml, [RFC3923]
XOP_XML = "xop+xml"  # application/xop+xml, [Mark_Nottingham]
XSLT_XML = "xslt+xml"  # , [W3C][http://www.w3.org/TR/2007/REC-xslt20-20070123/#media-type-registration]
ZIP = "zip"  # application/zip, [Paul_Lindner]
ZLIB = "zlib"  # application/zlib, [RFC6713]
OCTET_STREAM = 'octet-stream'


def make_content_type(major, minor, encoding=None):
    mime = '{}/{}'.format(major, minor)
    if encoding:
        charset = ';charset={}'.format(encoding)
    else:
        charset = ''
    return headers.Header('Content-Type', mime+charset)

HTML_UTF8 = make_content_type(TEXT, HTML, UTF8)
