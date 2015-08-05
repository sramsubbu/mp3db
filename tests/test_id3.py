from nose.tools import *
from mp3db.id3 import is_id3,SongFile

def test_is_id3():
  test_data_pass= ["/home/ramsubbu/Music/myway_sinatra.mp3"] #list of files which contain id3v2 tags 
  test_data_fail = ["/home/ramsubbu/Music/nitro.mp3"] #list of files that do not contain id3v2 tags 
  #pass condition
  for test_data in test_data_pass:
    assert_true( is_id3(test_data) )
    
  #fail condition 
  for test_data in test_data_fail:
    assert_false( is_id3(test_data) )

def test_songfile():
    test_data = "/home/ramsubbu/testdocs/test.mp3"
    obj= SongFile(test_data)
    artist = obj.artist
    try:
        assert_equals(artist[0] ,"Arijit")
        assert_equals(artist[1], "Singh")
    except Exception, e:
        print e

  
