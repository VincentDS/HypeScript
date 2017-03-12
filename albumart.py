from bs4 import BeautifulSoup
import os
import eyed3
import simplejson
import cStringIO
import urllib
import urllib2
import requests
import cookielib
import json


def main():
  os.chdir("./songs")
  for name in os.listdir('.'):
    if os.path.isfile(name) and name.endswith('.mp3'):
      song = eyed3.load(name)
      artist = song.tag.artist
      title = song.tag.title
      if not song.tag.images:
        art = get_album_art(artist, title)
        imagedata = open(art,"rb").read()
        song.tag.images.set(3, imagedata, "image/jpeg")
        song.tag.save();

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def get_album_art(artist, title):
  print '\tFETCHING ALBUM ART....'
  song = u'\t{} - {}'.format(artist, title).encode('utf-8')
  print song
  searchTerm = urllib.quote_plus(song)
  url="https://www.google.co.in/search?q="+searchTerm+"&source=lnms&tbm=isch"

  header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
  soup = get_soup(url,header)

  a = soup.find("div",{"class":"rg_meta"})
  img_link, img_type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]

  try:
      req = urllib2.Request(img_link, headers={'User-Agent' : header})
      raw_img = urllib2.urlopen(req).read()
      if len(img_type)==0:
        name = "image.jpg"
      else:
        name = "image."+img_type
      f = open(os.path.join(name), 'wb')
      f.write(raw_img)
      f.close()
      return name
  except Exception as e:
      print "could not load : "+ img_link
      print e

main()
