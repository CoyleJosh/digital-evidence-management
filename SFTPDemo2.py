import paramiko, os
#paramiko.util.log_to_file('/tmp/paramiko.log')
#innerDirPath = "C:/Users/admin/Dropbox/University/CSEE3/CE301/University Project/Evidence Folder"
#remoteDirTest = "/private/var/mobile/Media/DCIM/100APPLE/IMG_0012.JPG"

# Open a transport

host = "127.0.0.1"
port = 22
transport = paramiko.Transport((host, port))

# Auth

password = "baconpancakes"
username = "root"
transport.connect(username = username, password = password)

# Go!

sftp = paramiko.SFTPClient.from_transport(transport)

# Download
filename = "IMG_0012.JPG"
sftp.get("/private/var/mobile/Media/DCIM/100APPLE" + filename, "C:/Users/admin/Desktop/putthingsinsideme")

# Close

sftp.close()
transport.close()
