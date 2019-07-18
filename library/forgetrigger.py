#!/usr/bin/python

from ansible.module_utils.basic import *
#import git

class Tag:

    valid = True
    version_str = '0.0'
    env_str = 'AUT'
    pattern = '^.*/tags/(?P<version>\\d+(?:.\\d+)*)(?:_(?P<env>AUT|INT|UAT))*$'

    ENVS = {'AUT': 0, 'INT': 1, 'UAT': 2}

    def __init__(self, tagStr):
        pass

    def initWithGitTag(self, tag):
        self.tag = tag
        p = re.compile(self.pattern)
        m = p.match(self.tag)

        if m:
            if m.group('version'):
                self.setVersion(m.group('version'))

            if m.group('env'):
                self.setEnv(m.group('env'))
        else:
            self.valid = False


class Service:

    def __init__(self):
        pass


class Project:

    def __init__(self, project):
        print(project)
        self.name = project['name']
        self.services_ref = dict()
        self.services_new = dict()
        self.gitlab_trigger_url = project['gitlab_trigger_url']
        self.gitlab_trigger_token = project['gitlab_trigger_token']
        self.gitlab_trigger_branch = project['gitlab_trigger_ref']

    def set_services(self):
        self.last_tags = self.get_tags_from_forge(project['app_services'])

    def get_tags_from_forge(self, services):

        service_dict = dict()

        for service in services:
            service_name = service['service_name']
            url = service['thalesforge_url']

            git_object = git.cmd.Git()
            result = git_object.ls_remote(url).split('\n')

            last_tag = Tag()

            for ref in result:
                tag = Tag()
                tag.initWithGitTag(ref)

                if tag > last_tag:
                    last_tag = tag

            service_dict[service_name] = {
                'env': last_tag.getEnv(),
                'version': last_tag.getVersion()
            }

        return service_dict

    def get_services(self):
        return self.services

    def get_name(self):
        return self.name


class ForgeTrigger:

    def main(self):

        fields = {
            "projects": {"required": True, "type": "list"}
        }

        module = AnsibleModule(argument_spec=fields)

        debug = list()
        for project_vars in module.params['projects']:
            p = Project(project_vars)
            debug.append(p.name)

        response = {
            'projects': debug
        }
        module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    ForgeTrigger().main()
