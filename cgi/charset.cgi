#!/usr/bin/perl

use strict;
use warnings;
use CGI;

#CGI���֥�����������
my $q = CGI -> new;

#HTTP�إå�����(ʸ�������ɻ���)
$q -> charset('EUC-JP');
print $q -> header;

#�Ķ��ѿ��ν���
my $content = <<"EOF";
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>�����ȥ�</title>
	</head>
	<body>
		����ˤ���
	</body>
</html>
EOF

print $content;
