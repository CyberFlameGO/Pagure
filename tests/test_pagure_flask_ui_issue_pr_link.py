# -*- coding: utf-8 -*-

"""
 (c) 2018 - Copyright Red Hat Inc

 Authors:
   Pierre-Yves Chibon <pingou@pingoured.fr>

"""

__requires__ = ['SQLAlchemy >= 0.8']
import pkg_resources

import datetime
import json
import unittest
import re
import shutil
import sys
import tempfile
import time
import os

import pygit2
from mock import ANY, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

import pagure
import pagure.lib
import tests
from pagure.lib.repo import PagureRepo


class PagureFlaskPrIssueLinkTest(tests.Modeltests):
    """ Tests pagure when linking PRs to tickets """

    maxDiff = None

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        super(PagureFlaskPrIssueLinkTest, self).setUp()

        tests.create_projects(self.session)
        tests.create_projects(
            self.session, is_fork=True, user_id=2, hook_token_suffix='bar')
        tests.create_projects_git(os.path.join(self.path, 'repos'), bare=True)
        tests.create_projects_git(os.path.join(
            self.path, 'repos', 'forks', 'foo'), bare=True)

        repo = pagure.lib.get_authorized_project(self.session, 'test')

        # Create issues to play with
        msg = pagure.lib.new_issue(
            session=self.session,
            repo=repo,
            title=u'tést íssüé',
            content='We should work on this',
            user='pingou',
            ticketfolder=None
        )
        self.session.commit()
        self.assertEqual(msg.title, u'tést íssüé')

        msg = pagure.lib.new_issue(
            session=self.session,
            repo=repo,
            title=u'tést íssüé #2',
            content='We should still work on this',
            user='foo',
            ticketfolder=None
        )
        self.session.commit()
        self.assertEqual(msg.title, u'tést íssüé #2')

        # Add a commit to the fork

        newpath = tempfile.mkdtemp(prefix='pagure-fork-test')
        repopath = os.path.join(newpath, 'test')
        clone_repo = pygit2.clone_repository(os.path.join(
            self.path, 'repos', 'forks', 'foo', 'test.git'), repopath)

        # Create a file in that git repo
        with open(os.path.join(repopath, 'sources'), 'w') as stream:
            stream.write('foo\n bar')
        clone_repo.index.add('sources')
        clone_repo.index.write()

        try:
            com = repo.revparse_single('HEAD')
            prev_commit = [com.oid.hex]
        except:
            prev_commit = []

        # Commits the files added
        tree = clone_repo.index.write_tree()
        author = pygit2.Signature(
            'Alice Author', 'alice@authors.tld')
        committer = pygit2.Signature(
            'Cecil Committer', 'cecil@committers.tld')
        clone_repo.create_commit(
            'refs/heads/master',  # the name of the reference to update
            author,
            committer,
            'Add sources file for testing\n\n Relates to #2',
            # binary string representing the tree object ID
            tree,
            # list of binary strings representing parents of the new commit
            prev_commit
        )
        refname = 'refs/heads/master:refs/heads/master'
        ori_remote = clone_repo.remotes[0]
        PagureRepo.push(ori_remote, refname)

        # Create the corresponding PR

        repo = pagure.lib.get_authorized_project(self.session, 'test')
        fork_repo = pagure.lib.get_authorized_project(
            self.session, 'test', user='foo')

        request = pagure.lib.new_pull_request(
            self.session,
            branch_from='master',
            repo_to=repo,
            branch_to='master',
            title='test PR',
            user='foo',
            requestfolder=None,
            initial_comment=None,
            repo_from=fork_repo,
        )
        self.session.commit()

        pagure.lib.tasks.link_pr_to_ticket(request.uid)
        self.assertEqual(request.id, 3)

    def test_ticket_no_link(self):
        """ Test that no Related PR(s) block is showing in the issue page.
        """
        output = self.app.get('/test/issue/1')
        self.assertEqual(output.status_code, 200)
        self.assertNotIn(
            u'<strong>Related PR(s)</strong>',
            output.data.decode('utf-8'))

    def test_ticket_link(self):
        """ Test that no Related PR(s) block is showing in the issue page.
        """
        time.sleep(1)
        output = self.app.get('/test/issue/2')
        print output.data.decode('utf-8')
        self.assertEqual(output.status_code, 200)
        self.assertIn(
            u'<strong>Related PR(s)</strong>',
            output.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)