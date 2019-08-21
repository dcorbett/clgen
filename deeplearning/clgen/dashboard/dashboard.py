"""A flask server which renders test results."""
import flask
import portpicker
import threading

import build_info
from labm8 import app
from labm8 import bazelutil

FLAGS = app.FLAGS

app.DEFINE_integer('clgen_dashboard_port', portpicker.pick_unused_port(),
                   'The port to launch the server on.')

flask_app = flask.Flask(
    __name__,
    template_folder=bazelutil.DataPath(
        'phd/deeplearning/clgen/dashboard/templates'),
    static_folder=bazelutil.DataPath('phd/deeplearning/clgen/dashboard/static'),
)


@flask_app.route("/")
def index():
  app.Log(1, 'Rendering index')
  urls = {
      "cache_tag": build_info.BuildTimestamp(),
      "styles_css": flask.url_for('static', filename='bootstrap.css'),
      "site_js": flask.url_for('static', filename='site.js'),
  }
  return flask.render_template(
      "dashboard.html",
      urls=urls,
      build_info=build_info.FormatShortBuildDescription(html=True))


def Launch():
  """Launch dashboard in a separate thread."""
  threading.Thread(
      target=flask_app.run,
      kwargs={
          'port': FLAGS.clgen_dashboard_port,
          'debug':
          False,  # Debugging must be disabled when run in a separate thread.
          'host': '0.0.0.0',
      })