from socket import *
from requests.packages.urllib3.contrib import pyopenssl as reqs

def get_possible_domain():
    text = "microsoft"
    textchanged = text
    rank = 0
    ascii_values = []
    possible_mot = []
    for character in range(len(text)-1):
        try:
            textchanged = textchanged[1:]
        except:
            textchanged = ""
        
        for i in range(97,123):
            if rank == 0:
                result=chr(i)+textchanged
            elif rank < len(text):
                result=text[:rank]+chr(i)+textchanged
            else:
                result=text[:rank]+chr(i)
            possible_mot.append(result)
        rank = rank + 1
    list_domain = [s + ".com" for s in possible_mot]
    print(list_domain)
    return(list_domain)

def https_cert_subject_alt_names(host, port):
    """Read subject domains in https cert from remote server"""
    print(host,port)
    setdefaulttimeout(3)
    x509 = reqs.OpenSSL.crypto.load_certificate(
        reqs.OpenSSL.crypto.FILETYPE_PEM,
        reqs.ssl.get_server_certificate((host, port))
    )
    return reqs.get_subj_alt_name(x509)
    
if __name__ == '__main__':
    result={}
    for elem in get_possible_domain():
        try:
            domains = https_cert_subject_alt_names(elem, 443)
            if isinstance(domains, list):
                result[elem] = domains
                print(type(domains), domains)
        except:
            pass
    
    for elem in result:
        if len(dict_result[elem]):
            for element in range(len(dict_result[elem])):
                if "microsoft" in dict_result[elem][element][1]:
                    last_result[elem] = dict_result[elem]
    print(last_result)