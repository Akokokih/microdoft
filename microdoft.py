from socket import *
from requests.packages.urllib3.contrib import pyopenssl as reqs
import csv

def get_possible_domain():
    text = "microsoft"
    textchanged = text
    rank = 0
    ascii_values = []
    possible_mot = []
    for character in range(len(text)):
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
    return(list_domain)

def https_cert_subject_alt_names(host, port):
    """Read subject domains in https cert from remote server"""
    print("Trying host : ",host,port)
    setdefaulttimeout(3)
    x509 = reqs.OpenSSL.crypto.load_certificate(
        reqs.OpenSSL.crypto.FILETYPE_PEM,
        reqs.ssl.get_server_certificate((host, port))
    )
    return reqs.get_subj_alt_name(x509)
    
def export_file(file_name, json_dict):
    myCsv = csv.writer(open(file_name, 'w'))
    for key in json_dict:
        myCsv.writerow([key, json_dict[key]])
    
if __name__ == '__main__':
    result={}
    last_result={}
    for elem in get_possible_domain():
        try:
            domains = https_cert_subject_alt_names(elem, 443)
            if isinstance(domains, list):
                result[elem] = domains
        except:
            pass
    
    for elem in result:
        if len(result[elem]):
            for element in range(len(result[elem])):
                if "microsoft" in result[elem][element][1]:
                    last_result[elem] = result[elem]
    export_file('Item.csv', last_result)