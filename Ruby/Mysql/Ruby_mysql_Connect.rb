#!/usr/bin/ruby

require 'mysql'
require 'optparse'

opts = OptionParser.new
opts.on("-H Hostname", "--host Hostname", String, "Hostname") { |v| $Host = v }
opts.on("-u Username", "--user Username", String, "Username") { |v| $User = v }
opts.on("-p Password", "--password Password", String, "Password") { |v| $Password = v }
opts.on("-d Database Name", "--database Database Name", String, "Database Name") { |v| $Database = v }
opts.on("-h", "--help", "Help") { |v| puts opts ; exit}

begin
  opts.parse!(ARGV)
rescue OptionParser::ParseError => e
  puts e
end
raise OptionParser::MissingArgument, "Hostname [-H]" if $Host.nil?
raise OptionParser::MissingArgument, "Username [-u]" if $User.nil?
raise OptionParser::MissingArgument, "Password [-p]" if $Password.nil?
raise OptionParser::MissingArgument, "Database [-d]" if $Database.nil?

begin
    con = Mysql.new($Host,$User,$Password,$Database)
    puts "Version of Server is: #{con.get_server_info}"
    con.list_dbs.each do |db|
       puts db
    end
    #query=con.prepare "insert into CMDB values (?,?,?)"
    #query.execute "123456", "kumar", "kumar@test.com"
    results=con.query "select * from CMDB"
    results.each do |rs|
	puts rs.join("\s")
    end
     
rescue Mysql::Error => e
    puts e.errno
    puts e.error
ensure
    con.close if con
end
