#uses mysql database to store/retreive data
import MySQLdb
import os
unknown_gen_id = 900 #if a genre is not found in the master data, the unknown genre is used.

def get_data_from_config():
  data = {}
  with open("../config") as fp:
    for line in fp.readlines():
        key,value = line.split(":",1)
        data[key] = value.strip()
  return data
  

class DB:
  def __init__(self):
    self.cdata = get_data_from_config()
    self.db = MySQLdb.connect(user = self.cdata['username'], passwd = self.cdata['password'], db = self.cdata['database'] )
    self.NO_COMMIT = False
     
  def __del__(self):
    if not self.NO_COMMIT:
      self.db.commit()
    self.db.close()
  
  def add_folder(self,folder):
  	if not os.path.exists(folder) or not os.path.isdir(folder):
  		return False #cannot add something that does not exist or not a directory
  	query = "INSERT INTO folder(folder_addr,last_sync) VALUES('%s',NOW());" %(folder)
  	cur = self.db.cursor()
  	cur.execute(query)
  	
  def update_folder(self,folder_id, sync_date):
  	cur =self.db.cursor()
  	query = "UPDATE folders SET last_sync = '%s' WHERE id = %d;" %(sync_date,folder_id)
  	cur.execute(query)
    
  def add_artist(self,artist):
    cur = self.db.cursor()
    query = "SELECT id FROM artist WHERE fname = '%s' AND lname = '%s';" %(artist[0], artist[1])
    cur.execute(query)
    res = cur.fetchall()
    if res:
	    return res[0][0]
    else:
      query = "INSERT INTO artist(fname,lname) VALUES('%s','%s');" %(artist[0],artist[1])
      cur.execute(query)
      return cur.lastrowid
      
  def add_album(self,album):
    cur = self.db.cursor()
    query = "SELECT id FROM album WHERE name = '%s';" %(album['name'])
    cur.execute(query)
    res = cur.fetchall()
    if res:
	    return res[0][0]
    else:
      query = "INSERT INTO album(name,year) VALUES('%s', %d);" %(album['name'],album['date'])
      cur.execute(query)
      return cur.lastrowid
      
  def get_genre(self,genre):
    cur = self.db.cursor()
    query = "SELECT id FROM genre WHERE genre = '%s';" %(genre)
    cur.execute(query)
    res = cur.fetchall()
    if res:
    	return res[0][0]
    else:
    	return unknown_gen_id
    	
  def add_song(self, title, album, artist, genre, filepath, id3_version  = "id3v2"):
    cur = self.db.cursor()
    
    #check if the record already exists in the database 
    query = "SELECT id FROM song WHERE title = '%s' AND file_path = '%s';" %(title, filepath)
    cur.execute(query)
    res = cur.fetchall()
    if res:
      return False
      
    #add data to the supporting tables first
    genre_id = self.get_genre(genre)
    album_id = self.add_album(album)
    artist_id = self.add_artist(artist)
    
    #add record to the song table
    query = "INSERT INTO song(title,album,genre,file_path) VALUES('%s',%d,%d,'%s');" %(title, album_id,genre_id,filepath)
    cur.execute(query)
    song_id = cur.lastrowid
    
    #now connect song and artist table records (many to many relationship resolution)
    query = "INSERT INTO song_artist VALUES(%d,%d);" %(song_id,artist_id)
    cur.execute(query)
  
    return True
  def update_file(self,song_id, filepath):
  	cur = self.db.cursor()
  	query = "UPDATE song SET file_path = '%s' WHERE id = %d;" %(filepath,song_id)
  	return cur.execute(query)

if __name__ == "__main__":
    data = get_data_from_config()
    db = DB()

    from mutagen.easyid3 import EasyID3
    obj = EasyID3("/home/ramsubbu/testdocs/test.mp3")
    title = obj['title'][0].encode("ascii")
    artist = obj['artist'][0].encode("ascii")
    artist += " "
    artist = artist.split(" ",1)
    album = {}
    album['name'] = obj['album'][0].encode("ascii")
    album['date'] = int(obj['date'][0].encode("ascii"))
    album['composer'] = obj['composer'][0].encode("ascii")
    genre = obj['genre'][0].encode("ascii")
    filepath = obj.filename

    db.add_song(title = title, artist =artist, album = album, genre = genre, 
    filepath = filepath, id3_version = "id3v2")



    
  	
