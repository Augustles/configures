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
