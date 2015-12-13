from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks, utils


def create_playbook(playbook_file, host, username, password, private_key_file,
                    sudo_password, verbosity_level=0):
    """Create an ansible playbook
    """
    inventory = Inventory(host_list=[host])

    stats=callbacks.AggregateStats()

    playbook = PlayBook(
            playbook_file,
            runner_callbacks=callbacks.PlaybookRunnerCallbacks(
                callbacks.AggregateStats(),
                verbose=verbose),
            callbacks=callbacks.PlaybookCallbacks(verbose=VERBOSE),
            stats=stats,
            inventory=inventory,
            remote_user=username,
            remote_pass=password,
            private_key_file=private_key_file,
            become_pass=sudo_password,
    )
    utils.VERBOSITY = verbosity_level

    return playbook, stats

def main():
    """Run ansible playbook
    """
    playbook_file = 'playbook.yml'
    host = "172.16.7.143"
    username = "root"
    password = "pass123"
    private_key_file = "~/.ssh/id_rsa"
    sudo_password = "pass123"
    playbook, stats = create_playbook(playbook_file,
                                      host=host,
                                      username=username,
                                      password=password,
                                      private_key_file=private_key_file,
                                      sudo_password=sudo_password,
                                      verbosity_level=0)
    return playbook.run()


if __name__ == '__main__':
    main()
