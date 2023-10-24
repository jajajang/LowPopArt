# LowPopArt

This is the code for the paper 'Efficient Low-Rank Matrix Estimation, Experimental Design, and Arm-Set-Dependent Low-Rank Bandits'

## Required software
 - python 3 with numpy, scipy, sklearn, cython, ipdb, cvxpy, tqdm, mosek
- Especially about mosek, you need an additional license file to actually use the package.

## Compile needed
 - in `matrixrecovery`, run `cython myutils_cython.pyx` and then `python3 setup.py install`
 - for mac
    - in `pyOptSpace_py3_custom`, run `cython optspace.pyx` then `python3 setup.py install`
    - copy the created `*.so` file to the upper directory
 - for linux
    - do the same as mac above, but in the directory `pyOptSpace_py3_linux_custom`

## To replicate the Figure 1 (left) in the paper
- Run 'Figure1_left_estimator_experi_easy.ipynb' in 'Figure 123'

## To replicate the Figure 1 (right) in the paper
- Run 'Figure1_right_estimator_experi_hard.ipynb' in 'Figure 123'

## To replicate the Figure 2 (left) in the paper
- Run 'Figure2_left_ETC_regret_analysis.ipynb' in 'Figure 123'

## To replicate the Figure 2 (right) in the paper (experiment data already run)
 - run `python3 analyze_expr01_230928_paper.py`

### To replicate the result in Figure 4
  1. Run the script ./running_script.sh
  2. Move all .pkl files to a subfolder in /res-20230928/R1_lambda_1/T100000 folder 
  3. remove all the date prefix on .pkl file name. For example, change the name '20230928Sun-123456-bmoracle.pkl' to 'bmoracle.pkl'
  4. Run `python3 analyze_expr01_230928_paper.py`


<!--
# License

This SDK is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0), see [LICENSE](./LICENSE) and [NOTICE](./NOTICE) for more information.
-->
