require 'rubygems'
require 'json'
require 'optparse'

opts = OptionParser.new
opts.on("-H Hostname", "--host Hostname", String, "HostName") { |v| $Host = v }
opts.on("-o Operating System", "--os Operating System", String, "Operating System") { |v| $os = v }
opts.on("-c Count", "--count Count", String, "Count") { |v| $count = v }
opts.on("-k ", "--keyname Key Name", String, "Key Name") { |v| $keyname = v }
opts.on("-s ", "--sg Secutiry Group", String, "Secutiry Group") { |v| $sg = v }
opts.on("-h", "--help", "Help") { |v| puts opts ; exit}

begin
  opts.parse!(ARGV)
rescue OptionParser::ParseError => e
  puts e
end
raise OptionParser::MissingArgument, "Hostname [-H]" if $Host.nil?
raise OptionParser::MissingArgument, "Operating System [-o]" if $os.nil?
raise OptionParser::MissingArgument, "Count [-c]" if $count.nil?
raise OptionParser::MissingArgument, "Keyname [-k]" if $keyname.nil?
raise OptionParser::MissingArgument, "Security Group [-s]" if $sg.nil?

if (!defined?(ENV['AwS_REGION']))
  puts "Error: please enter Environment variable AWS_REGION"
  exit
end

instance_type='t2.micro'
# -*- Read the amis file containing aws ami's and parse the json
begin
  amis=JSON.parse(File.read('amis.json'))
  instance="#{amis["regions"]["us-west-2"][$os]}"
rescue  
  puts "Error: Not able to read amis file"
  exit
end
# -*- Create the aws instance
begin
  create_instance=(`aws ec2 run-instances  --image-id #{instance} --count #{$count} --instance-type #{instance_type} --key-name #{$keyname} --security-groups #{$sg} --query 'Instances[0].InstanceId'`).chomp.gsub('"','')
rescue
  puts "Error: Unable to create instance"
  exit
end

while (`aws ec2 describe-instances --instance-ids #{create_instance} --query 'Reservations[0].Instances[0].State.Name'`).chomp.gsub('"','') == "pending"
   puts 'pending...'
end

begin
`aws ec2 create-tags --resources #{create_instance} --tags Key=Name,Value=#{$Host}`
rescue  
  puts "Error: Not able to add tag"
  exit
end

describe_instance=`aws ec2 describe-instances --instance-ids #{create_instance}`
json_description = JSON.parse(describe_instance)
public_ipaddress = json_description["Reservations"][0]["Instances"][0]["PublicIpAddress"]
private_ipaddress = json_description["Reservations"][0]["Instances"][0]["PrivateIpAddress"]
puts "The machine #{instance} created sucssfully.
public ip is: 	#{public_ipaddress} 
private ip is: #{private_ipaddress}"

