#!/usr/bin/perl

use strict;
use warnings;
use DBI;

print "Content-type: text/html;charset=EUC-JP\n";
print "\n";

print "<html>\n";
print "<head>\n";
print "<title>CGI-DB��³�ƥ���</title>\n";
print "</head>\n";
print "<body>\n";
print "CGI-DB��³�ƥ���<br><br>\n";


my $user = 'sin-ad1973';
my $passwd = 'c3993955';
my $db = DBI->connect('DBI:mysql:sin-ad1973_test:mysql451.db.sakura.ne.jp', $user, $passwd) || CgiError("connect",$DBI::errstr);

print "��³���������ޤ���<BR>\n";

my $sth = $db->prepare("select * from test");

$sth->execute or die "��������:$DBI::errstr\n";


my $num_rows = $sth->rows;
print "���� $num_rows ��<BR>\n";
for (my $i=0; $i<$num_rows; $i++) {
	my @a = $sth->fetchrow_array;
	print "id=$a[0], name=$a[1] <BR>\n";
}

print "��������<BR>\n";

$sth->finish;
$db->disconnect;

print "</body>\n";
print "</html>\n";