#!/usr/bin/perl

use strict;
use warnings;
use CGI;

#CGI���֥�����������
my $q = CGI -> new;
$q -> charset('EUC-JP');

#Form�������
my $message = $q -> param('message');

$message = $q -> escapeHTML($message);

#HTTP�إå�����
print $q -> header;

my $contents = <<"EOF";
<html>
	<head>
		<meta http-equiv="Contents-Type" content="text/html;charset=EUC-JP">
		<title>Form�������</title>
	</head>
	<body>
		<center>$message</center>
	</body>
</html>
EOF

print $contents;
