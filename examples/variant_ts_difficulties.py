#!/usr/bin/env python
# -*- coding: utf8 - *-
from __future__ import print_function, unicode_literals

from cihai.core import Cihai
from cihai.data.unihan.bootstrap import bootstrap_unihan


def run(unihan_options={}):
    c = Cihai()
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        bootstrap_unihan(c.sql.metadata, options=unihan_options)
        c.sql.reflect_db()  # automap new table created during bootstrap

    c.unihan.add_plugin(
        'cihai.data.unihan.dataset.UnihanVariants', namespace='variants'
    )

    print(
        "This example prints some tricky cases of character-by-character "
        "Traditional-Simplified mapping."
    )
    print("https://www.unicode.org/reports/tr38/#N10211")
    print("3.7.1 bullet 4")

    for char in c.unihan.with_fields("kTraditionalVariant", "kSimplifiedVariant"):
        print("Character: {}".format(char.char))
        trad = set(char.untagged_vars("kTraditionalVariant"))
        simp = set(char.untagged_vars("kSimplifiedVariant"))
        Unihan = c.sql.base.classes.Unihan
        if Unihan.char in trad and Unihan.char in simp:
            print("Case 1")
        else:
            print("Case 2 (non-idempotent)")
        for trad_var in trad:
            print("s2t: {}".format(trad_var))
        for simp_var in simp:
            print("t2s: {}".format(simp_var))


if __name__ == '__main__':
    run()
