# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
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


"""Module tests."""

from __future__ import absolute_import, print_function

from click.testing import CliRunner

from invenio_accounts.cli import roles_add, roles_create, roles_remove, \
    users_activate, users_create, users_deactivate


def test_cli_createuser(script_info):
    """Test create user CLI."""
    runner = CliRunner()

    # Missing params
    result = runner.invoke(
        users_create, input='1234\n1234\n', obj=script_info)
    assert result.exit_code != 0

    # Create user with invalid email
    result = runner.invoke(
        users_create,
        ['not-an-email', '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 2

    # Create user
    result = runner.invoke(
        users_create,
        ['info@inveniosoftware.org', '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 0


def test_cli_createrole(script_info):
    """Test create user CLI."""
    runner = CliRunner()

    # Missing params
    result = runner.invoke(
        roles_create, ['-d', 'Test description'],
        obj=script_info)
    assert result.exit_code != 0

    # Create role
    result = runner.invoke(
        roles_create,
        ['superusers', '-d', 'Test description'],
        obj=script_info)
    assert result.exit_code == 0


def test_cli_addremove_role(script_info):
    """Test add/remove role."""
    runner = CliRunner()

    # Create a user and a role
    result = runner.invoke(
        users_create,
        ['a@example.org', '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 0
    result = runner.invoke(roles_create, ['superuser'], obj=script_info)
    assert result.exit_code == 0

    # User not found
    result = runner.invoke(
        roles_add, ['inval@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Add:
    result = runner.invoke(
        roles_add, ['a@example.org', 'invalid'],
        obj=script_info)
    assert result.exit_code != 0

    result = runner.invoke(
        roles_remove, ['inval@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Remove:
    result = runner.invoke(
        roles_remove, ['a@example.org', 'invalid'],
        obj=script_info)
    assert result.exit_code != 0

    result = runner.invoke(
        roles_remove, ['b@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    result = runner.invoke(
        roles_remove, ['a@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Add:
    result = runner.invoke(roles_add,
                           ['a@example.org', 'superuser'],
                           obj=script_info)
    assert result.exit_code == 0
    result = runner.invoke(
        roles_add,
        ['a@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Remove:
    result = runner.invoke(
        roles_remove, ['a@example.org', 'superuser'],
        obj=script_info)
    assert result.exit_code == 0


def test_cli_activate_deactivate(script_info):
    """Test create user CLI."""
    runner = CliRunner()

    # Create a user
    result = runner.invoke(
        users_create,
        ['a@example.org', '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 0

    # Activate
    result = runner.invoke(users_activate, ['in@valid.org'],
                           obj=script_info)
    assert result.exit_code != 0
    result = runner.invoke(users_deactivate, ['in@valid.org'],
                           obj=script_info)
    assert result.exit_code != 0

    result = runner.invoke(users_activate, ['a@example.org'],
                           obj=script_info)
    assert result.exit_code == 0
    result = runner.invoke(users_activate, ['a@example.org'],
                           obj=script_info)
    assert result.exit_code == 0

    # Deactivate
    result = runner.invoke(users_deactivate,
                           ['a@example.org'], obj=script_info)
    assert result.exit_code == 0
    result = runner.invoke(users_deactivate,
                           ['a@example.org'], obj=script_info)
    assert result.exit_code == 0
