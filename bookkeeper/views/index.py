from flask.ext.admin import AdminIndexView

from ..auth import AuthOverride


class IndexView(AuthOverride, AdminIndexView):
    pass
