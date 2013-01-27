#!/usr/bin/env python

# Copyright (C) 2013  Galaxy Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tornado
import tornado.ioloop
import tornado.web
import tornado.template

loader = tornado.template.Loader(
    os.path.join(os.getcwd(), 'templates'))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader.load("test.html").generate(myvalue="XXX")
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()
