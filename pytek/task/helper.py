from slugify import slugify
from urllib.parse import urlparse
import re
import os

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def unique_slug_generator_name_category(instance, new_slug = None, category = True): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.name) 
    Klass = instance.__class__ 
    qs_count = Klass.objects.count()
    if qs_count != 0:
        if category: 
            ct =  str(instance.category).encode('utf-8')
            slug = "{slug}-{countstr}-{category}".format( 
                slug = slug, countstr = qs_count, category = slugify(ct))  
        else:
            slug = "{slug}-{countstr}".format( 
                slug = slug, countstr = qs_count)  
    return slug 


def youtube_url_validation(str):

    regex = ('(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
     
    p = re.compile(regex)

    if (str == None):
        return False

    if(re.search(p, str)):
        return True
    else:
        return False

def get_filename(path):
    return os.path.basename(path)


def get_files_from_db(repo, model, serializer, product_id):
    postImageRepo = repo(model)
    prductFiles = postImageRepo.get_by_product_id(product_id)
    if prductFiles:
        prductFiles = serializer(prductFiles, many = True)
        prductFiles = prductFiles.data[:]

    return prductFiles
