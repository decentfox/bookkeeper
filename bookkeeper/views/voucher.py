from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.fields import InlineModelFormList
from flask.ext.admin.contrib.sqla.form import InlineModelConverter
from flask.ext.admin.form import RenderTemplateWidget, BaseForm
from flask.ext.admin.model.fields import InlineModelFormField
from flask.ext.admin.model.widgets import InlineFormWidget
from flask.ext.login import current_user
from wtforms import HiddenField

from .. import models
from ..auth import AuthOverride


class InlineRecordFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super().__init__('inline_record_list.html')


class InlineRecordFormWidget(InlineFormWidget):
    def __init__(self):
        RenderTemplateWidget.__init__(self, 'inline_record_form.html')

    def __call__(self, field, **kwargs):
        kwargs['models'] = models
        return super().__call__(field, **kwargs)


class InlineRecordFormField(InlineModelFormField):
    widget = InlineRecordFormWidget()


class InlineRecordFormList(InlineModelFormList):
    widget = InlineRecordFieldListWidget()
    form_field_type = InlineRecordFormField

    def __init__(self, form, session, model, prop, inline_view, **kwargs):
        super().__init__(form, session, model, prop, inline_view, **kwargs)


class InlineRecordConverter(InlineModelConverter):
    inline_field_list_type = InlineRecordFormList


class DirectionField(HiddenField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = models.Direction(int(valuelist[0]))
        else:
            self.data = None

    def _value(self):
        return self.data.value


class VoucherForm(BaseForm):
    def populate_obj(self, obj):
        if not obj.creator:
            obj.creator = models.User.query.first()
        super().populate_obj(obj)


# noinspection PyAbstractClass
class VoucherView(AuthOverride, ModelView):
    create_template = 'voucher_create.html'
    edit_template = 'voucher_edit.html'
    form_columns = [
        'index',
        'date',
        'records',
    ]
    form_base_class = VoucherForm
    form_args = dict(
        # date=dict(format='%Y 年 %m 月 %d 日')
    )
    form_widget_args = dict(
        # date={
        #     'data-date-format': 'YYYY 年 MM 月 DD 日',
        # }
    )
    inline_model_form_converter = InlineRecordConverter
    inline_models = [
        (models.Record, dict(
            form_columns=[
                'id',
                'summary',
                'direction',
                'amount',
                'account',
            ],
            form_args=dict(
                account=dict(
                    allow_blank=True,
                ),
            ),
            form_overrides=dict(
                direction=DirectionField,
                amount=HiddenField,
            ),
            form_widget_args=dict(
                direction={'class': 'direction'},
                amount={'class': 'amount'},
            ),
        ))
    ]

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.creator = current_user
            model.company = current_user.current_company
            model.period = current_user.current_period

    def render(self, template, **kwargs):
        kwargs['models'] = models
        return super().render(template, **kwargs)
