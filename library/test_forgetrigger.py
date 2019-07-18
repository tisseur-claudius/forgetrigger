from library.forgetrigger import *
import pytest


@pytest.fixture(scope='module')
def forgeTags():
    pass


@pytest.fixture(scope='module')
def bpm_project():

    project = dict()
    project['name'] = 'bpm'
    project['app_services'] = list()
    project['app_services'].append({'service_name': 'bpm', 'thalesforge_url': 'forge_url'})
    project['gitlab_trigger_url'] = 'gitlab_trigger_url'
    project['gitlab_trigger_token'] = 'BPM_TOKEN'
    project['gitlab_trigger_ref'] = 'automation'

    return project


def test_project_name(bpm_project):
    assert Project(bpm_project).get_name() == 'bpm'
