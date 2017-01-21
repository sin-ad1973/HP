#!/usr/bin/perl

use strict;
use warnings;
use CGI;

#CGI���֥�����������
my $q = CGI -> new;
$q -> charset('EUC-JP');

#Form�������
my $name = $q -> param('name');
my $sex = $q -> param('sex');
my $job = $q -> param('job');
my $message = $q -> param('message');

my @hobbys = $q -> param('hobby');
my $hobby = join(',', @hobbys);
my @foods = $q -> param('food');
my $food = join(',', @foods);

$name = $q -> escapeHTML($name);
$sex = $q -> escapeHTML($sex);
$job = $q -> escapeHTML($job);
$hobby = $q -> escapeHTML($hobby);
$food = $q -> escapeHTML($food);
$message = $q -> escapeHTML($message);

#HTTP�إå�����
print $q -> header;

my $contents = <<"EOF";
<html>
	<head>
		<meta http-equiv="Contents-Type" content="text/html;charset=EUC-JP">
		<title>Form�������2</title>
	</head>
	<body>
		<div>
			̾����$name
		</div>
		<div>
			���̡�$sex
		</div>
		<div>
			��̣��$hobby
		</div>
		<div>
			���ȡ�$job
		</div>
		<div>
			�����ʿ���ʪ��$food
		</div>
		<div>
			��å�������$message
		</div>
</body>
</html>
EOF

print $contents;
