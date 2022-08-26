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


class ConsumerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.secret_relation_changed, self._on_relation_changed)
        self.framework.observe(self.on.install, self._on_install)

    def _on_install(self, event):
        self.unit.status = ActiveStatus()

    def _on_relation_changed(self, event):
        if 'the-secret' in event.relation.data[event.app]:
            sec_id = event.relation.data[event.app]['the-secret']
            s = self.model.get_secret(sec_id)
            payload = s.get('payload')
            logger.debug(f'received permission from {event.app} for secret {s} with payload {payload}')

    def _on_fortune_action(self, event):
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})


if __name__ == "__main__":
    main(ConsumerCharm)
