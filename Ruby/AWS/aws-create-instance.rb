require 'rubygems'
require 'json'

amis=JSON.parse(File.read('amis.json'))


os='ubuntu-14.04'
count=1
instance_type='t2.micro'
keyname='sarath'
sg='default'
tag='Sarath-Ubuntu-test'

#def create(instance)
  create_instance=(`aws ec2 run-instances  --image-id #{amis["regions"]["us-west-2"]["#{os}"]} --count #{count} --instance-type #{instance_type} --key-name #{keyname} --security-groups #{sg} --query 'Instances[0].InstanceId'`).chomp.gsub('"','')

while (`aws ec2 describe-instances --instance-ids #{create_instance} --query 'Reservations[0].Instances[0].State.Name'`).chomp.gsub('"','') == "pending"
   puts 'pending...'
end


`aws ec2 create-tags --resources #{create_instance} --tags Key=Name,Value=#{tag}`

describe_instance=`aws ec2 describe-instances --instance-ids #{create_instance}`
json_description = JSON.parse(describe_instance)

public_ipaddress = json_description["Reservations"][0]["Instances"][0]["PublicIpAddress"]
private_ipaddress = json_description["Reservations"][0]["Instances"][0]["PrivateIpAddress"]

puts "The machine you are connecting public ip is: #{public_ipaddress} and private ip is: #{private_ipaddress}"

