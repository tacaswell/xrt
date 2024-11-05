# -*- coding: utf-8 -*-
#
# xrt documentation build configuration file, created by
# sphinx-quickstart on Thu Mar 01 09:52:50 2012.

import matplotlib as mpl
mpl.use('agg')

import sys
import os
import shutil
import subprocess

on_rtd = os.environ.get('READTHEDOCS') == 'True'

autodoc_mock_imports = [
    'OpenGL', 'OpenGL.GL', 'OpenGL.GLU', 'OpenGL.GLUT',
    'OpenGL.arrays', 'pyopencl',
    'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
    'PyQt5.QtOpenGL', 'PyQt5.QtWebEngineWidgets', 'PyQt5.QtSql',
    'matplotlib.backends.backend_qt5agg',
    'PySide', 'PySide.QtCore',
    'spyder.widgets', 'spyderlib.widgets',
    'cv2', 'zmq']

__fdir__ = os.path.dirname(os.path.abspath(__file__))


def execute_shell_command(cmd, repo_dir):
    """Executes a shell command in a subprocess, waiting until it has completed.

    :param cmd: Command to execute.
    :param work_dir: Working directory path.
    """
    pipe = subprocess.Popen(cmd, shell=True, cwd=repo_dir,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    print(out, error)
    pipe.wait()


def git_clone(repo_url, repo_dir):
    cmd = 'git clone --depth 1 -b docres ' + repo_url + ' ' + repo_dir
    execute_shell_command(cmd, repo_dir)


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.
    https://stackoverflow.com/questions/2656322/
        shutil-rmtree-fails-on-windows-with-access-is-denied

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def load_res():
    if os.path.exists(os.path.join(__fdir__, "_images")):
        return  # already exists from the 1st run (rtfd has several runs)

    repo_dir = os.path.join(__fdir__, "tmp")
    while os.path.exists(repo_dir):
        repo_dir += "t"
    os.makedirs(repo_dir)

    repo_url = "https://github.com/kklmn/xrt.git"
    git_clone(repo_url, repo_dir)

    for dd in ["_images", "_videos", "_static", "_templates", "_themes"]:
        try:
            shutil.move(os.path.join(repo_dir, "doc", dd), __fdir__)
        except shutil.Error:
            pass
    for ff in os.listdir(os.path.join(repo_dir, "doc")):
        print(ff)
        if ff == 'conf.py':
            continue
        try:
            shutil.move(os.path.join(repo_dir, "doc", ff), __fdir__)
        except shutil.Error:
            pass

    shutil.rmtree(repo_dir, onerror=onerror)

# import Cloud
#import cloud_sptheme as csp

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, '..')
sys.path.insert(0, '.')
#sys.path.append('..')
sys.path.append(os.path.abspath('exts'))
#autodoc_mock_imports = ["PyQt5.QtWebKitWidgets"]

import xrt.backends.raycing.materials_elemental as xrtelem
import xrt.backends.raycing.materials_compounds as xrtcomp
import xrt.backends.raycing.materials_crystals as xrtxtal
import xrt.backends.raycing.pyTTE_x.elastic_tensors as xrtxelt


def sort_compounds(method):
    if method == 'density':
        res = sorted([(cname, getattr(xrtcomp, cname)().rho)
                      for cname in xrtcomp.__all__],
                     key=lambda mat: mat[1])
        return ['{0[0]} ({0[1]:.3g})'.format(tup) for tup in res]
    elif method == 'name':
        res = sorted([(cname, getattr(xrtcomp, cname)().name)
                      for cname in xrtcomp.__all__],
                     key=lambda mat: mat[1])
        return ['{0[0]} ({0[1]})'.format(tup) for tup in res]


def sort_crystals(method):
    elxs = xrtxelt.CRYSTALS
    if method == 'volume':
        res = sorted([(cname, getattr(xrtxtal, cname)().V)
                      for cname in xrtxtal.__all__],
                     key=lambda mat: mat[1])
        return ['{1}{0[0]}{1} ({0[1]:.4g})'.format(
            tup, '**' if tup[0] in elxs else '') for tup in res]


rst_epilog = """
.. |elemall| replace:: {0}
.. |compall| replace:: {1}
.. |xtalall| replace:: {2}
""".format(', '.join(xrtelem.__all__),
           ', '.join(sort_compounds('name')),
           ', '.join(sort_crystals('volume')))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
#extensions = ['sphinx.ext.autodoc', 'sphinx.ext.pngmath']
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.mathjax', 'sphinx_tabs.tabs',
              'animation',
              # 'sphinx_build_compatibility.extension'
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'xrt'
copyright = u'2014 Konstantin Klementiev, Roman Chernikov'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.6.0'
# The full version, including alpha/beta/rc tags.
release = '1.6.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'mytheme'
#html_theme = "cloud"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    # "rightsidebar": False,
    # "stickysidebar": True,
    # "collapsiblesidebar": True,
    # "max_width": 20,
    # "externalrefs": True,
    # "roottarget": "index"
    }

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ["./_themes"]
#html_theme_path = [csp.get_theme_dir()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_images/logo-xrt.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_images/xrt_logo.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
if on_rtd:
    # html_theme = 'default'
    # html_static_path = []
    # for keeping Download ZIP smaller:
    load_res()  # load doc resources from a dedicated branch
else:
    pass
#    html_theme = 'nature'

html_static_path = ['_static']
html_theme_options["body_min_width"] = '96%'

toc_object_entries = False

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'xrtdoc'
