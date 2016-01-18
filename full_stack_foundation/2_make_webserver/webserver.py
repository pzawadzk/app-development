from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>New restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Type in new restaurant</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                items = session.query(Restaurant).all()
                output = ""
                output += "<a href=/restaurants/new>Add new restaurant</br></a>"
                output += "<html><body>"
                for item in items:
                    output += "%s</br>"% item.name
                    output += "<a href=%d/edit>edit</br></a>"%item.id
                    output += "<a href=%d/delete>delete</br></a>"%item.id
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("edit"):
                id = int(self.path.split('/')[1])
                print id
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit restaurant name</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='%d/edit'><h2>Type in new for %s restaurant</h2><input name="new_name" type="text" ><input type="submit" value="Submit"> </form>''' %(id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("delete"):
                id = int(self.path.split('/')[1])
                print id
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Delete restaurant name</h1>"
                output += '''<form action="" method="post">
                    <button name="delete" value="delete">Delete</button> </form>''' 
                #<form method='POST' enctype='multipart/form-data' action='%d/delete'><h2>Delete %s restaurant</h2> <button type="button">Delete</button> </form>
                #%(id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
            if self.path.endswith("restaurants/new"):
                messagecontent = fields.get('message')
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("edit"):
                id = int(self.path.split('/')[1])
                messagecontent = fields.get('new_name')
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                restaurant.name = messagecontent[0]
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("delete"):
                id = int(self.path.split('/')[1])

                session.query(Restaurant).filter_by(id=id).delete()
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except:
            pass


def main():
    try:
        port = 8081
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
