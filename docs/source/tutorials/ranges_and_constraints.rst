Parameter Ranges and Constraints
================================

When performing a fit to a probability distribution, you may want to
restrict the parameter space that must be explored for the fit.
``powerlaw`` provides two ways to do this: parameter ranges, which give
fixed bounds for parameter values, and constraints, which are relational
expressions between parameters.

Parameter ranges
----------------

If neither of these are provided, the fitting will be performed with no
constraints, and the default bounds for parameters defined in each
distribution's ``DEFAULT_PARAMETER_RANGES`` property.

.. code-block::

    import powerlaw

    data = powerlaw.load_test_dataset('blackouts')

    # Uses default parameter ranges
    pl = powerlaw.Fit(data)

For a power law, the default parameter ranges are:

.. exec_code::

    # --- hide: start ---

    # Hide warnings from showing up.
    import warnings
    warnings.filterwarnings('ignore')

    #hide:toggle

    import powerlaw

    print(powerlaw.Power_Law.DEFAULT_PARAMETER_RANGES)

If you want to manually set this parameter range, you can easily do so:

.. code-block::

    # Some data that has an exponent between 1 and 1.5
    data = ...

    pl = powerlaw.Fit(data, parameter_ranges={"alpha": [1, 1.5]})

You can do the same thing directly with a distribution class like ``powerlaw.Power_Law()``:

Of course, this parameter range will only apply to distributions that have
a parameter called ``"alpha"``; ``fit.exponential``, for example,
would be unaffected.

For a distribution with multiple parameters, the format is exactly the same:

.. code-block::

    tpl = powerlaw.Truncated_Power_Law(data,
                                       parameter_ranges={"alpha": [1, 1.5]}, "Lambda": [1e-1, 1e-2]})


Parameter constraints
---------------------

Let's say instead of using fixed bounds for these parameters, you wanted to
specify a relational constraint between them, for example, that ``Lambda``
is always less than ``alpha``. This can be accomplished by passing
constraint functions using the ``parameter_constraints`` keyword to either
``Fit`` or a ``Distribution`` object.

There are two or three parts to a constraint that
need to be defined in a dictionary that is eventually passed to the fitting:

1. The type of constraint you are imposing,

2. The function that implements this constraint, and

3. The distributions to which this constraint should apply (only required if
you want to restrict which distributions the constraint applies to).

These constraints are eventually passed to ``scipy.optimize.minimize``, so
you may find it helpful to read through
`their documentation <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html>`_
(the dictionary kind of constraints). That being said, there are a few
differences due to some wrapping and preprocessing done when setting
up constraints for fits here.

There are two types of constraints: equality ('eq') and inequality ('ineq').
Equality constraints will try to ensure that whatever function you
provide evaluates to zero, whereas inequality constraints will try to
keep that function at a non-zero, positive value.

An equality constraint might look something like this:

.. math::

    x_1 + x_2 = 5

And an inequality constraint might look something like this:

.. math::
    
    x_1 + x_2 \le 5

You might be tempted to implement this functions exactly as they are
above, for example:

.. exec_code::

    def constraint(x1, x2):
        return x1 + x2 == 5

This is incorrect; when defining constraints, you generally want to avoid
using boolean expressions like this, since it makes it very difficult for
the minimizer to figure out how to satisfy the constraint. Instead you
should set up this constraint like:

.. exec_code::

    def constraint(x1, x2):
        return 5 - x2 - x1

Now, even if the constraint isn't perfectly satisfied, the minimizer can at least tell
that ``(x1=2, x2=2)`` is closer to satisfying the constraint than ``(x1=987, x2=4210)``.

Let's move onto the actual functional form of constraints in ``powerlaw``,
and several examples. Your constraint function should take a single argument,
which will be the distribution object itself.  This way, you have full
access to all of the class variables, and all of the relevant information
in deciding if your fit is properly constrained. Note that this is different
from regular ``scipy.optimize.minimize`` constraints, and is achieved
by wrapping constraint functions within the ``Distribution`` class.

.. code-block::
    
    def constraint(dist):
        # Some computation with distribution properties/functions here...

As an example, let's assume that I want to create a constraint that requires
that I always have at least ``N`` points while trying to find the optimal
``xmin`` value. That is, I should constrain the ``xmin`` search to only
values that leave at least ``N`` points in the distribution domain. Note
that the same constraint that works for numerical fitting works for finding
the optimal ``xmin`` value since this is really just trying a bunch of fits.

This will be an inequality constraint, since I don't care if the number of
points is exactly ``N``, but just that it should be larger than
``N``. I would implement that as:

.. exec_code::

    def constraint(dist):
        # Some value
        N = 100
       
        # Note that dist.data property is already cropped from xmin to
        # xmax, so its length is a true measure of the points in the range.
        return len(dist.data) - N 

Now, when ``len(dist.data)`` is greater than ``N``, this will be some
positive value (allowed for inequality constraint), and otherwise will
be zero or negative (not allowed for inequality constraint).

Now I need to indicate the type of constraint ('ineq') and that this should
apply to all distributions:

.. code-block::

    constraint_dict = {"type": 'ineq',
                       "fun": constraint,
                       "dists": ['power_law']}

If I wanted this constraint to apply to all distributions, you can leave
out the ``"dists"`` entry in the dictionary. In fact, this is probably
a good example of a constraint that could apply to any distribution, 
since it only cares about the number of data points, but we'll leave
the specification just to show how it works.

Let's first try our ``xmin`` fitting without the constraint:

.. plot::
   :caption: Results of ``xmin`` fitting for the ``blackouts`` dataset.
   :filename-prefix: blackouts_xmin

    import powerlaw
    import matplotlib.pyplot as plt

    data = powerlaw.load_test_dataset('blackouts') / 1e3
    
    fit = powerlaw.Fit(data)

    plt.plot(fit.xmin_fitting_results["xmins"], fit.xmin_fitting_results["distances"], label='KS distance')
    plt.plot(fit.xmin_fitting_results["xmins"], fit.xmin_fitting_results["valid_fits"], label='Is valid fit')

    plt.axvline(fit.xmin, linestyle='--', c='black', label='Optimal $x_{min}$')

    plt.xlabel('$x_{min}$')
    plt.xscale('log')
    plt.legend()
    plt.show()

Now let's apply our constraint:

.. plot::
   :caption: Results of ``xmin`` fitting for the ``blackouts`` dataset with a constraint on the number of data points.
   :filename-prefix: blackouts_xmin_constrained

    import powerlaw
    import matplotlib.pyplot as plt

    data = powerlaw.load_test_dataset('blackouts') / 1e3
    
    def constraint(dist):
        N = 100
        return len(dist.data) - N

    constraint_dict = {"type": 'ineq',
                       "fun": constraint,
                       "dists": ['power_law']}

    fit = powerlaw.Fit(data, parameter_constraints=constraint_dict)

    plt.plot(fit.xmin_fitting_results["xmins"], fit.xmin_fitting_results["distances"], label='KS distance')
    plt.plot(fit.xmin_fitting_results["xmins"], fit.xmin_fitting_results["valid_fits"], label='Is valid fit')

    plt.axvline(fit.xmin, linestyle='--', c='black', label='Optimal $x_{min}$')

    plt.xlabel('$x_{min}$')
    plt.xscale('log')
    plt.legend()
    plt.show()

Indeed we see that the optimal ``xmin`` value is different, since the previous
one would have excluded too many data points to satisfy the constraint.

----

To demonstrate how else you might use constraints, below are a few more examples
of how you might achieve different goals:

.. code-block::

    def constraint(dist):
        """
        Require that the exponential scale is larger than the power law
        exponent (doesn't really make sense, but just to illustrate).
        """
        return dist.Lamda - dist.alpha

    # This should only apply to a truncated power law
    constraint_dict = {"type": 'ineq',
                       "fun": constraint,
                       "dists": ['truncated_power_law']}

    # Pass it to a fit
    fit = powerlaw.Fit(..., parameter_constraints=constraint_dict)

    # Or could directly pass it to a truncated power law
    tpl = powerlaw.Truncated_Power_Law(..., parameter_constraints=constraint_dict)


.. code-block::

    def constraint_1(dist):
        """
        Require that the number of points is greater than a specific value
        (so this is designed for xmin fitting).
        """
        return len(dist.data) - 1000

    # This constraint applies to all distributions
    constraint_dict_1 = {"type": 'ineq',
                         "fun": constraint_1}

    def constraint_2(dist):
        """
        Require that the ratio of beta to Lambda is a certain value
        (only applies to a stretched exponential).
        """
        return 10 - dist.Lambda / dist.beta

    # This constraint applies to only stretched exponentials
    constraint_dict_2 = {"type": 'eq',
                         "fun": constraint_2,
                         "dists": ['stretched_exponential']}


    all_constraints = [constraint_dict_1, constraint_dict_2]

    # Pass it to a fit
    fit = powerlaw.Fit(..., parameter_constraints=all_constraints)
