ID = "ECS_SERVICE_PRIMARY_DEPLOYMENT_COMPLETED_WAITER_ID"
CONFIG = {
    'version': 2,
    'waiters': {
        ID: {
            'delay': 15,
            'operation': 'DescribeServices',
            'maxAttempts': 40,
            'acceptors': [
                {
                    'expected': True,
                    'matcher':  'path',
                    'state':    'success',
                    'argument': "length(services[].deployments[] | [?status == 'PRIMARY' && rolloutState == 'COMPLETED']) == `1`"
                },
                {
                    'expected': False,
                    'matcher':  'path',
                    'state':    'failure',
                    'argument': "length(services[]) == `1`"
                },
                {
                    'expected': False,
                    'matcher':  'path',
                    'state':    'failure',
                    'argument': "length(services[].deployments[?status == 'PRIMARY']) == `1`"
                },
                {
                    'expected': True,
                    'matcher':  'path',
                    'state':    'failure',
                    'argument': "length(services[].deployments[] | [?status == 'PRIMARY' && rolloutState == 'FAILED']) == `1`"
                },
            ]
        }
    }
}
