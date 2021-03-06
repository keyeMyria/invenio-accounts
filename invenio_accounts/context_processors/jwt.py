# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""JWT context processors."""

from flask import current_app, render_template
from jinja2 import Markup

from ..proxies import current_accounts


def jwt_proccessor():
    """Context processor for jwt."""
    def jwt():
        """Context processor function to generate jwt."""
        token = current_accounts.jwt_creation_factory()
        return Markup(
            render_template(
                current_app.config['ACCOUNTS_JWT_DOM_TOKEN_TEMPLATE'],
                token=token
            )
        )

    def jwt_token():
        """Context processor function to generate jwt."""
        return current_accounts.jwt_creation_factory()

    return {
        'jwt': jwt,
        'jwt_token': jwt_token,
    }
