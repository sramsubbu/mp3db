from nose.utils import *
from mp3db import id3

def test_is_id3():
  test_data_pass= [] #list of files which contain id3v2 tags 
  test_data_fail = [] #list of files that do not contain id3v2 tags 
  #pass condition
  for test_data in test_data_pass:
    assert_true( is_id3(test_data) )
    
  #fail condition 
  for test_data in test_data_fail:
    assert_fail( is_id3(test_data) )
  
