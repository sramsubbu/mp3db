#Read/Write ID3 related data from the mp3 file
from mutagen.easyid3 import EasyID3

def get_mp3_files(root):
  mp3_files = []
  for dirpath, subdirs, files:
    for i in files:
      mp3_files.append( os.path.extend(dirpath,i) )
      


class SongFile:
  def __init__(self, filepath):
    self.fio = EasyID3(filepath) #handle noid3header exception
  
  @property  
  def title(self):
    return self.fio['title'][0].encode('ascii')
  
  @propery
  def album(self):
    album = {}
    album['name'] = self.fio['album'][0].encode('ascii')
    album['composer'] = self.fio['composer'][0].encode('ascii')
    album['date'] = self.fio['date'][0].encode('ascii')
    
  @property
  def artist(self):
    artist = self.fio['artist'][0].encode('ascii')
    artist = artist + ' '
    return artist.split(' ', 1)
    
  @propery
  def genre(self):
    return self.fio['genre'][0].encode('ascii')
    
  @property
  def filepath(self):
    return self.fio.filename
    
      
