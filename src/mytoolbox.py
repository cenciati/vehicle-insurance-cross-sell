'''
Author: Gabriel Cenciati
LinkedIn: https://www.linkedin.com/in/cenciati/
GitHub: https://github.com/cenciati/
'''

# data manipulation
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# data visualization
from matplotlib import pyplot as plt

# other
import warnings

class MyToolBox:
    def __init__(self):
        pass
    
    
    def jupyter_settings(self, figsize=(24, 12), fontsize=12, filterwarnings=False):
        '''Set jupyter notebook settings.

        Parameters
        ----------
        figsize : tuple, default=(24, 12)
            Size of the figure.
        fontsize : int, default=12
            Font size of the labels.
        filterwarnings : boolean, default=False
            Defines whether warnings will be displayed during the project.
        
        Returns
        -------
        None
        '''
        # pandas settings
        pd.options.display.max_columns = None
        pd.options.display.max_rows = 40
        pd.options.display.float_format = '{:.4f}'.format
        
        # numpy settings
        np.random.seed(42)
        np.set_printoptions(precision=3)
        
        # matplotlib settings
        plt.rc('figure', figsize=figsize)
        plt.rc('font', size=fontsize)
        
        # warnings settings
        if filterwarnings:
            warnings.filterwarnings('ignore')
        
        # message
        print('Jupyter settings set.')

        return None
    
    
    def cramers_v(self, x, y):
        '''Calculates the Cramer's V correlation between two variables.

        Parameters
        ----------
        x : pandas series
            First variable.
        y : pandas series
            Second variable.
        
        Returns
        -------
        Cramer's V correlation
        '''
        # confusion matrix
        cm = pd.crosstab(x, y).to_numpy()
        
        # formula
        n = cm.sum()
        r, k = cm.shape
        chi2 = chi2_contingency(cm)[0]
        
        # bias correction
        chi2corr = max(0, chi2 - (k-1)*(r-1) / (n-1))
        kcorr = k - (k-1)**2 / (n-1)
        rcorr = r - (r-1)**2 / (n-1)
        
        return np.sqrt((chi2corr / n) / (min(kcorr-1, rcorr-1)))
