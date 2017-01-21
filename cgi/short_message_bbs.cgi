#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use Encode;

#CGI���֥�����������
my $q = CGI -> new;

#ʸ������������
$q -> charset('EUC-JP');

#���������¸�ե�����
my $data_file = "./data_file/bbs_data.txt";

#�Ǽ��Ĥ������ܥ��󤬲����줿���ν���(���������¸)
if ($ENV{REQUEST_METHOD} eq 'POST') {

	#�ե����फ���������줿�ǡ��������
	my $title = $q -> param('title');
	my $message = $q -> param('message');

	#�����ȥ뤬̵�����ϥ��顼�ڡ���ɽ��
	if (!$title) {
		show_error_page($q, "�����ȥ�����Ϥ��Ʋ�����");
	}

	#��å�������̵�����ϥ��顼�ڡ���ɽ��
	if (!$message) {
		show_error_page($q, "��å����������Ϥ��Ʋ�����");
	}

	#ʸ�����perl�������������Ѵ�����
	$title = decode('EUC-JP', $title);
	$message = decode('EUC-JP', $message);

	#�����ȥ��ʸ����������å�
	if (length $title > 30) {
		show_error_page($q, "�����ȥ뤬Ĺ�����ޤ�");
	}

	#��å�������ʸ����������å�
	if (length $message > 100) {
		show_error_page($q, "��å��������ʤ������ޤ�");
	}

	#���դȻ���μ���
	my ($sec, $min, $hour, $day, $month, $year) = localtime;
	$month = $month + 1;
	$year = $year + 1900;

	#���եե����ޥå�(YYYY/mm/dd hh:mm:ss)
	my $datetime = sprintf("%04s/%02s/%02s %02s:%02s:%02s",
				$year, $month, $day, $hour, $min, $sec);

	#�ǡ�������¸���䤹�����˲ù�����
	my $record = join("\t", $datetime, $title, $message)."\n";

	#�ɲý񤭹��ߤǥե����륪���ץ�
	my $data_fh;
	open $data_fh, ">>", $data_file
		or die "Cannot open $data_file: $!";

	#�ե�����˽��Ϥ�������ʸ���������������������
	$record = encode('EUC-JP', $record);

	#�ǡ����񤭹���
	print $data_fh $record;

	close $data_fh;

	#��ʬ����(������ץ�)�˥�����쥯��
	print $q -> redirect($ENV{SCRIPT_NAME});

} else {
	#�ڡ����˥������������ä����ν���(GET�᥽�å�,�������ɽ��)

	#�ǡ����ե����륪���ץ�
	my $data_fh;
	open $data_fh, "<", $data_file
		or die "Cannot open $data_file: $!";

	#�ǡ����ɤ߹���
	my $entry_infos = [];
	while (my $line = <$data_fh>) {
		chomp $line;
		my @items = split /\t/, $line;

		my $entry_info = {};
		$entry_info -> {datetime} = $items[0];
		$entry_info -> {title} = $items[1];
		$entry_info -> {message} = $items[2];

		push @{$entry_infos}, $entry_info;
	}
	close $data_fh;

	#�ǡ����򿷤�������¤��ؤ���
	@{$entry_infos} = reverse @{$entry_infos};

	#ɽ������񤭹������ƺ���
	my $embed_entries;
	foreach my $entry_info (@{$entry_infos}) {
		#HTML����������
		my $datetime = $q -> escapeHTML($entry_info -> {datetime});
		my $title = $q -> escapeHTML($entry_info -> {title});
		my $message = $q -> escapeHTML($entry_info -> {message});

		my $entry = <<"EOS";
<div>
	<hr>
	<div>�����ȥ�: $title ($datetime)</div>
	<div>��å�����</div>
	<div>$message</div>
</div>
EOS

		$embed_entries .= $entry
	}

	my $content = <<"EOS";
<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
	<title>�����å������Ǽ���</title>
	</head>
	<body>
		<h1>�����å������Ǽ���</h1>
		<form method="post" action="short_message_bbs.cgi">
			<div>
			�����ȥ�
			<input type="text" name="title">
			</div>
			<div>
			��å�����
			<textarea name="message" cols="50" rows="10"></textarea>
			</div>
			<div>
			<input type="submit" value="����">
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