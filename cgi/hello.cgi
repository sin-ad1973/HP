#!/usr/bin/perl

use strict;
use warnings;
use CGI;

#CGI���֥�����������
my $q = CGI->new;

#HTTP�إå�����
print $q -> header;

my $title = "Title";
my $message = "Helo World";

#�ҥ��ɥ������
my $content = <<"EOS";
<html>
	<head>
		<title>$title</title>
	</head>
	<body>
		<h1>$message</h1>
	</body>
</html>
EOS

print $content;

