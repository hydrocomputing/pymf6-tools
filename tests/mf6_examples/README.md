# Run all MODFLOW 6 examples

Run all models from [modflow6-examples](https://github.com/MODFLOW-ORG/modflow6-examples) with:

* MODFLOW 6 (MF6) - ground truth

and with BMI-based runners:

* xmipy
* modflowapi
* pymf6

Each of them is run with and without solution loop.

**`with solution loop`**

Do iterations for solving directly:

```python
yield sim_grp, States.iteration_start
has_converged = mf6.solve(sol_id)
yield sim_grp, States.iteration_end
```

**`without solution loop`**

Do only higher level time steps:

```python
yield sim, States.timestep_start
mf6.do_time_step()
yield sim, States.timestep_end
```

Iterations are done internally.
