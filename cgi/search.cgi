#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use Encode;
use Scalar::Util qw(looks_like_number);
use URI;

#CGI���֥�����������
my $q = CGI -> new;

#ʸ�������ɤ�����
$q -> charset("EUC-JP");

#������¸�ե�����
my $data_file = "./data_file/person_data.txt";

#�ѥ���������
my $path_info = $q -> path_info;

#���Ϥ���HTML
my $content;


if ($path_info eq '/resist') {
	#��Ͽ����ɽ��
	$content = create_resist_content($q);

} elsif ($path_info eq '/post') {
	#��Ͽ����
	post_entry($q, $data_file);

	#�������̤˥�����쥯��
	print $q -> redirect($q -> script_name);
	exit;

} elsif ($path_info eq '/error') {
	#���顼����ɽ��
	$content = create_error_content($q);

} elsif ($path_info eq '/search-result') {
	#������̲���ɽ��
	$content = create_search_result_content($q, $data_file);

} else {
	#��������ɽ��
	$content = create_search_content($q);

}

#HTML����
print $q -> header;
print $content;



#��Ͽ����ɽ�� ����
sub create_resist_content {

	#�ѥ�᡼������
	my $q = shift;

	#��Ͽ����URL����
	my $post_url = $q -> script_name . '/post';

	#��������URL����
	my $search_page_url = $q -> script_name . '/search';

	#��Ͽ����HTML
	my $content=<<"EOS";
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>�ʰ׸��������ƥ�</title>
	</head>
	<body>
		<h1>�ʰ׸��������ƥ�</h1>
		<form method="post" action="$post_url">
			<div>
			�������Ͽ���ޤ�
			</div>
			<div>
			��̾
			<input type="text" name="name">
			</dif>
			<div>
			��Ĺ
			<input type="text" name="height">
			</div>
			<div>
			<input type="submit" value="��Ͽ">
			</div>
		</form>
		<div>
			<a href="$search_page_url">�������̤�</a>
		</div>
	</body>
</html>
EOS
	return $content;
}


#��Ͽ����
sub post_entry {

	#�ѥ�᡼������
	my ($q, $data_fle) = @_;

	#��̾(�ǥ�����)
	my $name = decode('EUC-JP', $q -> param('name'));

	#��̾���ϥ����å�
	if (!$name) {
		#���顼�ڡ����˥�����쥯��
		my $error = "��̾�����Ϥ��Ʋ�������";
		redirect_error_page($error);
	}

	#��Ĺ(�ǥ�����)
	my $height = decode('EUC-JP', $q -> param('height'));

	#��Ĺ ���ͥ����å�
	if (!looks_like_number($height)) {
		#���顼�ڡ����˥�����쥯��
		my $error = "��Ĺ�Ͽ��ͤ����Ϥ��Ʋ�������";
		redirect_error_page($error);
	}

	#�ե����륪���ץ�
	open my $fh, ">>", $data_file
		or die "Cannot open $data_file: $!";

	#���������󥳡���
	$name = encode('EUC-JP', $name);
	$height = encode('EUC-JP', $height);

	#���ϹԺ���
	my $line = join("\t", $name, $height) . "\n";

	#�ե��������
	print $fh $line;

	#�ե����륯����
	close $fh;

	#�����ڡ����˥�����쥯��
	print $q -> redirect($q -> script_name);
}


#��������ɽ�� ����
sub create_search_content {

	#�ѥ�᡼������
	my $q = shift;

	#������̲���URL����
	my $search_result_url = $q -> script_name . '/search-result';

	#��Ͽ����URL����
	my $resist_page_url = $q -> script_name . '/resist';

	#��������HTML
	my $content=<<"EOS";
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>�ʰ׸��������ƥ� ��������</title>
	</head>
	<body>
		<h1>�ʰ׸��������ƥ� ��������</h1>
		<form method="get" action="$search_result_url">
			<div>
			����򸡺����ޤ�
			</div>
			<div>
			��Ĺ
			<input type="text" name="height-min">��
			<input type="text" name="height-max">
			</div>
			<div>
			<input type="submit" value="����">
			</div>
		</form>
		<div>
		<a href="$resist_page_url">��Ͽ���̤�</a>
		</div>
	</body>
</html>
EOS
	return $content;
}


#�������� �ڤ� ������̲���ɽ�� ����
sub create_search_result_content {

	#�ѥ�᡼������
	my ($q, $data_file) = @_;

	#����������(�ǥ�����)
	my $height_min = decode("EUC-JP", $q -> param('height-min'));
	my $height_max = decode("EUC-JP", $q -> param('height-max'));

	#��Ĺ���ͥ����å�
	if (!looks_like_number($height_min) || !looks_like_number($height_max)) {
		#���顼�ڡ����˥�����쥯��
		my $error = "��Ĺ���ϰϤ���ͤ����Ϥ��Ʋ�������";
		redirect_error_page($error);
	}

	#�ե����륪���ץ�
	open my $fh, "<", $data_file
		or die "Cannot open $data_file: $!";

	#�����˥ޥå������ǡ��������
	my $match_persons = [];
	while (my $line = <$fh>) {

		#���Ժ��
		chomp $line;

		#��ʬ��
		my @items = split("\t", $line);

		#��ʪ����ϥå���(��ե����)
		my $person = {};
		$person -> {name} = $items[0];
		$person -> {height} = $items[1];

		#���˥ޥå����������ɲ�
		if ($person -> {height} >= $height_min && 
			$person -> {height} <= $height_max) {

			push @{$match_persons}, $person;
		}
	}

	#�������HTML����(�쥳������)
	my $embed_entries;
	foreach my $person (@{$match_persons}) {

		my $name = $q -> escapeHTML($person -> {name});
		my $height = $q -> escapeHTML($person -> {height});

		my $entry=<<"EOS";
<div>
	<hr>
	<div>��̾: $name</div>
	<div>��Ĺ: $height</div>
</div>
EOS
		$embed_entries .= $entry;

	}

	#��������URL����
	my $search_page_url = $q -> script_name . '/search';

	#��Ͽ����URL����
	my $resist_page_url = $q -> script_name . '/resist';

	#�������HTML����
	my $content=<<"EOS";
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>�ʰ׸��������ƥ� �������</title>
	</head>
	<body>
		<h1>�ʰ׸��������ƥ� �������</h1>
		<div>
			<a href="$search_page_url">�������̤�</a>
			<a href="$resist_page_url">��Ͽ���̤�</a>
		</div>
		<div>
			$embed_entries
		</div>
	</body>
</html>
EOS
	#�ե����륯����
	close $fh;

	return $content;
}

#���顼���̥�����쥯�� ����
sub redirect_error_page {

	#�ѥ�᡼������
	my $error_message = shift;

	#���顼���̤�ɽ������ڡ�����URL����
	my $error_page_url = URI -> new($q -> script_name . '/error');

	#���顼��å������򥯥���ʸ���������
	$error_page_url -> query_form({error => $error_message});

	#URL��ʸ������Ѵ�
	my $error_page_url_as_string = $error_page_url -> as_string;

	#������쥯��
	print $q -> redirect($error_page_url_as_string);
	exit;
}

#���顼����ɽ�� ����
sub create_error_content {

	#�ѥ�᡼������
	my $q = shift;
	my $error = $q -> param('error');

	#���顼����HTML
	my $content=<<"EOS";
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>�ʰ׸��������ƥ� ���顼����</title>
	</head>
	<body>
		$error
	</body>
</html>
EOS
	return $content;
}
