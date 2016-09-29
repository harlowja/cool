from cool import utils

import six
from voluptuous import Schema
from voluptuous import Required, All, Length, Range, Optional


class BuildParser(object):
    # Inspired by:
    #
    # https://github.com/sahid/warm-templates/blob/master/wordpress/stack.yaml
    server_schema = {
        Required('name'): All(str, Length(min=1, max=15)),
        Required('flavor'): All(str, Length(min=1)),
        Required('image'): All(str, Length(min=1)),
        Required('availability_zone'): All(str, Length(min=1)),
        Optional('user_data'): str,
        Optional('networks'): Schema([
            {
                Required('name'): All(str, Length(min=1)),
            }
        ]),
        Optional('security_groups'): Schema([six.string_types]),
    }
    network_schema = {
        Required('name'): All(str, Length(min=1, max=15)),
        Required('subnets'): Schema([
            {
                Required('name'): All(str, Length(min=1, max=15)),
                Required('cidr'): All(str, Length(min=1)),
                Optional('ip_version'): int,
            }
        ])
    }
    volume_schema = {
         Required('name'): All(str, Length(min=1, max=15)),
         Optional('size'): int,
    }
    security_group_rules_schema = Schema([
        {
            Required('protocol'): ['tcp', 'icmp', 'udp'],
            Required('from_port'): int,
            Required('to_port'): int,
            Optional('cidr'): All(str, Length(min=1)),
        }
    ])
    security_group_schema = Schema([
        {
            Required('name'): All(str, Length(min=1)),
            Optional('description'): str,
            Required('rules'): security_group_rules_schema,
        }
    ])
    schema = Schema({
        Optional('server'): server_schema,
        Optional('volume'): volume_schema,
        Optional('network'): network_schema,
        Optional('security_group'): security_group_schema,
    })

    def parse(self, raw_request):
        request = utils.safe_load_yaml(raw_request)
        self.schema(request)
        # The above will do basic validation, now we have to parse
        # the pieces apart and ensure it really makes sense knowing
        # the associations between items (aka the context).