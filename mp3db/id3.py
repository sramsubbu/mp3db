#Read/Write ID3 related data from the mp3 file
from mutagen.easyid3 import EasyID3

def is_id3(filepath):
  with open(filepath) as fp:
    return fp.read(3) == "ID3"

class SongFile:
  def __init__(self, filepath):
    self.fio = EasyID3(filepath) #handle noid3header exception
  
  @property  
  def title(self):
    try:
        return self.fio['title'][0].encode('ascii')
    except KeyError, e:
        return "Unknown"
  
  @property
  def album(self):
    album = {}
    keys = ['name', 'composer', 'date']
    for key in keys:
        try:
            album[key] = self.fio[key][0].encode("ascii")
        except KeyError:
            album[key] = "Unknown"
    if album['date'] != "Unknown":
        album['date'] = int(album['date'])
    else:
        album['date'] = -1
    return album
    
  @property
  def artist(self):
    try:
        artist = self.fio['artist'][0].encode('ascii')
    except KeyError:
        artist = "Unknown"
    artist = artist + ' '
    return artist.split(' ', 1)
    
  @property
  def genre(self):
    try:
        return self.fio['genre'][0].encode('ascii')
    except KeyError:
        return "Unknown"
    
  @property
  def filepath(self):
    return self.fio.filename
    
      
