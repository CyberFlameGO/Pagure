# -*- coding: utf-8 -*-

"""
 (c) 2014-2017 - Copyright Red Hat Inc

 Authors:
   Pierre-Yves Chibon <pingou@pingoured.fr>

"""

import logging

import flask

from sqlalchemy.exc import SQLAlchemyError

import pagure
from pagure.flask_app import logout
from pagure.config import config as pagure_config
import flask_fas_openid
FAS = flask_fas_openid.FAS()

_log = logging.getLogger(__name__)


@FAS.postlogin
def set_user(return_url):
    ''' After login method. '''
    if flask.g.fas_user.username is None:
        flask.flash(
            'It looks like your OpenID provider did not provide an '
            'username we could retrieve, username being needed we cannot '
            'go further.', 'error')
        logout()
        return flask.redirect(return_url)

    flask.session['_new_user'] = False
    if not pagure.lib.search_user(
            flask.g.session, username=flask.g.fas_user.username):
        flask.session['_new_user'] = True

    try:
        pagure.lib.set_up_user(
            session=flask.g.session,
            username=flask.g.fas_user.username,
            fullname=flask.g.fas_user.fullname,
            default_email=flask.g.fas_user.email,
            ssh_key=flask.g.fas_user.get('ssh_key'),
            keydir=pagure_config.get('GITOLITE_KEYDIR', None),
        )

        # If groups are managed outside pagure, set up the user at login
        if not pagure_config.get('ENABLE_GROUP_MNGT', False):
            user = pagure.lib.search_user(
                flask.g.session, username=flask.g.fas_user.username)
            groups = set(user.groups)
            fas_groups = set(flask.g.fas_user.groups)
            # Add the new groups
            for group in fas_groups - groups:
                groupobj = None
                if group:
                    groupobj = pagure.lib.search_groups(
                        flask.g.session, group_name=group)
                if groupobj:
                    try:
                        pagure.lib.add_user_to_group(
                            session=flask.g.session,
                            username=flask.g.fas_user.username,
                            group=groupobj,
                            user=flask.g.fas_user.username,
                            is_admin=pagure.is_admin(),
                            from_external=True,
                        )
                    except pagure.exceptions.PagureException as err:
                        _log.error(err)
            # Remove the old groups
            for group in groups - fas_groups:
                if group:
                    try:
                        pagure.lib.delete_user_of_group(
                            session=flask.g.session,
                            username=flask.g.fas_user.username,
                            groupname=group,
                            user=flask.g.fas_user.username,
                            is_admin=pagure.is_admin(),
                            force=True,
                            from_external=True,
                        )
                    except pagure.exceptions.PagureException as err:
                        _log.error(err)

        flask.g.session.commit()
    except SQLAlchemyError as err:
        flask.g.session.rollback()
        _log.exception(err)
        flask.flash(
            'Could not set up you as a user properly, please contact '
            'an admin', 'error')
        # Ensure the user is logged out if we cannot set them up
        # correctly
        logout()
    return flask.redirect(return_url)