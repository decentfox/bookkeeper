import csv
import sys

from . import create_app

from bookkeeper import models


def import_account_titles():
    with create_app().app_context():
        inp = csv.reader(sys.stdin)
        next(inp)
        for row in inp:
            models.Account.create(
                code=row[0], title=row[1],
                direction=models.Direction.credit if row[3] == '贷'
                else models.Direction.debit)
