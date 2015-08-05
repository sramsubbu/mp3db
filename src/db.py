#uses mysql database to store/retreive data
import MySQLdb
import os
unknown_gen_id = 900 #if a genre is not found in the master data, the unknown genre is used.

def get_data_from_config():
  data = {}
  with open("config") as fp:
    for line in fp.readline():
      key,value = line.split(":")
      data[key] = value
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
  	if not os.path.exists(folder) or if not os.path.isdir(folder):
  		return False #cannot add something that does not exist or not a directory
  	now = None #change to get the current date
  	query = "INSERT INTO folder(folder_addr,last_sync) VALUES('%s','%s');" %(folder,now)
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
      query = "INSERT INTO album(album,composer,year) VALUES('%s','%s', %d);" %(album['name'],album['composer'],album['date'])
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
    	
  def add_song(self, title, album, artist, genre, filepath, id3_version ):
    cur = self.db.cursor()
    
    #check if the record already exists in the database 
    query = "SELECT id FROM song WHERE title = '%s' AND filepath = '%s';" %(title, filepath)
    cur.execute(query)
    res = cur.fetchall()
    if res:
      return False
      
    #add data to the supporting tables first
    genre_id = self.get_genre(genre)
    album_id = self.add_album(album)
    artist_id = self.add_artist(artist)
    
    #add record to the song table
    query = "INSERT INTO song(title,album,genre,filepath, id3_version) VALUES('%s',%d,%d,'%s','%s');" %(title, album_id,genre_id,filepath, id3_version)
    cur.execute(query)
    song_id = cur.lastrowid
    
    #now connect song and artist table records (many to many relationship resolution)
    query = "INSERT INTO song_artist VALUES(%d,%d);" %(song_id,artist_id)
    cur.execute(query)
  
    return True
  def update_file(self,song_id, filepath):
  	cur = self.db.cursor()
  	query = "UPDATE song SET filepath = '%s' WHERE id = %d;" %(filepath,song_id)
  	return cur.execute(query)
  	
