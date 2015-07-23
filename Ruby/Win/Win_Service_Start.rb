require 'json'
require 'winrm'
require 'optparse'

opts = OptionParser.new
opts.on("-s Service Name", "--service Service Name", String, "Service Name") { |v| $ServiceName = v }
opts.on("-h", "--help", "Help") { |v| puts opts ; exit}
begin
  opts.parse!(ARGV)
rescue OptionParser::ParseError => e
  puts e
end
raise OptionParser::MissingArgument, "Service Name [-s]" if $ServiceName.nil?

#$ServiceName = 'RemoteAccess'

PS_SCRIPT = <<-PS_SCRIPT
$result = @{
  "service"     =  \$(Get-Service -Name #{$ServiceName} -ServicesDependedOn).Name
}
$result | ConvertTo-JSON
PS_SCRIPT

url_params = {
  :ipaddress => "192.168.0.39",
  :port      => 5985                # Default port 5985
}

connect_params = {
  :user         => "administrator",    # Example: domain\\user
  :pass         => "Pass@word1",
  :disable_sspi => true
}

url = "http://#{url_params[:ipaddress]}:#{url_params[:port]}/wsman"
#$evm.log("info", "Connecting to WinRM on URL :#{url}")

winrm   = WinRM::WinRMWebService.new(url, :ssl, connect_params)
get_deps = winrm.run_powershell_script(PS_SCRIPT)
errors = get_deps[:data].collect { |d| d[:stderr] }.join
$evm.log("error", "WinRM returned stderr: #{errors}") unless errors.blank?
data = get_deps[:data].collect { |d| d[:stdout] }.join
json_hash = JSON.parse(data, :symbolize_names => true)

$startmode_cmd = "Get-WmiObject win32_service -Filter \"Name=\'#{$ServiceName}\'\" | select startmode -ExpandProperty startmode"
get_startmode= winrm.run_powershell_script($startmode_cmd)
errors = get_startmode[:data].collect { |d| d[:stderr] }.join
puts errors unless errors.blank?
startmode = get_startmode[:data].collect { |d| d[:stdout] }.join

if startmode.chomp == "Disabled"
   puts "Service #{$ServiceName} is Disabled, Enabling...."
   $set_service_startmode = "Set-Service #{$ServiceName} -startuptype 'manual'"
   set_service_startmode=winrm.run_powershell_script($set_service_startmode)
   errors = set_service_startmode[:data].collect { |d| d[:stderr] }.join
   puts errors unless errors.blank?
end

unless (json_hash[:service]).nil?
  puts "Starting Dependent services #{json_hash[:service]}"
  json_hash[:service].each do |hash|
    $cmd ="Start-Service -name #{hash}"
    results = winrm.run_powershell_script($cmd)
    errors = results[:data].collect { |d| d[:stderr] }.join
    puts errors unless errors.blank?
    #$evm.log("error", "WinRM returned stderr: #{errors}") unless errors.blank?
  end
end
$cmd ="Start-Service -name #{$ServiceName}"
results = winrm.run_powershell_script($cmd)
errors = results[:data].collect { |d| d[:stderr] }.join
puts errors unless errors.blank?


#$evm.log("info", "WinRM returned hash: #{json_hash.inspect}")
