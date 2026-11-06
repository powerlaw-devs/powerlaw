powerlaw: A Python Package for Analysis of Heavy-Tailed Distributions
=====================================================================

.. image:: https://github.com/powerlaw-devs/powerlaw/workflows/Tests/badge.svg
   :target: https://github.com/powerlaw-devs/powerlaw/actions
   :alt: Tests

``powerlaw`` is a toolbox implementing the statistical methods developed in
`Clauset et al. 2007 <http://arxiv.org/abs/0706.1062>`_ and
`Klaus et al. 2011 <https://doi.org/10.1371/journal.pone.0019779>`_
to fit heavy-tailed distributions like power laws. Academics, please cite as:

Jeff Alstott, Ed Bullmore, Dietmar Plenz. (2014). powerlaw: a Python package
for analysis of heavy-tailed distributions.
`PLoS ONE 9(1): e85777 <https://doi.org/10.1371/journal.pone.0085777>`_
(also available at `arXiv:1305.0215 [physics.data-an] <http://arxiv.org/abs/1305.0215>`_)


Basic Usage
------------
The most basic use of this library is to fit some data, extract parameters,
and make comparisons to other distributions:

.. code-block:: python

    import powerlaw
    import numpy as np

    data = np.array([1.7, 3.2, 5.4, 2.1, 1.5, 2.8]) # data can be a list or a numpy array
    fit = powerlaw.Fit(data)

    print(fit.power_law.alpha)
    print(fit.power_law.xmin)

    R, p = fit.distribution_compare('power_law', 'lognormal')

You can also plot various results easily using ``matplotlib``:

.. code-block:: python

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    fit.plot_pdf(ax=ax, label='PDF')
    fit.power_law.plot_pdf(ax=ax, label='Power law fit')

    plt.legend()
    plt.show()


Quick Links
-----------
`API documentation, tutorials, and derivations <https://powerlaw-devs.github.io/powerlaw/>`__

`Original paper illustrating powerlaw's features, with figures <http://arxiv.org/abs/1305.0215>`__ *

`Code examples from manuscript, as an IPython Notebook <https://nbviewer.org/github/powerlaw-devs/powerlaw/blob/ee7dfc61d2683da01760f8fc692f11893c3038a1/manuscript/Manuscript_Code.ipynb>`__ *

\* The current version of powerlaw has changed slightly compared to the version that
was used in these resources. For the most up-to-date information and tutorials,
please see the documentation.


Installation
------------
The package can be installed from PyPi using pip:

.. code-block:: console

    $ pip install powerlaw

Alternatively, you can install directly from the source:

.. code-block:: console

    $ git clone https://github.com/powerlaw-devs/powerlaw
    $ cd powerlaw
    $ pip install .

This library depends on the usual scientific computing libraries that you
probably already have installed: ``numpy``, ``scipy``, ``matplotlib``, and
``mpmath``, as well as ``dill`` and ``h5py`` for caching objects and ``tqdm``
for creating progress bars.

The requirement of ``mpmath`` will be dropped if/when the scipy functions
``gamma``, ``gammainc`` and ``gammaincc`` are updated to have sufficient numerical
accuracy for negative numbers.


Development
-----------

To run the test suite, we recommend using pytest:

.. code-block:: console

    python -m pytest testing/ -v

The test suite includes comprehensive tests for distribution fitting, comparisons, and statistical validation using reference and synthetic datasets. All tests should pass successfully.

This repository uses GitHub Actions for continuous integration. Tests are automatically run on every push and pull request across multiple Python versions (3.8-3.12) and operating systems (Ubuntu, Windows, macOS). The CI status is shown in the badge above.

The original author of `powerlaw`, Jeff Alstott, is now only writing minor tweaks, but ``powerlaw`` remains open for further development by the community. If there's a feature you'd like to see in ``powerlaw`` you can `submit an issue <https://github.com/jeffalstott/powerlaw/issues>`_, but pull requests are even better. Offers for expansion or inclusion in other projects are welcomed and encouraged.


Mailing List
~~~~~~~~~~~~
Questions/discussions/help go on the Google Group `here <https://groups.google.com/g/powerlaw-general>`__. Also receives update info.


Acknowledgements
----------------
Many thanks to Andreas Klaus, Mika Rubinov and Shan Yu for helpful
discussions. Thanks also to Andreas Klaus,
`Aaron Clauset, Cosma Shalizi <https://aaronclauset.github.io/powerlaws/>`_,
and `Adam Ginsburg <https://github.com/keflavich/plfit>`_ for making
their code available. Their implementations were a critical starting point for
making ``powerlaw``.
