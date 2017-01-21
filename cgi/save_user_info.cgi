#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Session;

my $q = CGI -> new;
$q -> charset('EUC-JP');

#�桼����������Ǽ����ե��������¸����ǥ��쥯�ȥ�
my $user_data_dir = "user_data";

#���å������饻�å����ID����
my $id = $q -> cookie('id');

#���å��������Τ���Υ⥸�塼�� CGI::Session ���֥�����������
#�ǽ��ˬ��ξ��ϥ��å����ID�����������
#2���ܰʹߤ�ˬ��ξ��ϥ��å�����������������å����ID����Ѥ���
my $session = CGI::Session -> new("driver:File", $id, {Directory => $user_data_dir});

#���å����ID����
$id = $session -> id;

#�桼������ˬ��������Ф�
my $visit_cnt = $session -> param('visit_cnt');

#ˬ������û�
$visit_cnt++;

#�桼������ˬ�����򥻥å����˳�Ǽ
$session -> param('visit_cnt', $visit_cnt);

#���å����κ���(���å����ID���Ǽ)
my $cookie = $q -> cookie(-name => 'id', -value => $id);

my $content = <<"EOS";
<html>
	<head>
		<meta-equiv="Content-Type" content="text/html;charset=EUC-JP">
		<title>���å��������ȥ��å���</title>
	</head>
	<body>
		ˬ������$visit_cnt
	</body>
</html>
EOS

#�إå��˥��å��������ꤷ�ƽ���
print $q -> header(-cookie => $cookie);
print $content;

