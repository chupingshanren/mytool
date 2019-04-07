from subprocess import call

IDM = r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
DownUrl = r'http://music.163.com/song/media/outer/url?id=1331535573.mp3'
DownPath = r'C:\Users\22129\mytool\Music\周杰伦'
OutPutFileName = '1.mp3'
call([IDM, '/d',DownUrl, '/p',DownPath, '/f', OutPutFileName, '/n', '/a'])
call([IDM, '/d',DownUrl, '/p',DownPath, '/f', '2.mp3', '/n', '/a'])
call([IDM, '/s'])
#, '/a'
