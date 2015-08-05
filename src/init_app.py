from db import DB
from id3 import SongFile, is_id3
import os

def get_all_mp3files(root):
  mp3_files = []
  for dirpath, subdirs, files in os.walk(root):
    for i in files:
      mp3_files.append( os.path.join(dirpath,i) )
      
  #filter out the files that do not contain id3 header
  mp3_files filter(is_id3, mp3_files)
  return mp3_files
  
def init_app(audio_folders):
  mp3_files = []
  for folder in audio_folders:
    mp3_files.extend( get_all_mp3files(folder) )
  
  db_obj = DB()
  for mp3_file in mp3_files:
    id3_obj = SongFile(mp3_file)
    if not db_obj.add_song(id3_obj.title, id3_obj.artist, id3_obj.album, id3_obj.genre, id3_obj.filepath):
      print mp3_file, "failed"
  
  for folder in audio_folder:
    db_obj.add_folder(folder)
    
    
if __name__ == "__main__":
  folders = []
  print "Enter the locations where the audio files exist\nPress Ctrl+D to end the loop"
  while True:
    try:
      folder = raw_input(">>")
      if os.path.exists(folder) and os.path.isdir(folder):
        folders.append(folder)
      else:
        print """Folder name incorrect. It must be the fullpath from the root or the drive name.
        Enter pwd or similar command for assistance"""
    except KeyboardInterrupt:
      break
  init_app(folders)
    
    
