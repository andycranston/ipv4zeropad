# A web based CGI script to zero pad IPv4 addresses to make them easier to sort

## For the really impatient --> Demo video

For a demonstration look at this:

[Sorting by IPv4 addresses in Excel](https://www.youtube.com/watch?v=-cfEYPztbn0)

it shows the `ipv4zeropad.py` CGI script being used to zero pad a column
of IPv4 addresses in a spreadsheet so the spreadsheet can be properly
sorted by IPv4 address.

## Background

Sorting IPv4 addreses can be tricky.  For example sorting the following
list of IP addresses in Excel:

```
192.168.1.11
192.168.1.213
192.168.1.100
192.168.1.2
```

will result in this:

```
192.168.1.100
192.168.1.11
192.168.1.2
192.168.1.213
```

which is probably not what you want.

Many applications similar to Excel will do the same.

Why is this?  Well it is because Excel is treating the IPv4
addresses as strings.

If we could convert the IPv4 addresses to a zero padded format like this:

```
192.168.001.011
192.168.001.213
192.168.001.100
192.168.001.002
```

then they should sort correctly as:

```
192.168.001.002
192.168.001.011
192.168.001.100
192.168.001.213
```

This is where the `ipv4zeropad.py` CGI script comes in.

## How to use the `ipv4zeropad.py` CGI script

Open a web browser and point it to the web server you have installed the
`ipv4zeropad.py` CGI script (see below for hints on how to do this).

If you do not want to go to the trouble of installing the script
then you can use my web server at this URL:

http://cranstonhub.com/cgi-bin/ipv4zeropad.py

From your application copy the list of unsorted IPv4 addresses and paste
them into the text input box on the left hand side.

Next click the `Click to zero pad the IPv4 addresses` button.

The text box on the right hand side should now display the IPv4
addresses in zero padded format (e.g. 10.234.1.70 will be displayed
as 010.234.001.070).

Select and copy the zero padded IPv4 addresses from the right hand side
text input box and paste them back into your application.

Finally use the sort function in your application to sort on the zero
padded IPv4 addresses.

## Installing the `ipv4zeropad.py` CGI script

There are many web servers and several ways to configure CGI
scripting on each one so I cannot go into every possible
configuration but I will explain how I set this up using the open source
`lighttpd` web server running on Linux.  Details on `lighttpd` are here:

[Lighttpd - fly light](https://www.lighttpd.net/)

First ensure Python 3 is installed on your Linux server and that the
Python 3 interpreter can be started by typing:

```
/usr/bin/python3
```

at the command prompt.

A directory called `cgi-bin` must exist under the document
root directory.  In my setup the directory I needed to create was:

```
/home/andyc/www/cgi-bin
```

Into this directory copy the following two files from my GitHub repository:

```
ipv4zeropad.css
ipv4zeropad.py
```

Set the following file permissions on these two files:

```
cd /home/andyc/www/cgi-bin
chmod u=rw,go=r ipv4zeropad.css
chmod u=rwx,go=rx ipv4zeropad.py
```

In the `lighttpd.conf` configuration file ensure these lines are present:

```
"mod_cgi",
```

is under the `server.modules =` section.

Ensure there is a:

```
cgi.assign =
```

section and that under this section is the line:

```
".py" => "/usr/bin/python3",
```

Finally restart the `lighttpd` web server so any changes to
the `lighttpd.conf` file are applied:

```
sudo service lighttpd restart
```

Now access the `ipv4zeropad.py` CGI script from a web browser with
a URL similar to:

```
http://youwebservername/cgi-bin/ipv4zeropad.py
```

Good luck!

## Andy Cranston's `lighttpd.conf` configuration file

As getting CGI scripting up and running on a web server can be
tricky I have copied below the `lighttpd.conf` file I use
on my development machine.  It may help...

```
server.modules = (
  "mod_cgi",
)

server.document-root        = "/home/andyc/www"
server.username             = "andyc"
server.groupname            = "general"
server.port                 = 80
server.errorlog             = "/var/log/lighttpd/error.log"
server.pid-file             = "/var/log/lighttpd/lighttpd.pid"
server.breakagelog          = "/var/log/lighttpd/breakage.log"

index-file.names            = ( "index.htm", "index.html" )

mimetype.assign = (
  ".html" => "text/html",
  ".htm" => "text/html",
  ".css" => "text/css",
  ".txt" => "text/plain",
  ".jpg" => "image/jpeg",
  ".png" => "image/png",
)

cgi.assign = (
  ".py" => "/usr/bin/python3",
  ".cgi" => "",
)
```

---------------------------------------------------------

End of README.md
