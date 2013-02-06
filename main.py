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

import os
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
import tornado.options

import sys
sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
loader = tornado.template.Loader(template_dir)
render = lambda handler, name, values: loader.load(name).generate(static_url=handler.static_url, **values)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'home.html', {}))


class GithubButtonHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'github-btn.html', {}))

from events import get_events


class GitHubStream(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'github_stream.html', {'events': get_events()}))

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}


application = tornado.web.Application([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/", MainHandler),
    (r"/github", GitHubStream),
    (r"/github-btn", GithubButtonHandler)
], **settings)

if __name__ == "__main__":
    application.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()
