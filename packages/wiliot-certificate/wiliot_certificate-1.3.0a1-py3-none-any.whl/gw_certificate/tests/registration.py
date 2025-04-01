import datetime
import time
import os
from enum import Enum

from wiliot_api.api_client import WiliotCloudError

from gw_certificate.common.debug import debug_print
from gw_certificate.tests.generic import INCONCLUSIVE_MINIMUM, PassCriteria, MINIMUM_SCORE, PERFECT_SCORE, GenericStage, GenericTest, INFORMATIVE
from gw_certificate.api.extended_api import ExtendedEdgeClient
from gw_certificate.tests.static.connection_defines import *
from gw_certificate.tests.static.references import GW_REGISTER_DOC, GW_MQTT_DOC


# HELPER DEFINES
REG_CERT_OWNER_ID = 'gw-certification-account'
ENV_VAR_AWS = 'WLT_REG_CERT_KEY_AWS'
STAGES_TIMEOUT = 2
TOKEN_EXPIRY_MINUTES = 3

ERROR_NO_API_KEY = f'You must receive an API security key from wiliot and save if to the environment variable {ENV_VAR_AWS} first.'
ERROR_NO_REGISTER = 'Gateway did not register itself in time.'
ERROR_NO_ONLINE = 'Gateway did not connect to MQTT in time.'
ERROR_NO_ACTIVE = 'Gateway did not upload a status message with its configurations in time.'
ERROR_NO_REFRESH = 'Gateway did not reconnect to MQTT in time.'

# HELPER CLASSES
class GetGwField(Enum):
    STATUS = 'status'
    ONLINE = 'online'
    ONLINE_UPDATED_AT = 'onlineUpdatedAt'
    ACTIVATED_AT = 'activatedAt'

class Status(Enum):
    PRE_REGISTERED = 'pre-registered'
    APPROVED = 'approved'
    ACTIVE = 'active'

class Online(Enum):
    FALSE = False
    TRUE = True

class SharedData():
    """
    Hold variables which values must be shared between different stages.
    gw_online_ts hold the time in which the gateway status became online
    """
    def __init__(self):
        self.gw_online_ts = None

# TEST STAGES
class GenericRegistrationStage(GenericStage):
    def __init__(self, gw_id, edge:ExtendedEdgeClient, **kwargs):
        self.__dict__.update(kwargs)
        self.gw_id = gw_id
        self.edge = edge
        super().__init__(**self.__dict__)
    
    def get_gateway_field(self, field:GetGwField):
        temp = self.edge.get_gateway(self.gw_id)
        return temp[field.value]

class RegistryStage(GenericRegistrationStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.stage_tooltip = "Validate the gateway's registry step"
        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def prepare_stage(self):
        super().prepare_stage()
        debug_print('Pre-registering the gateway, please make sure it is not registered to any other account '
                    'and that your device is ready to run the registration flow')
        
        def pre_register_gw_anew(gw_id):
            try:
                pre_registered = self.edge.register_gateway([gw_id])
            except WiliotCloudError as wce:
                wce_dict = wce.args[0]
                status_code = wce_dict.get('status_code')
                msg = wce_dict.get('message')
                if status_code == 400 and 'already exists' in msg:
                    debug_print(f'{gw_id} already exists in Wiliot platform! Deleting and pre-registering from scratch')
                    self.edge.delete_gateway(gw_id)
                    pre_registered = self.edge.register_gateway([gw_id])
                else:
                    raise wce
            return pre_registered

        pre_registered = pre_register_gw_anew(self.gw_id)
        if not pre_registered:
            debug_print('Failed pre-registering the gateway')
            raise Exception(f"Failed pre-registering the gateway. Make sure:\n-Your API key ({ENV_VAR_AWS}) is valid.\n"
                            "-You have a stable internet connection.\nOtherwise, try again later.")
        debug_print(f"{self.gw_id} was pre-registered successfully")

    def run(self):
        super().run()
        debug_print(f"Waiting for the gateway to finish the Registry step..")
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=STAGES_TIMEOUT)
        self.status = self.get_gateway_field(GetGwField.STATUS)
        while datetime.datetime.now() < timeout and not any(self.status == s.value for s in {Status.APPROVED, Status.ACTIVE}):
            time.sleep(5)
            self.status = self.get_gateway_field(GetGwField.STATUS)

    def generate_stage_report(self):
        self.add_report_header()
        if not any(self.status == s.value for s in {Status.APPROVED, Status.ACTIVE}):
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = ERROR_NO_REGISTER
            self.add_to_stage_report(ERROR_NO_REGISTER)
            debug_print(f"The gateway failed to register. Its status is '{self.status}' while it is expected to be '{Status.APPROVED.value}'.")
            self.add_to_stage_report(f"There was an error in the Device-authorize or Registry steps.")
            self.add_to_stage_report(f"Please go over the Device-authorize and Registry sections in this document:\n{GW_REGISTER_DOC}")
            # TODO Ideally we should know where the error is exactly and inform the user. We currently lack such resolution
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report("Device-authorize and Registry requests were issued well.")
            self.add_to_stage_report("Gateway registered successfully.")
            debug_print("Gateway registered successfully")

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        return super().generate_stage_report()
    
class OnlineStage(GenericRegistrationStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.stage_tooltip = "Validate the gateway become online on the platform"
        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def prepare_stage(self):
        super().prepare_stage()

    def run(self):
        super().run()
        debug_print(f"Waiting for the gateway to connect to MQTT..")
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=STAGES_TIMEOUT)
        self.online = self.get_gateway_field(GetGwField.ONLINE)
        while datetime.datetime.now() < timeout and self.online != True:
            time.sleep(5)
            self.online = self.get_gateway_field(GetGwField.ONLINE)

    def generate_stage_report(self):
        self.add_report_header()
        if self.online != True:
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = ERROR_NO_ONLINE
            self.add_to_stage_report(ERROR_NO_ONLINE)
            self.add_to_stage_report(f"Either it didn't acquire a token or it didn't connect to MQTT in time.")
            self.add_to_stage_report(f"Please go over the Poll For Token section in:\n{GW_REGISTER_DOC}")
            self.add_to_stage_report(f"and the MQTT details in:\n{GW_MQTT_DOC}")
            debug_print("Gateway did not connect ot MQTT within time limit")
            # TODO Ideally we should know where the error is exactly and inform the user. We currently lack such resolution
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report("Token acquisition and MQTT connection were done succesfully.")
            self.add_to_stage_report("Gateway is online.")
            debug_print("Gateway connected to MQTT successfully, it is online")
            self.shared_data.gw_online_ts = datetime.datetime.now()

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        return super().generate_stage_report()

class ActiveStage(GenericRegistrationStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.stage_tooltip = "Validate the gateway upload a status message upon MQTT connection"
        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def prepare_stage(self):
        super().prepare_stage()

    def run(self):
        super().run()
        debug_print(f"Waiting for the gateway to upload a status message..")
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=STAGES_TIMEOUT)
        self.status = self.get_gateway_field(GetGwField.STATUS)
        while datetime.datetime.now() < timeout and self.status != Status.ACTIVE.value:
            time.sleep(5)
            self.status = self.get_gateway_field(GetGwField.STATUS)

    def generate_stage_report(self):
        self.add_report_header()
        if self.status != Status.ACTIVE.value:
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = ERROR_NO_ACTIVE
            self.add_to_stage_report(ERROR_NO_ACTIVE)
            self.add_to_stage_report(f"Please go over the Status section in:\n{GW_MQTT_DOC}")
            debug_print("Gateway did not upload a status message upon connecting to MQTT")
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report("The gateway uploaded a status message in time.")
            self.add_to_stage_report("Gateway is active.")
            debug_print("Gateway uploaded a status message, it is active")

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        return super().generate_stage_report()

class RefreshStage(GenericRegistrationStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.stage_tooltip = "Validate the gateway refresh-token step"
        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def prepare_stage(self):
        super().prepare_stage()

    def run(self):
        super().run()
        debug_print(f"Waiting for the token to expire..")
        timeout = self.shared_data.gw_online_ts + datetime.timedelta(minutes=TOKEN_EXPIRY_MINUTES)
        while datetime.datetime.now() < timeout:
            time.sleep(5)

        def kick_gw_from_mqtt():
            response = self.edge.kick_gw_from_mqtt(self.gw_id)
            debug_print(f"Kick response:{response}")

        debug_print(f"Token expired, kicking gateway")
        kick_gw_from_mqtt()

        debug_print(f"Waiting for the gateway to refresh its token and connect to MQTT..")
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=STAGES_TIMEOUT)
        self.online = self.get_gateway_field(GetGwField.ONLINE)
        while datetime.datetime.now() < timeout and self.online != True:
            time.sleep(5)
            self.online = self.get_gateway_field(GetGwField.ONLINE)

    def generate_stage_report(self):
        self.add_report_header()
        if self.online != True:
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = ERROR_NO_REFRESH
            self.add_to_stage_report(ERROR_NO_REFRESH)
            self.add_to_stage_report(f"Either it didn't refresh its token or it didn't connect to MQTT in time.")
            self.add_to_stage_report(f"Please go over the Refresh Token section in:\n{GW_REGISTER_DOC}")
            self.add_to_stage_report(f"and the MQTT details in:\n{GW_MQTT_DOC}")
            debug_print("Gateway did not reconnect MQTT (was the token refreshed?)")
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report("Token refresh and MQTT reconnection were done succesfully.")
            self.add_to_stage_report("Gateway is online.")

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        return super().generate_stage_report()


STAGES = [RegistryStage, OnlineStage, ActiveStage, RefreshStage]

class RegistrationTest(GenericTest):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.test_tooltip = "Stages related to the process of registering a gateway with the Wiliot cloud"

        # Set up the edge client for all stages
        env = '' if self.env == 'prod' else '_' + str(self.env).upper()
        api_sec_key = os.environ.get(ENV_VAR_AWS + env)
        if not api_sec_key:
            raise Exception(f"An API security key must be set to the envrionment variable {ENV_VAR_AWS} in order to run the RegistrationTest")
        self.edge = ExtendedEdgeClient(api_sec_key, REG_CERT_OWNER_ID, env=self.env)

        self.shared_data = SharedData()

        super().__init__(**self.__dict__, test_name=type(self).__name__)
        stages = STAGES
        self.stages = [stage(**self.__dict__) for stage in stages]
        
    def run(self):
        super().run()
        self.test_pass = PERFECT_SCORE
        for idx, stage in enumerate(self.stages):
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self.test_pass, stage)
            if self.test_pass != PERFECT_SCORE and stage != self.stages[-1]:
                debug_print(f"{type(self).__name__} stopped without running all of its stages since {type(stage).__name__} failed")
                self.add_to_test_report(f"{type(self).__name__} stopped without running all of its stages since {type(stage).__name__} failed")
                self.stages = self.stages[0:idx + 1]
                break
    
    def end_test(self):
        debug_print(f'Deleting {self.gw_id} from {REG_CERT_OWNER_ID} before exiting')
        self.edge.delete_gateway(self.gw_id)
        super().end_test()
