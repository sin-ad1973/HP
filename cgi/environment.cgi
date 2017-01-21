#!/usr/bin/perl

use strict;
use warnings;
use CGI;

#CGI���֥�����������
my $q = CGI -> new;

#HTTP�إå�����
print $q -> header;

#�Ķ��ѿ��ν���
my $content = <<"EOF";
<html>
	<head>
		<title>Environment Variable</title>
	</head>
	<body>
		<h1>Evironment Variables</h1>
		<table border="1">
			<tr>
				<td>DOCUMENT_ROOT</td>
				<td>$ENV{DOCUMENT_ROOT}</td>
			</tr>
			<tr>
				<td>SERVER_NAME</td>
				<td>$ENV{SERVER_NAME}</td>
			</tr>
			<tr>
				<td>SCRIPT_NAME</td>
				<td>$ENV{SCRIPT_NAME}</td>
			</tr>
		</table>
	</body>
</html>
EOF

print $content;
