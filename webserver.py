from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi

from database_setup import Base, Restaurant, MenuItem

engine = create_engine('postgres:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):


  def do_GET(self):

    try:
      if self.path.endswith("/hello"):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        output = ""
        output += "<html><body>Hello!"
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to day? </h2><input name = 'message' type='text' ><input type='submit' value = 'Submit'> </form>"
        output += "</body></html>"

        self.wfile.write(output)
        print(output)
        return

      if self.path.endswith("/hola"):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        output = ""
        output += "<html><body>&#161Hola!<a href = '/hello'>Back to hello</a>"
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to day? </h2><input name = 'message' type='text' > <input type='submit' value = 'Submit'> </form>"
        output += "</body></html>"
        self.wfile.write(output)
        print(output)
        return

      if self.path.endswith("/restaurants"):
        restaurants = session.query(Restaurant).all()
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        output = ""
        output += "<html><body><h1>Restaurants</h1>"
        output += "<a href = '/restaurants/new'>Create new restaurant</a></br>"
        output += "</br>"

        for restaurant in restaurants:
          output += restaurant.name
          output += "</br>"
          output += "<a href = '/restaurants/" + `restaurant.id` + "/edit'>Edit</a></br>"
          output += "<a href = '/restaurants/" + `restaurant.id` + "/delete'>Delete</a></br></br>"

        output += "</body></html>"
        self.wfile.write(output)
        print(output)
        return

      if self.path.endswith("/restaurants/new"):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        output = ""
        output += "<html><body><h1>Make a new restaurant</h1>"
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>" + \
          "<h2> Name </h2><input name = 'name' type='text' > <input type='submit' value = 'Create'> </form>"
        output += "</body></html>"
        self.wfile.write(output)
        print(output)
        return

      if self.path.endswith("/edit"):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        path = self.path.split("/")
        restaurantId = path[2]

        query = session.query(Restaurant).filter(Restaurant.id == restaurantId)
        restaurant = query.first()

        output = ""
        output += "<html><body><h1>Rename " + restaurant.name + "</h1>"
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + restaurantId + "/edit'>" + \
          "<h2> Name </h2><input name = 'name' type='text' > <input type='submit' value = 'Rename'> </form>"
        output += "</body></html>"
        self.wfile.write(output)
        print(output)
        return

      if self.path.endswith("/delete"):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        path = self.path.split("/")
        restaurantId = path[2]

        query = session.query(Restaurant).filter(Restaurant.id == restaurantId)
        restaurant = query.first()

        output = ""
        output += "<html><body><h1>Delete " + restaurant.name + "</h1>"
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + restaurantId + "/delete'>" + \
          "<input type='submit' value = 'Delete'> </form>"
        output += "</body></html>"
        self.wfile.write(output)
        print(output)
        return

    except IOError:
      self.send_error(404, "File not found %s" % self.path)

  def do_POST(self):
    try:
      print self.path
      if self.path.endswith("/restaurants/new"):

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          restaurantName = fields.get('name')
          restaurant = Restaurant(name=restaurantName[0])

          session.add(restaurant)
          session.commit()

        self.send_response(301)
        self.send_header("Content-type", 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

      if self.path.endswith("/edit"):

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          path = self.path.split("/")
          restaurantId = path[2]
          fields = cgi.parse_multipart(self.rfile, pdict)
          restaurantName = fields.get('name')[0]
          query = session.query(Restaurant).filter(Restaurant.id == restaurantId)
          restaurant = query.first()
          restaurant.name = restaurantName

          # session.addrestaurant)
          session.commit()

        self.send_response(301)
        self.send_header("Content-type", 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

      if self.path.endswith("/delete"):

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          path = self.path.split("/")
          restaurantId = path[2]
          query = session.query(Restaurant).filter(Restaurant.id == restaurantId)
          restaurant = query.first()

          session.delete(restaurant)
          session.commit()

        self.send_response(301)
        self.send_header("Content-type", 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

      if self.path.endswith("/zzz"):
        self.send_response(301)
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('message')

          newName = messagecontent[0]




        self.wfile.write(output)
        print(output)

    except IOError:
      pass

def main():
  try:
    port = 8085
    server = HTTPServer(('', port), webserverHandler)
    print "Web server is runnint n port %s" % port
    server.serve_forever()


  except KeyboardInterrupt:
    print "^C entered, stopping web server..."
    server.socket.close()

if __name__ == "__main__":
  main()