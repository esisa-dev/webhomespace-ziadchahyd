Flask File Explorer

This is a Flask application that allows users to explore the files and directories on their system, search for files, download their home directory, and check the number of files and directories in their home directory.


Functionality

Login

-Users are required to log in before they can access the application. The application authenticates users against the system's /etc/shadow file.

File Explorer

-Once authenticated, users can navigate the file system by clicking on directories in the table. They can also click on files to view their content, if they are text files and shows them in a table Column called Content. Hidden files are not displayed.

Search

-Users can search for files and directories containing a particular string by entering the string in the search bar.

Download Home Directory

-Users can download their home directory as a zip file by clicking the "Download Home Directory" button. This button will generate a zip file containing all of the user's files and directories.

Count Files and Directories

-Users can view the number of files and directories in their home directory by clicking the "Count Files" and "Count Directories" buttons, respectively.

Disk Space

Users can view their disk usage statistics, including total space, used space, and free space, by clicking the "Disk Space" button.