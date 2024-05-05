# Natural Language Generator module
# using template from Mako

from mako.template import Template
from mako.lookup import TemplateLookup

class NaturalLanguageGeneration:

    def __init__(self, tpl_file_name, data_for_tpl):

        self.file_name = tpl_file_name
        self.tpl_data = data_for_tpl

    def view(self):

        the_template = Template(filename='konversa/templates/' + self.file_name)
        
        return the_template.render(**self.tpl_data)
