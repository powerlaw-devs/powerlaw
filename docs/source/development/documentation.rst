Documentation guidelines
------------------------


Tutorial pages
==============

Wherever possible, code included in tutorial pages should be self-contained
such that it can be directly copied by a user and run. The ``plot`` and
``exec_code`` directives are preferred over the generic ``code-block``, since
these are actually executed when compiling the documentation. For more
information, see:

- https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html
- https://sphinx-exec-code.readthedocs.io/en/stable/index.html 

For ``exec_code`` directives, it is a good idea to include the following
header, which will suppress any warnings (from powerlaw or otherwise)::

    # --- hide: start ---

    # Hide warnings from showing up.
    import warnings
    warnings.filterwarnings('ignore')

    # --- hide: stop ---

Similarly, if you want to look at the output of some quantity involving a fit
object, I think it is good to hide the progress bar so the output doesn't
look messy. That being said, so as to not distract from the content of the
example, you can display the Fit call without the verbose option while
running it with one like::

    # --- hide: start ---
    # This code will run, but not be displayed, the opposite of the block
    # below.
    fit = powerlaw.Fit(..., verbose=0) 
    # --- hide: stop ---

    # --- skip: start ---
    # This code will show up, but not actually be run.
    fit = powerlaw.Fit(...) 
    # --- skip: stop ---

    ...

A similar statement is included in the configuration option ``plot_pre_code``, 
giving the same effect for any ``plot`` directives.

Various global settings for matplotlib are set using the ``plot_rcparams``
variable; none of these affect the content of plots, but standardize the size/dpi/etc.
of the output figures.

You should set an appropriate caption and file name for any output figures
using the ``:caption:`` and ``:filename-prefix:`` options in ``plot`` directives.

For examples where the code itself isn't an important part, and you just
want to show a comparison between figures, you can use the ``:include-source: False``
option. This is still better than just including the image, since it will provide
a link to the source code for interested users.
