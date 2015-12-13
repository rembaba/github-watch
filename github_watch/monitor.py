"""Github monitoring service
"""
import os
import sys
import json
import yaml
import time
import logging
from multiprocessing import Process
import urllib2
import requests
from requests.auth import HTTPBasicAuth


from util import get_new_entries

DEFAULT_POLL_INTERVAL = 5 # default poll interval in secs

GITHUB_API = "https://api.github.com/repos"


class GithubClient(object):
    """Client to process github api responses
    """

    def __init__(self, owner, repo, auth_user=None, auth_token=None):
        """Github client
        """
        self.owner = owner
        self.repo = repo
        self.auth_user = auth_user
        self.auth_token = auth_token

    def _get(self, url, auth=None):
        """Make http request to a url and return response in json
        """
        if self.auth_user and self.auth_token:
            response = requests.get(url, auth=(self.auth_user, self.auth_token))
        else:
            response = requests.get(url)

        status_code = response.status_code
        if status_code != 200:
            raise urllib2.URLError("Error getting API response")
        return response.json()


    def list_contributors(self):
        """Get contributors for a repo
        """
        # example: https://api.github.com/repos/docker/swarm/contributors
        api_url = "{github_api}/{owner}/{repo}/contributors".format(
                                        github_api=GITHUB_API,
                                        owner=self.owner, repo=self.repo)
        print("Listing contributors from {0}".format(api_url))
        contributors = self._get(api_url)
        return contributors


class GithubRepoMonitor(Process):
    """Service to watch a github repo
    """

    def __init__(self, owner, repo, auth_user, auth_token,
                 poll_interval, notification_receivers, logger):
        """Monitoring service for github repo
        """
        self.github_client = GithubClient(owner, repo, auth_user, auth_token)
        self.poll_interval = poll_interval
        self.notification_receivers = notification_receivers
        self.log = logger
        # cached contributors
        self._cache = self.github_client.list_contributors()


    def start(self):
        """Run the main thread
        """
        while True:
            self.notify_new_contributors()
            time.sleep(self.poll_interval)

    def notify_new_contributors(self):
        """Get updated repo contributors
        """
        self.log.info("Checking new contributors")
        new_contributors = []
        # initialize the cache
        if not self._cache or len(self._cache) == 0:
            self.log.debug("Initializing...")
            self._cache= self.github_client.list_contributors()
        else:
            self.log.debug("Listing contributors on github...")
            contributors = self.github_client.list_contributors()
            new_contributors = get_new_entries(self._cache, contributors)
            # update the cache
            self._cache = new_contributors
            self.log.debug("New contributors are: {}".format(new_contributors))
            self.notify(new_contributors)

    def notify(self, data, destination=None):
        """Notify about the new updates
        """
        # we only handle the simplest case of posting the data to some API
        # TODO: handle authentication
        for receiver in self.notification_receivers:
            url = receiver["url"]
            # just post the raw data
            r = requests.post(url, data)
            if r.status_code == 200:
                self.log.debug("Notified {} successfully".format(url))
            else:
                self.log.debug("Posting to {} faliled. Status Code: {}".format(url, r.status_code))


class ConfigError(Exception):
    pass


def load_config(config_file):
    """Load a config file and returns a dict
    """
    if not os.path.exists(os.path.abspath(config_file)):
        raise ConfigError("The config file {0} is not found".format(
                          os.path.abspath(config_file)))
    with open(config_file, "r") as f:
        config = yaml.load(f)
    return config

def is_valid_config(config):
    """Validate the required keys are defined in the config
    """
    if (not "github" in config or
       "owner" not in config["github"] or
       "repo" not in config["github"]):
        return False
    return True


def get_logger():
    DEFAULT_LOG_LEVEL = logging.DEBUG

    logger = logging.getLogger("github_watch")
    logger.setLevel(DEFAULT_LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler("github_watch.log")
    file_handler.setLevel(DEFAULT_LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.handlers = [console_handler, file_handler]
    return logger


def main():
    """Monitoring service for github
    Usage: python monitor.py <config_file>
    """
    def usage():
        print "python monitor.py <config_file>"
    # load config from a yaml file
    if len(sys.argv) < 2:
        print "Config file must be specified"
        sys.exit(1)

    config_file = sys.argv[1]

    logger = get_logger()
    config = load_config(config_file)
    # exit if config does not contain required keys
    if not is_valid_config(config):
        print "Config is invalid: github repo and owner are required"
        sys.exit(1)
    poll_interval = config.get("poll_interval", DEFAULT_POLL_INTERVAL)
    auth_user = config["github"].get("auth_user", None)
    auth_token = config["github"].get("auth_token", None)
    notification_receivers = config.get("notification_receivers", [])
    monitor_service = GithubRepoMonitor(owner=config["github"]["owner"],
                                        repo=config["github"]["repo"],
                                        auth_user=auth_user, auth_token=auth_token,
                                        poll_interval=int(poll_interval),
                                        notification_receivers=notification_receivers,
                                        logger=logger)
    monitor_service.start()


if __name__ == '__main__':
    main()
