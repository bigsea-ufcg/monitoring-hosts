import sys

from monascaclient import client as monclient, ksclient
import monascaclient.exc as exc


class MonascaMonitor:

    def __init__(self, configuration):
        try:
            if configuration.has_section('monasca'):
                self.client = self._get_monasca_client(configuration)
            else:
                print "No section monasca in configuration file"
                raise Exception("No section monasca in configuration file")
        except Exception as e:
            print e.message
            sys.exit(1)

    def _get_monasca_client(self, configuration):

        # Authenticate to Keystone
        ks = ksclient.KSClient(
            auth_url=configuration.get('monasca', 'auth_url'),
            username=configuration.get('monasca', 'username'),
            password=configuration.get('monasca', 'password'),
            project_name=configuration.get('monasca', 'project_name'),
            debug=False
        )

        # Monasca Client
        monasca_client = monclient.Client(
            configuration.get('monasca', 'monasca_api_version'), ks.monasca_url,
            token=ks.token, debug=False
        )

        return monasca_client

    def send_metrics(self, measurements):

        batch_metrics = {'jsonbody': measurements}
        try:
            self.client.metrics.create(**batch_metrics)
            return True
        except exc.HTTPException as httpex:
            return False
        except Exception as ex:

            return False
