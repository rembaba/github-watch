## Github Watchdog

Github contributors monitoring service

## Installation:

```
python setup.py install
```

## Usage

### Create service config:

Config is stored in a yaml file, refer to config/monitor.yaml for example.

### Start the service:
```
github_watch [config_file]
```

## For Developers:

### Packaging the service (to install on other hosts):
```
python setup.py sdist
```

## Caveats

If the following errors occur, this is because the rate-limit to github api has been exceeded:
```
Listing contributors from https://api.github.com/repos/docker/swarm/contributors
Traceback (most recent call last):
  File "/Users/rembaba.cao/.virtualenvs/blippar/bin/github_watch", line 9, in <module>
    load_entry_point('github-watch==0.9.0', 'console_scripts', 'github_watch')()
  File "build/bdist.macosx-10.9-intel/egg/github_watch/monitor.py", line 173, in main
  File "build/bdist.macosx-10.9-intel/egg/github_watch/monitor.py", line 65, in __init__
  File "build/bdist.macosx-10.9-intel/egg/github_watch/monitor.py", line 49, in list_contributors
  File "build/bdist.macosx-10.9-intel/egg/github_watch/monitor.py", line 37, in _get
urllib2.URLError: <urlopen error Error getting API response>
```

This is because the rate limit has been exceeded:
```
curl https://api.github.com/repos/docker/swarm/contributors
{
  "message": "API rate limit exceeded for 73.189.183.60. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
  "documentation_url": "https://developer.github.com/v3/#rate-limiting"
}
```

To overcome this you need to set your auth_user and auth_token in the config yaml file:
Example:
```
github:
  owner: docker
  repo: swarm
  # these 2 are optional but will hit rate-limit if not set
  auth_user: rembaba
  auth_token: <user_token_here>
```
