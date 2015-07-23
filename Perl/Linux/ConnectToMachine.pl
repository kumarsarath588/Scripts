#!/usr/bin/perl -w
use strict;
use Net::SSH::Perl;

my $sshusername = "sarath";
my $sshpasswd = "pass,123";
my $host = "192.168.11.68";
my $service = "cups";
my $ssh;
eval{
$ssh = Net::SSH::Perl->new($host, debug => 0, protocol => 2);
my $loginStatus = $ssh->login($sshusername,$sshpasswd);
};
if($@){
	if($@=~/^Can't connect to .*/){
	print "Unable to connect to $host.\n";
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
($stdout,$stderr,$exit) = $ssh->cmd("echo $sshpasswd | sudo -S  /etc/init.d/$service status");
if($stderr){
	if($stderr!~/^\[sudo] password for/){
        chomp($stderr);
        print "Error occured : $stderr\n";
        exit;
	}
}
if($stdout=~/not running$/){
	print "Service : '$service' not running\n";
}
else{
	print "Service : '$service' running\n";
}
exit;
my @Status=split("\n",$stdout);
foreach(@Status){
	print ":$_:\n";
}
