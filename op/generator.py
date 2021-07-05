import os
from dataclasses import asdict

import jinja2

from op.config import Config


class Generator:
    def __init__(self, config: Config, templates_dir: str):
        self.config = config
        self.templates_dir = templates_dir

    def generate_everything(self):
        files = ['compose/base.yml', 'compose/tests.yml']
        files_names = {}
        for env in self.config.environments:
            files.append('compose/{}.yml'.format(env))
        if 'local' in self.config.environments:
            files.append('compose/debug.yml')

        if self.config.language == 'python':
            files.append('Dockerfile.python')
            files.append('Makefile.python')
            files_names['Dockerfile.python'] = 'Dockerfile'
            files_names['Makefile.python'] = 'Makefile'
        elif self.config.language == 'go':
            files.append('Dockerfile.go')
            files.append('Makefile.go')
            files_names['Dockerfile.go'] = 'Dockerfile'
            files_names['Makefile.go'] = 'Makefile'

        if self.config.database:
            files.append('db/Dockerfile')
            files.append('db/run.py')

        template_loader = jinja2.FileSystemLoader(searchpath=self.templates_dir)
        template_env = jinja2.Environment(loader=template_loader, autoescape=True, keep_trailing_newline=True)

        for file in files:
            template = template_env.get_template(file)
            dest_file = files_names.get(file, file)
            with open(dest_file, 'w') as f:
                f.write(template.render(asdict(self.config)))
