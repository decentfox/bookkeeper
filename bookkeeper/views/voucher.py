from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.fields import InlineModelFormList
from flask.ext.admin.contrib.sqla.form import InlineModelConverter
from flask.ext.admin.form import RenderTemplateWidget
from flask.ext.admin.model.fields import InlineModelFormField
from flask.ext.admin.model.widgets import InlineFormWidget

from . import base
from .. import models


class InlineRecordFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super().__init__('inline_record_list.html')


class InlineRecordFormWidget(InlineFormWidget):
    def __init__(self):
        RenderTemplateWidget.__init__(self, 'inline_record_form.html')


class InlineRecordFormField(InlineModelFormField):
    widget = InlineRecordFormWidget()


class InlineRecordFormList(InlineModelFormList):
    widget = InlineRecordFieldListWidget()
    form_field_type = InlineRecordFormField


class InlineRecordConverter(InlineModelConverter):
    inline_field_list_type = InlineRecordFormList


class VoucherView(base.ViewMixin, ModelView):
    create_template = 'voucher_create.html'
    inline_model_form_converter = InlineRecordConverter
    inline_models = [
        (models.Record, dict(form_columns=[
            'id',
            'summary',
            'direction',
            'amount',
            'account',
        ]))
    ]
