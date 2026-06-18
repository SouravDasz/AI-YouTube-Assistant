from urllib.parse import urlparse,parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator

#Function for extract id from url
def get_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in (
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com"
    ):
        return parse_qs(parsed_url.query).get("v", [None])[0]

    return None

def group_by_time(transcript,time=20):
    chunks=[]
    current_chunks=[]
    st=None
    ed=None
    for t in transcript:
        if st is None:
            st=t.start
        current_chunks.append(t.text)
        ed=t.start+t.duration
         #check for 20 sec
        if (ed-st) >=time:
            chunks.append({"text":" ".join(current_chunks),
                "start":st,
                "end":ed})
            current_chunks=[]
            st=None
            ed=None
    if current_chunks:
        chunks.append({
            "text":" ".join(current_chunks),"start":st,"end":ed
        })
    return chunks

#for translating 


            
        
        

def context_retival(youtube_url:str):
    video_id=get_video_id(youtube_url)
    
    ytt_s=YouTubeTranscriptApi()
    transcript_list=ytt_s.list(video_id)
    try:
        transcript=transcript_list.find_transcript(["en"])
        data=transcript.fetch()
        chunks=group_by_time(data,time=20)
        return chunks 
    except:
        transcript=None
        for t in transcript_list:
            transcript=t
            break
        data=transcript.fetch()
        chunks=group_by_time(data,time=20)
        translater=GoogleTranslator(source="auto",target="en")
        for chunk in chunks:
            text=chunk["text"]
            translate_text=translater.translate(text)
            chunk["text"]=translate_text

        return chunks


        
            


#print(context_retival("https://youtu.be/eNDVp-hxiic?si=sE7ZqX7eDS8O6Cgd"))
    