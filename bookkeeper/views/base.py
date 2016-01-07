import os

from flask.helpers import get_root_path


class ViewMixin:
    def create_blueprint(self, admin):
        ret = super().create_blueprint(admin)
        root_path = os.path.abspath(os.path.join(
            get_root_path(__name__), os.pardir))
        ret.jinja_loader.searchpath.insert(
            0, os.path.join(root_path, 'templates'))
        ret.static_folder = os.path.join(root_path, 'static')
        return ret
