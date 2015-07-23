#!/usr/bin/perl -w
use DBI;
use Net::SSH::Perl;

my %INPUTVARS;
if(!($dbh = DBI->connect('dbi:mysql:test','sarath','sarath',{RaiseError => 0, PrintError => 0}))){
#{RaiseError => 1, PrintError => 0}
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
while(@row = $sth->fetchrow_array)
{
$INPUTVARS{$row[0]}=$row[1];
}

my $ssh;
eval{
$ssh = Net::SSH::Perl->new($INPUTVARS{'HOST'}, debug => 0, protocol => 2);
my $loginStatus = $ssh->login($INPUTVARS{'USERNAME'},$INPUTVARS{'PASSWORD'});
};
if($@){
        if($@=~/^Can't connect to .*/){
        print "Unable to connect to $INPUTVARS{'HOST'}.\n";
        }
        elsif($@=~/^Permission denied.*/){
        print "Invalid username/password.\n";
        }
        else{
        print "Error Occured\n";
        }
        exit 1;
}
my($stdout,$stderr,$exit) = $ssh->cmd("cat /proc/meminfo | grep MemTotal | awk '{print \$2}'");
        if($stderr){
                chomp($stderr);
                print "Error occured : $stderr\n";
                exit;
        }
chomp($stdout);
$stdout=$stdout/1024;
print "Ram : $stdout\n";
($stdout,$stderr,$exit) = $ssh->cmd("echo $INPUTVARS{'PASSWORD'} | sudo -S  /etc/init.d/$INPUTVARS{'SERVICE'} status");
if($stderr){
        if($stderr!~/^\[sudo] password for/){
        chomp($stderr);
        print "Error occured : $stderr\n";
        exit;
        }
}
if($stdout=~/not running$/){
        print "Service : '$INPUTVARS{'SERVICE'}' not running\n";
}
else{
        print "Service : '$INPUTVARS{'SERVICE'}' running\n";
}
