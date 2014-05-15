# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Clases para subir archivos

"""
#from apps.utils.messages import Message
import hashlib
import uuid
import time
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from django.conf import settings

class Upload:
	"""
	Clase que permite subir un archivo.
	
	"""
	@staticmethod
	def save_file(filex, path=''):
		""" 
		Little helper to save a file

		Usage::

			from apps.sad.upload import Upload
			Upload.save_file(request.FILES["photo"],"package/")

		Example::
			data = {}
			data ["name"] = "%s" % Upload.save_file(request.FILES["photo"],"personas/")
			return HttpResponse(json.dumps(data))
	    """
		filename = filex._get_name()
		file_list = filename.rsplit('.', 1)
		file_name = "%s.%s" % (hashlib.md5("%s%s" % (uuid.uuid1(), time.time())).hexdigest(), file_list[1])
		# file_ext = file_list[1]

		fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + str(file_name)), 'wb+')
		for chunk in filex.chunks():
			fd.write(chunk)
		# fd.write(filex['content'])
		fd.close()
		return str(path) + str(file_name)


