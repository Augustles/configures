#stackoverflow vote top 100
1. what is “:-!!” in C code
http://stackoverflow.com/questions/9229601/what-is-in-c-code
2. finding all files containing a text string
    grep -rnw 'directory' -e "pattern"
    find . -iname '.py'|xargs 'hello'
3. git gui client for linux
4. why does the c preprocessor interpret the word 'linux' as the constant '1'
5. how to set chmod a folder and all its subfloders and files in linux ubuntu terminal
6. how do i prompt for input in a linux shell script
read -p 'please enter a word' y
$y
7. how to output mysql query results csv format
SELECT order_id,product_name,qty FROM orders INTO OUTFILE '/tmp/orders.csv' FIELDS TERMINATED BY ','ENCLOSED BY '"'LINES TERMINATED BY '\n';
8. bash: redirect and append both stdout and stderr
python的'w'
    cmd > file.txt
python的'a'
    cmd >> file.txt
2为stderr,1为stdout,0为stdin
将stderr输出2重定向到标准输出1中,&1为标准输出
&可以让bash在后台运行
    cmd >>file.txt 2>&1
9. vim and ctags tips and tricks
10. how to symlink a file in linux
    ln -s /path/to/file /path/to/symlink
11. utf-8 all the way through
http://stackoverflow.com/questions/279170/utf-8-all-the-way-through
12. how to determine whether a given linux is 32 bit or 64 bit
    uname -m
    cat /proc/cpuinfo
13. starting iphone app development in linux
14. how to measure actual memory usage of an application or process
    top/htop
15. how can i update node.js and npm to next versions
    npm update [<name>]
16. remove a symlink to a drectory
    rm /path/symlink
17. how do i use  sudo redrect ouput a location i don't have permission to write
    :x !sudo tee %
18. how do i delete (unset) an expoerted environment variable
    unset
19. looping throught the content of a file in bash
    while read p;
    do
    echo $p
    done < file.txt
20. convert dos line endings to linux endings in vim
21. exclude directory from find. command
http://stackoverflow.com/questions/4210042/exclude-directory-from-find-command
22. how to set a bash variable equal to the output from a command
    o="$(ls -l)"
    echo "${o}"
23. how can i recursively find all files in current and subfolders based on wildcard matching
    find . -name '*.py' 
24. defining a variable with or without export
    export home=/home
    cd $home
    home=3
    echo $home
25. pip to/from clipboard
linux
    cat /dev/clip
mac
    pbcopy
window/cygwin
    cat /dev/clipboard
26. redirect all output to file
    ls > stdout.txt 2> stderr.txt
27. kill detached screen session
http://stackoverflow.com/questions/1509677/kill-detached-screen-session
28. why doesn't 'cd' work in a bash shell script
29. how to download a from a server using ssh
    scp your_username@remotehost.edu:foobar.txt /local/dir
30. what is linux's native gui api
    gnome,kde,unity,xfce
31. downloading java jdk on linux via wget is shown license page instead
http://stackoverflow.com/questions/10268583/downloading-java-jdk-on-linux-via-wget-is-shown-license-page-instead
32. dude, where's my php.in
    php -r "phpinfo();" | grep php.ini
33. how can i use grep to show just filenames on linux
http://stackoverflow.com/questions/6637882/how-can-i-use-grep-to-show-just-filenames-no-in-line-matches-on-linux
34. how to change the output color of echo in linux
http://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
35. how to expand/collapse a diff sections in vimdiff
http://stackoverflow.com/questions/5288875/how-to-expand-collapse-a-diff-sections-in-vimdiff
36. merge/convert multiple pdf files into one pdf
http://stackoverflow.com/questions/2507766/merge-convert-multiple-pdf-files-into-one-pdf
37. best way to kill all child processes
http://stackoverflow.com/questions/392022/best-way-to-kill-all-child-processes
38. Socket options SO_REUSEADDR and SO_REUSEPORT, how do they differ? Do they mean the same across all major operating systems?
http://stackoverflow.com/questions/14388706/socket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t
39. shell command to tar directory excluding certain files/folder
    tar --exclude='file1' --exclude='patter*' --exclude='file2'
40. using is to list directories and their total sizes
    du -sh /path
41. how do i know script file name in a bash script
    me=`basename "$0"`
42. how can i write a here doc to a file in bash script
43. how do i test if a variables is a number in bash
44. how to 'grep' a continous stream
45. how to count lines in a document
    wc -l /path/to/file
46. why does printf not flush after the call unless a newline is in the format string
47. i never really understood: what is posix
48. where is my httpd.conf located apached
49. how do i write stderr to a file while using 'tee' with a pipe
50. what does the number in parentheses shown after unix command names mean
51. Linux: Prevent a background process from being stopped after closing SSH client
52. is there a way for non-root processes to bind to 'privileged' ports
53. need a good hex editor for linux
54. how to get full path of a file
55. unix shell script find out which directory the script file reside
56. how to have the cp command create any necessary folders for copying a file to destination
57. get current time in seconds since the epoch on linux, bash
58. set screen names with gnu screen
59. how to redirect output to a file and stdout
60. who 'killed' my process and why
61. aborting a shell script if any command returns a non-zero value
62. how can i get 'find' to ignore .svn directories
63. getting root permission on a file inside of vi
64. grep, but only certain file extensions
65. how do send a file  as email attachment using linux command line
66. how to compare strings in bash script
67. graphical diff programs for linux
68. print a file skipping x lines in bash
69. how to run process as background an never die
70. are there any standard exit status codes in linux
71. how to list the contents of a package using yum
72. quickly create al large file on a linux system
73. how to find out which processes are swapping in linux
74. what is the ld_preload trick
75. can a shell script set environment variables of the calling shell
76. sudo echo “something” >> /etc/privilegedFile doesn't work… is there an alternative?
77. how to list all users in a linux group
78. given two directory trees, how can i find out which file differ
79. how do you recursively ftp a folder in linux
80. how to join multiple lines of file names into one with custom delimiter
81. exclude .svn directories from grep
82. good linux svn client
83. sleep for milliseconds
84. append one file to another in linux
85. get program execution time in the shell
86. how do i find my rsa key fingerprint
87. peak memory usage of a linux/unix process
88. is there a c++ gdb gui for linux
89. how to permanently set $path on linux
90. bash: how __best__ to include other scripts
91. mysql_config not found when installing mysqldb python interface
92. threads vs processes in linux
93. Why does “while(true)” without “Thread.sleep” cause 100% CPU usage on Linux but not on Windows?
94. is there a command to list all unix group names
95. how to add default include path for gcc in linux
96. why use python's os module methods instead of executing shell commands directly
97. how can i exclude directories from grep -r
98. ./configure :/bin/sh^M :bad interpreter
99. error: could not find or load main class
100. how to kill all precesses with a given partial name

1. how do i output color text to linux terminal
2. what linux/unix commands are outdated and have powerful alternatives
3. how to write cd command in makefile
4. how to recursively find and list the lastest
5. iptables remove specific rules
6. how should strace be used 
7. bash: pipe output and capture exist status
8. how does `cat << EOF` work in bash
9. how to see top processes by actual memory usage
10. argument list too long error for rm,cp,mv commands
find . -name "*.pdf" -print0 | xargs -0 rm
11. linux command to print directory structure in the form of a tree
sudo apt-get install tree
12. clear the ubuntu bash screen for real
printf "\033c"
13. simulate delayed and droped packets on linux
14. is it safe to parse a /proc/file
15. how is linux kernel tested
16. android debug bridge (adb) device no permissions
17. restarting cron after changing crontab file
18. how do i check syntax in bash without running the script
19. what does 'opt' mean (as in the 'opt' directory) is it an abbreviation
20. how to remove all .svn drectories from my application directories
21. linux command to list all available commands and aliases
22. virtual memory usage from java under linux, too much memory used
23. set up device from development (????? no permissions)
24. how to force cp to overwrite without confirmation
25. what's an easy way to read random line from a file in unix command line
26. make $java_home easily changable in ubuntu
27. linux equivalent of the mac os x 'open' command
28. force unmount of nfs-mounted directory
29. maximum number of  threads per process in linux
30. why do you need to put #!/bin/bash at the beginning of a script file
31. how to know mysql my.cnf location
32. how can i copy the output of a command directly into my clipboard
33. how can i use xargs to copy files that have spaces and quotes in their names
34. bash tool to get nth line from a file
35. create a symbolic link of directory in ubuntu
36. how do i get windows to go as fast as linux compiling c++
37. httpd: could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for servername
38. how do i get curl to not show progress bar
39. id cannot find an existing library
40. how to get console window width in python
41. centos 64 bit bad elf interpreter
42. network usage top/htop on linux
43. why main does not return 0 here
44. http post and get using curl in linux
45. finding current executable's path without /proc/self/exe
46. svn checkout the contents of a folder, not the folder itself
47. extract file basename without path and extension in bash
48. command line csv viewer
49. how can i format my grep output show line numbers at the end of the line, and the hit count
50. how to find the location of the executable in c
