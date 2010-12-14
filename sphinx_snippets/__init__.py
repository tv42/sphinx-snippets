from docutils import nodes
import docutils.parsers.rst.directives
import sphinx.addnodes
import sphinx.util.compat

class snippets(docutils.nodes.Element):
    def __init__(self, pagename):
        self.pagename = None
        docutils.nodes.Element.__init__(self)

class Snippets(sphinx.util.compat.Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        (pagename,) = self.arguments
        s = snippets(pagename=pagename)
        return [
            s,
            ]

def _get_pages_under(env, pagename):
    toc = env.tocs[pagename]
    for toctree in toc.traverse(sphinx.addnodes.toctree):
        entries = toctree.attributes['entries']
        for (_, docname) in entries:
            yield docname
            for x in _get_pages_under(env, docname):
                yield x

def doctree_resolved(app, doctree, docname):
    env = app.builder.env

    for node in doctree.traverse(condition=snippets):
        l = []

        for page in _get_pages_under(env=app.env, pagename=docname):
            if page.endswith('/index'):
                continue
            # TODO avoid re-processing it
            doc = env.read_doc(page, save_parsed=False)
            for section in doc.traverse(nodes.section):
                l.append(section)

        l.reverse()
        node.replace_self(l)


def setup(Sphinx):
    Sphinx.add_directive('snippets', Snippets)
    Sphinx.connect('doctree-resolved', doctree_resolved)
