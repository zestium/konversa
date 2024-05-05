# Natural Language Generator module
# using template from Mako

from mako.template import Template
from mako.lookup import TemplateLookup

nlg_template_dir = TemplateLookup(directories=['templates/'])

class NaturalLanguageGeneration:

    def __init__(self, tpl_file_name, data_for_tpl):

        self.file_name = tpl_file_name
        self.tpl_data = data_for_tpl

    def view(self):

        the_template = Template(filename=self.file_name, lookup=nlg_template_dir)
        
        return the_template.render(item_description=self.tpl_data)
