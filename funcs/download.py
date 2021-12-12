from pytube import YouTube


class Descargar:

    def __init__(self,path) -> None:
        self.path = path
    
    def mp3_viaPytube(self,link:str):
        '''Download mp3 songs from youtube [Pytube]'''
        
        yt = YouTube(
            url=link
        )

        try:
            dl = yt.streams.filter(
                only_audio=True
            ).first()
            
            dl.download(
                output_path=self.path,
                filename=f'{yt.title.replace("/","|")}-{yt.video_id}.mp3'
            )
            
        
        except Exception as E:
            return 0
        
        return yt