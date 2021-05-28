import os
import sys
import hashlib
import requests
import glob

from time import sleep
from requests import exceptions as requests_exceptions
from requests.auth import AuthBase

from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.exceptions import AirflowException
from airflow import configuration
from airflow.models import Connection

from hopsworks_plugin.hooks.hopsworks_hook import *


class GiottoHook(HopsworksHook):
    """
    Hook to interact with Hopsworks
    """
    #def __init__(self, hopsworks_conn_id='hopsworks_default', project_id=None,
    #             project_name=None, owner=None):
    #    super().__init__(self)

    def get_job_state(self, job_name):
        """
        Function to get the state of a job

        :param job_name: Name of the job in Hopsworks
        :type job_name: str
        """
        method, endpoint = JOB_STATE
        endpoint = endpoint.format(project_id=self.project_id, job_name=job_name)
        response = self._do_api_call(method, endpoint)
        item = response['items'][0]
        #self.log.debug(item)
        """
        G.A: Restituiamo lo stato dell'object JobExecution e non solo l'attributo state
        """
        return item
