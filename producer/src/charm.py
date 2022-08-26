#!/usr/bin/env python3
# Copyright 2022 Robert Carlsen
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)

class ProducerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.secret_relation_joined, self._on_relation_joined)

    def _on_install(self, event):
        # create a global secret
        s = self.app.add_secret('foo', payload='top-secret')
        logger.debug(f'just created secret {s}')
        self.unit.status = ActiveStatus()

    def _on_relation_joined(self, event):
        # share a global secret to units
        s = self.model.get_secret('foo')
        s.grant(event.relation)
        event.relation.data[self.app]['the-secret'] = s.id
        logger.debug(f'granting {event.app.name} access to secret {s}')

    def _on_fortune_action(self, event):
        """Just an example to show how to receive actions.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle actions, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the actions.py file.

        Learn more about actions at https://juju.is/docs/sdk/actions
        """
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})


if __name__ == "__main__":
    main(ProducerCharm)
