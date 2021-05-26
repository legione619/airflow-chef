#
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from hopsworks_plugin.hooks.hopsworks_hook import HopsworksHook
from hopsworks_plugin.hooks.giotto_hook import GiottoHook
from hopsworks_plugin.sensors.hopsworks_sensor import *


class GiottoJobSuccessSensor(HopsworksJobSuccessSensor):
    """
    Sensor to wait for a successful completion of a job
    If the job fails, the sensor will fail

    :param job_name: Name of the job in Hopsworks
    :type job_name: str
    :param project_id: Hopsworks Project ID the job is associated with
    :type project_id: int
    :param project_name: Hopsworks Project name this job is associated with
    :type project_name: str
    """

    @apply_defaults
    def __init__(
            self,
            hopsworks_conn_id = 'hopsworks_default',
            job_name = None,
            project_id = None,
            project_name = None,
            poke_interval = 10,
            timeout = 3600,
            *args,
            **kwargs):
        super(GiottoJobSuccessSensor, self).__init__(*args, **kwargs)
        self.hopsworks_conn_id = hopsworks_conn_id
        self.job_name = job_name
        self.project_id = project_id
        self.project_name = project_name

    def _get_hook(self):
        return GiottoHook(self.hopsworks_conn_id, self.project_id, self.project_name, self.owner)

    def poke(self, context):
        hook = self._get_hook()
        stateJobObject = hook.get_job_state(self.job_name)
        finalStatus = stateJobObject['finalStatus']
        state = stateJobObject['state']
        if finalStatus.upper() in JOB_FAILED_FINAL_STATES:
            raise AirflowException("Hopsworks job failed")

        return state.upper() in JOB_SUCCESS_FINAL_STATES
