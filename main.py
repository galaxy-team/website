#!/usr/bin/env python

# Copyright (C) 2013 Galaxy Team

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

# setup the connection to the database before anything else
import os

# os.environ['NEW_RELIC_LICENSE_KEY'] = '12b902d9b0341674b9965e99319ce90eecbdbf89'

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

import sys
import tornado
import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.options
import tornado.template
import tornado.httpserver

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(template_name='home.html')


class GithubButtonHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('github-btn.html')


class GitHubStream(tornado.web.RequestHandler):
    def get(self):
        self.render('github_stream.html')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
    "template_path": os.path.join(os.path.dirname(__file__), 'templates')
}


application = tornado.wsgi.WSGIApplication([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/", MainHandler),
    (r"/github", GitHubStream),
    (r"/github-btn", GithubButtonHandler),
], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(application))
    http_server.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
