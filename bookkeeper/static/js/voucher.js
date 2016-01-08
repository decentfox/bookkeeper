(function () {
    faForm.addInlineField = function (el, elID) {
        // Get current inline field
        var $el = $(el).closest('tr');
        // Figure out new field ID
        var id = elID;

        var maxId = 0;

        $('.record').each(function (idx, field) {
            var $field = $(field);

            var parts = $field.attr('id').split('-');
            idx = parseInt(parts[parts.length - 1], 10) + 1;

            if (idx > maxId) {
                maxId = idx;
            }
        });

        var prefix = id + '-' + maxId;

        // Get template
        var $template = $($('#records-template').find('> td').text());

        // Set form ID
        $template.attr('id', prefix);

        // Fix form IDs
        $('[name]', $template).each(function (e) {
            var me = $(this);

            var id = me.attr('id');
            var name = me.attr('name');

            id = prefix + (id !== '' ? '-' + id : '');
            name = prefix + (name !== '' ? '-' + name : '');

            me.attr('id', id);
            me.attr('name', name);
        });

        $template.insertBefore($el);

        // Select first field
        $('input:first', $template).focus();

        // Apply styles
        faForm.applyGlobalStyles($template);
    };

    faForm.deleteField = function (el, hasID) {
        if ($('.record').size() == 2) return;
        if (hasID) {
        } else {
            $(el).closest('.record').remove();
        }
    };

    var digitUppercase = function (n) {
        var fraction = ['角', '分'];
        var digit = [
            '零', '壹', '贰', '叁', '肆',
            '伍', '陆', '柒', '捌', '玖'
        ];
        var unit = [
            ['元', '万', '亿'],
            ['', '拾', '佰', '仟']
        ];
        var head = n < 0 ? '欠' : '';
        n = Math.abs(n);
        var s = '';
        for (var i = 0; i < fraction.length; i++) {
            s += (digit[Math.floor(n * 10 * Math.pow(10, i)) % 10] + fraction[i]).replace(/零./, '');
        }
        s = s || '整';
        n = Math.floor(n);
        for (var i = 0; i < unit[0].length && n > 0; i++) {
            var p = '';
            for (var j = 0; j < unit[1].length && n > 0; j++) {
                p = digit[n % 10] + unit[1][j] + p;
                n = Math.floor(n / 10);
            }
            s = p.replace(/(零.)*零$/, '').replace(/^$/, '零') + unit[0][i] + s;
        }
        return head + s.replace(/(零.)*零元/, '元')
                .replace(/(零.)+/g, '零')
                .replace(/^整$/, '零元整');
    };

    var setAmount = function (el, direction, amount) {
        var tds = $(el).children(direction);
        $('> span', tds).text('');
        var i = 1;
        while (amount > 0 || i < 4) {
            var digit = amount % 10;
            amount = Math.floor(amount / 10);
            $('> span', tds[tds.size() - i]).text(digit);
            i++;
        }
    };

    var records = $('.record');
    var left = 4 - records.size();
    var body = $('body');
    for (var i = 0; i < left; i++)
        faForm.addInlineField('#records-template', 'records')
    body.on('click', '.record td.debit, .record td.credit', function () {
        var self = $(this);
        self.parent().children('.' + self.attr('class')).first().children().show().focus();
    });
    body.on('blur', '.record td.debit input, .record td.credit input', function () {
        var self = $(this);
        var td = self.parent();
        var tr = td.parent();
        self.hide();
        $('td.debit > span, td.credit > span', tr).text('');
        if (!self.val()) {
            self.val('');
            $('.amount', tr).val('');
        } else {
            var amount = Math.round(self.val() * 100);
            var direction = '.' + td.attr('class');
            $('.debit input, .credit input', tr).val('');
            self.val(amount / 100);
            $('.amount', tr).val(amount / 100);
            $('.direction', tr).val(direction == '.debit' ? '1' : '-1');
            setAmount(tr, direction, amount);
        }
        var sum = {'1': 0, '-1': 0};
        $('.record').each(function () {
            if ($('.amount', this).val() != '')
                sum[$('.direction', this).val()] += Math.round(parseFloat($('.amount', this).val()) * 100);
        });
        setAmount('.summary', '.debit', sum['1']);
        setAmount('.summary', '.credit', sum['-1']);
        if (sum['1'] == sum['-1']) {
            $('.summary > td > span').first().text(digitUppercase(sum['1'] / 100));
        } else
            $('.summary > td > span').first().text('');
    });
    records.each(function () {
        var self = $(this);
        $($('.direction', self).val() == '1' ? '.debit input' : '.credit input', self).val($('.amount', self).val()).blur();
    });
})();
