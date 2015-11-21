use Rack::Static, :urls => [""], :root => 'app', :index => 'index.html'

run lambda { |env| [200, {'Content-Type' => 'text/plain'}, ['OK']] }