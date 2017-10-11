from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
from disk.models import FileInfo
from django.utils import timezone
import os

# Create your views here.

def index(request):
	return render(request, 'disk/index.html')

def upload(request):
	if request.method == "POST":
		myFile = request.FILES.get('upfile')
		if not myFile:
			return HttpResponse('no file is uploaded')

		file = myFile.read()
		if not file:
			return HttpResponse('The file is not exists')

		md5 = hashlib.md5(file).hexdigest()
		filename = myFile.name
		filesize = myFile.size
		fileInfo = FileInfo.objects.filter(md5=md5)

		if not fileInfo:
			try:
				with open('disk/files/{}'.format(md5), 'wb') as fn:
					fn.write(file)
					print('try: files/disk')
			except Exception as e:
				THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
				my_file = os.path.join(THIS_FOLDER, 'files/{}'.format(md5))
				print('except-before: /files/disk')
				with open(my_file, 'wb') as fn:
					fn.write(file)
					print('except-after: /files/disk')
			else:
				print('no exception: 666')
				pass
			finally:
				print('finally: 886')
				pass

		files = {
			'name': myFile.name,
			'size': myFile.size,
			'downloads': 0,
			'created_date': timezone.now(),
			'url':'/disk/files/{}'.format(myFile.name)
		}

		FileInfo(name=filename,size=filesize,md5=md5).save()
		# return render(request, 'disk/uploadfiles.html', {'files': files})
		return HttpResponseRedirect('/disk/s/{}'.format(md5))
	else:
		return HttpResponse('GET')


def download_list(request, md5):
	fileInfo = FileInfo.objects.filter(md5=md5)
	if not fileInfo:
		return HttpResponse('The file is not exists or has been deleted.')

	# context = {
	# 	'name': fileInfo[0].name,
	# 	'size': fileInfo[0].size,
	# 	'url':'/disk/files/disk/{}'.format(fileInfo[0].name)
	# }
	# return render(request, 'disk/downloadfiles.html', context=context)

	files = {
		'name': fileInfo[0].name,
		'size': fileInfo[0].size,
		'downloads': fileInfo[0].downloads,
		'created_date': fileInfo[0].created_date,
		'url':'/disk/files/{}'.format(fileInfo[0].name)
	}

	# FileInfo(name=filename,size=filesize,md5=md5).save()
	# return render(request, 'disk/uploadfiles.html', {'files': files})
	# return HttpResponseRedirect('/disk/s/{}'.format(md5))
	return render(request, 'disk/uploadfiles.html', {'files': files})

def download_detail(request):
	referer = request.META.get('HTTP_REFERER')	
	if not referer:
		return render(request, 'disk/error_404.html')

	md5 = referer[-32:]
	fileinfo = FileInfo.objects.filter(md5=md5)
	if not fileinfo:
		return render(request, 'disk/error_404.html')

	file = None
	try:
		file = open('files/{}'.format(md5), 'rb').read()
	except Exception as e:
		THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		my_file = os.path.join(THIS_FOLDER, 'files/{}'.format(md5))
		file = open(my_file, 'rb').read()		
	else:
		pass
	finally:
		pass

	fileinfo[0].downloads = fileinfo[0].downloads + 1
	fileinfo[0].save()
	response=HttpResponse(file)
	response['Content-type'] = 'application/octet-stream'
	return response