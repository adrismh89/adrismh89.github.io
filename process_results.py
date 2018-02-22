
import signal
import sys

from google.cloud import language, exceptions

def detect_sentiment(text):
    
    document=language.types.Document(content=text,type=language.enums.Document.Type.PLAIN_TEXT)
    sentiment=client.analyze_sentiment(document).document_sentiment
    return sentiment.score, sentiment.magnitude

count=0
postitive_count=0
neutral_count=0
negative_count=0

def print_summary():
    print()
    print('Total comments analysed:{}'.format(count))
    print('Positivo:{}({:.2%})'.format(postive_count ,postive_count/count))
    print('Neutral:{}({:.2%})'.format(neutral_count,neutral_count/count))
    print('Negativo:{}({:.2%})'.format(negative_count,negative_count/count))
    

def signal_handler(signal, frame):
    print('KeyboardInterrupt')
    print_summary()
    sys.exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

with open('comments.txt',encoding='utf-8')as f:
    for line in f:
        try:
            score,mag=detect_sentiment(line)
        except exceptions.BadRequest:
            continue
            
        count+=1
        
        if score>0:
            positive_count+=1
        elif score<0:
            negative_count+=1
        else:
            neutral_count+=1
        
        positive_proportion=positive_count/count
        neutral_proportion=neutral_count/count
        negative_proportion=negative_count/count
        
        print('Count:{},Postive:{:.3f},Neutral:{:.3f},Negative:{:.3f}'.format(count,positive_proportion,neutral_proportion,negative_proportion))
        

print_summary()