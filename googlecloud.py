import requests
import signal
import sys

graph_api_version = 'v2.12'
access_token = 'EAACEdEose0cBACBSZBLD8NM47r8r4CzT5Na9VlXuDBvjndkU3PneJVmjlZBhasf7bZBQADxD6HAGrURsjspnn7EozEwvQQ2I6UtGV4k3fsKvm4ZCsxJuPYnmqgG1FsxkwTh58KK79H4Is4VgDhZAG6KJpYZBEq07dzVOCeaFQVjyqqSn0v3ZCNZBOZBBU384BQyUZD'

user_id = '37107394336'

url = 'https://graph.facebook.com/{}/{}?fields=posts'.format(graph_api_version, user_id)

posts = [];

limit = 325

def write_comments_to_file(filename):
    print()
    
    if len(posts) == 0:
        print ("No posts to write.")
        return
    with open(filename, 'w', encoding='utf-8')as f:
        for post in posts:
            f.write(post + '\n')
    print ("Wrote {} posts to {}".format(len(posts), filename))
    
    
    #registrar una señal para que se pueda salir antes
def signal_handler(signal, frame):
    print('Keyboard interrupt')
    write_comments_to_file('posts.txt')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

r = requests.get(url, params={'access_token':access_token})
i=1
while True:
    data = r.json()
    if 'error' in data:
        raise Exception(data['error']['message'])
    
    if i==1:
        datos=data['posts']['data']
    else:
        datos=data['data']
        
    for post in datos:
        #remove line breajjs in each comment
        text = post['message'].replace('\n', ' ')
        posts.append(text)
        
    print('Got {} posts, total:{}'.format(len(datos), len(posts)))
    
    
    if  0<limit<=len(posts):
        break
    if i==1:
        pag=data['posts']
        paginas=data['posts']['paging']
        req=data['posts']['paging']['next']
    else:
        pag=data
        paginas=data['paging']
        req=data['paging']['next']
        
    if 'paging' in pag and 'next' in paginas:
        r=requests.get(req)
        print("true")
        
    else:
        #break
        print("break")
        
    write_comments_to_file('posts.txt')
    
    i=i+1
    
    
    