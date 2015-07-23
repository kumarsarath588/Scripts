#!/usr/bin/perl -w
use DBI;
if(!($dbh = DBI->connect('dbi:mysql:test;host=192.168.0.214','sarath','pass,123',{RaiseError => 1, PrintError => 0}))){
	print "Connection failed\n";
        exit;
}
$sql = "select * from CMDB;";
if (!($sth=$dbh->prepare($sql))){
	print "Preparation of query failed\n";
        exit;
}
if(!$sth->execute)
{
	print "Execution of query failed : $DBI::errstr\n";
	exit;
}
my $fields = $sth->{NAME};
foreach(@$fields){
print "$_\t\t";
}
print "\n";
while (@row = $sth->fetchrow_array) 
{
	for($i=0;$i<=$#row;$i++){
	#print "$$fields[$i]\n";
	print "$row[$i]\t\t";
	}
	print "\n";
}
