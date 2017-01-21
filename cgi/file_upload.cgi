#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use File::Copy;

#���åץ��ɤξ�¤�3MB������
$CGI::POST_MAX = 3 * 1024 * 1024;

#CGI���֥�����������
my $q = CGI -> new;

#ʸ������������
$q -> charset('EUC-JP');

#�����ե�������¸�ǥ��쥯�ȥ�
my $image_dir = $ENV{DOCUMENT_ROOT} . '/' . 'image';

#�Ǽ��Ĥ������ܥ��󤬲����줿���ν���(�����ե�������¸)
if ($ENV{REQUEST_METHOD} eq 'POST') {

	#CGI���顼�����å�
	my $cgi_error = $q -> cgi_error;
	if ($cgi_error) {
		if ($cgi_error =~ /413/) {
			show_error_page($q, "�ե����륵�������礭�����ޤ���");
		} else {
			show_error_page($q, "���顼��ȯ�����ޤ�����");
		}
	}

	#���åץ��ɤ��줿�����ե�����Υϥ�ɥ����
	my $fh = $q -> upload('image');

	#�ե����뤬���ꤵ��Ƥ��ʤ���票�顼�ڡ���ɽ��
	if (!$fh) {
		show_error_page($q, "�ե��������ꤷ�Ʋ�������");
	}

	#�ե�����μ��ब�����ե�����Ǥ��뤳�Ȥ�����å�����
	my $content_type = $q -> uploadInfo($fh) -> {'Content-Type'};

	my $is_image;
	if ($content_type eq 'image/gif' ||
		$content_type eq 'image/pjpeg' ||
		$content_type eq 'image/jpeg' ||
		$content_type eq 'image/jpg' ||
		$content_type eq 'image/png') {

		$is_image = 1;
	}

	if (!$is_image) {
		show_error_page($q, "�ե���������������Ǥ���($content_type)");
	}

	#���åץ��ɤ��줿�ե�����̾����ʣ���ʤ��褦��̾�������

	#���դȻ���μ���
	my ($sec, $min, $hour, $day, $month, $year) = localtime;
	$month = $month + 1;
	$year = $year + 1900;

	#0��99999�Υ�����ʿ��������
	my $rand_num = int(rand 100000);

	#���դȥ�����ʿ�������ե�����̾�����
	#image-yyyymmddhhmmss-���������
	my $file = sprintf("image-%04s%02s%02s%02s%02s%02s-%05s",
		$year, $month, $day, $hour, $min, $sec, $rand_num);

	#�ե�����̾������¸�ߤ�����ϥե�����̾�������
	while (-f "$image_dir/$file") {
		$rand_num = int(rand 100000);
		my $file = sprintf("image-%04s%02s%02s%02s%02s%02s-%05s",
			$year, $month, $day, $hour, $min, $sec, $rand_num);
	}

	#�����ե�������¸
	copy($fh, "$image_dir/$file")
		or die "Cannot copy: $!";

	#��ʬ����(������ץ�)�˥�����쥯��
	print $q -> redirect($ENV{SCRIPT_NAME});

} else {
	#�ڡ����˥������������ä����ν���(GET�᥽�å�,�������ɽ��)

	#�����ե�����Υǥ��쥯�ȥ꤫��ե�����̾�����
	my $dh;
	opendir $dh, $image_dir
		or die "Cannot open $image_dir: $!";

	my @files;
	while (my $file = readdir $dh) {
		#�����ȥǥ��쥯�ȥ�ȿƥǥ��쥯�ȥ�ʳ��Υե�����̾����
		if ($file ne '.' && $file ne '..') {
			push @files, $file;
		}
	}

	closedir $dh;

	#�����ե�����򿷤�������¤��ؤ���
	@files = sort {$b cmp $a} @files;

	#������ɽ������HTML����
	my $embed_entries;
	foreach my $file (@files) {
		my $entry = <<"EOS";
<div>
	<hr>
	<div>����: $file</div>
	<div>
		<img src = "/image/$file">
	</div>
</div>
EOS

		$embed_entries .= $entry
	}

	my $content = <<"EOS";
<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
	<title>�����Ǽ���</title>
	</head>
	<body>
		<h1>�����Ǽ���</h1>
		<form method="post" action="file_upload.cgi" enctype="multipart/form-data">
			<div>
			�ե�����̾
			<input type="file" name="image">
			<input type="submit" value="�ե����륢�åץ���">
			</div>
		</form>
		<div>
			$embed_entries
		</div>
	</body>
</html>
EOS

	print $q -> header;
	print $content;
}

#���顼��å�����ɽ���ѥ��֥롼����
sub show_error_page {
	my ($q, $err_message) = @_;

	my $content = <<"EOS";
<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
	<title>���顼</title>
	<body>
		$err_message
	</body>
</html>
EOS

	print $q -> header;
	print $content;
	exit;
}