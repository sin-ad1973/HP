#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use Encode;
use lib '~/perl5/lib/perl5/';
use HTML::Template;

#CGI���֥�����������
my $q = CGI -> new;

$q -> charset('EUC-JP');

#HTML::Template���֥�����������
my $tmpl = HTML::Template -> new(filename => './tmpl/sample.tmpl');

#�ǡ���������
$tmpl -> param(message => '����ˤ���');

#�����߸��HTML����
print $q -> header;
print $tmpl -> output;
