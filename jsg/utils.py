# -*- coding: UTF-8 -*-
# vim: ts=4 sts=4 sw=4 tw=100 sta et


class NotInRole(Exception):
    pass


def check_role(my_roles, requested_roles):
    if not my_roles:
        return True

    for role in my_roles:
        if role in requested_roles:
            return True
    raise NotInRole()
