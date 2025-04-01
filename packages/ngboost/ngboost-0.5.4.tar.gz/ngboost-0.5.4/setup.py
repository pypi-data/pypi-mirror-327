# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ngboost', 'ngboost.distns']

package_data = \
{'': ['*']}

install_requires = \
['lifelines>=0.25',
 'numpy>=1.21.2',
 'scikit-learn>=1.0.2',
 'scipy>=1.7.2',
 'tqdm>=4.3']

setup_kwargs = {
    'name': 'ngboost',
    'version': '0.5.4',
    'description': 'Library for probabilistic predictions via gradient boosting.',
    'long_description': '# NGBoost: Natural Gradient Boosting for Probabilistic Prediction\n\n<h4 align="center">\n\n![Python package](https://github.com/stanfordmlgroup/ngboost/workflows/Python%20package/badge.svg)\n[![GitHub Repo Size](https://img.shields.io/github/repo-size/stanfordmlgroup/ngboost?label=Repo+Size)](https://github.com/stanfordmlgroup/ngboost/graphs/contributors)\n[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/ngboost?logo=pypi&logoColor=white)](https://pypi.org/project/ngboost)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/ngboost?logo=icloud&logoColor=white)](https://pypistats.org/packages/ngboost)\n\n</h4>\n\nngboost is a Python library that implements Natural Gradient Boosting, as described in ["NGBoost: Natural Gradient Boosting for Probabilistic Prediction"](https://stanfordmlgroup.github.io/projects/ngboost/). It is built on top of [Scikit-Learn](https://scikit-learn.org/stable/), and is designed to be scalable and modular with respect to choice of proper scoring rule, distribution, and base learner. A didactic introduction to the methodology underlying NGBoost is available in this [slide deck](https://docs.google.com/presentation/d/1Tn23Su0ygR6z11jy3xVNiLGv0ggiUQue/edit?usp=share_link&ouid=102290675300480810195&rtpof=true&sd=true).\n\n## Installation\n\n```sh\nvia pip\n\npip install --upgrade ngboost\n\nvia conda-forge\n\nconda install -c conda-forge ngboost\n```\n\n## Usage\n\nProbabilistic regression example on the Boston housing dataset:\n\n```python\nfrom ngboost import NGBRegressor\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error\n\n#Load Boston housing dataset\ndata_url = "http://lib.stat.cmu.edu/datasets/boston"\nraw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)\nX = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])\nY = raw_df.values[1::2, 2]\n\nX_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)\n\nngb = NGBRegressor().fit(X_train, Y_train)\nY_preds = ngb.predict(X_test)\nY_dists = ngb.pred_dist(X_test)\n\n# test Mean Squared Error\ntest_MSE = mean_squared_error(Y_preds, Y_test)\nprint(\'Test MSE\', test_MSE)\n\n# test Negative Log Likelihood\ntest_NLL = -Y_dists.logpdf(Y_test).mean()\nprint(\'Test NLL\', test_NLL)\n```\n\nDetails on available distributions, scoring rules, learners, tuning, and model interpretation are available in our [user guide](https://stanfordmlgroup.github.io/ngboost/intro.html), which also includes numerous usage examples and information on how to add new distributions or scores to NGBoost.\n\n## License\n\n[Apache License 2.0](https://github.com/stanfordmlgroup/ngboost/blob/master/LICENSE).\n\n## Reference\n\nTony Duan, Anand Avati, Daisy Yi Ding, Khanh K. Thai, Sanjay Basu, Andrew Y. Ng, Alejandro Schuler. 2019.\nNGBoost: Natural Gradient Boosting for Probabilistic Prediction.\n[arXiv](https://arxiv.org/abs/1910.03225)\n',
    'author': 'Stanford ML Group',
    'author_email': 'avati@cs.stanford.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stanfordmlgroup/ngboost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
