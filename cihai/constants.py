# -*- coding: utf8 - *-
from __future__ import unicode_literals

#: Default configuration
DEFAULT_CONFIG = {
    "debug": False,
    "database": {"url": 'sqlite:///{user_data_dir}/cihai.db'},
    "dirs": {
        "cache": '{user_cache_dir}',
        "log": '{user_log_dir}',
        "data": '{user_data_dir}',
    },
}

#: User will be prompted to automatically configure their installation for UNIHAN
SUGGESTED_CONFIG = {
    "datasets": {"unihan": "cihai.unihan.Unihan"},
    "extensions": {"unihan": {"variants": "cihai.unihan.UnihanVariants"}},
}
