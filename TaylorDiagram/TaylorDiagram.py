import numpy as np
import pandas as pd
from typing import Union
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from warnings import filterwarnings
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa
filterwarnings('ignore')

class TaylorDiagram(object):
    def __init__(self, STD, fig=None, rect=111, label='plot', 
                 color_grid:str='black', linestyle_grid:str='--', 
                 linewidth_grid:float=0.1, grid_alpha:float=0.5,
                 fontfamily:str='serif', fontsize:int=10, 
                 fontweight:str='normal',
                 size_xlabel: int = 12,
                 weight_xlabel: str = 'normal',
                 fontfamily_xlabel: str ='Georgia',
                 positive_only:bool=False,
                 title: str = None,
                 corr_range = None,
                 ylabel:str = 'Correlation Coeficient',
                 xlabel:str='Standard Value'):
        
        self.STD = STD
        self.smin = 0.0
        self.smax = 1.5 * self.STD
        self.positive_only = positive_only
        self.corr_range = corr_range

        tr = PolarAxes.PolarTransform()
        
        def law_of_transform(corr_range):
            rlocs = np.linspace(corr_range[0], corr_range[1], 6)
            
            # Inversion of lawn:
            # angle = pi * (1 - corr)
            tlocs = np.pi * (1 - rlocs)
            # extremes angles
            angle_min = np.pi * (1 - corr_range[1])
            angle_max = np.pi * (1 - corr_range[0])
            return tlocs, (angle_min, angle_max, self.smin, self.smax), rlocs
        # def law_of_transform(corr_range):
        #     rlocs = np.linspace(corr_range[0], corr_range[1], 6)
            
        #     # Transformação não-linear para melhor distribuição
        #     # ângulo = (π/2) * (1 - correlação) / (1 - corr_range[0])
        #     scale = 1 - corr_range[0]  # 0.4 para (0.6,1)
        #     tlocs = (np.pi/2) * (1 - rlocs) / scale
            
        #     angle_min = 0  # corr=1.0
        #     angle_max = np.pi/2  # corr=0.6 → 90°
            
        #     return tlocs, (angle_min, angle_max, self.smin, self.smax), rlocs
        
        # define var to initialize
        rlocs, tlocs, extremes = None, None, None
        if positive_only:
            if corr_range is None:
                rlocs = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0])
                tlocs = np.arccos(rlocs)
                extremes = (0, np.pi/2, self.smin, self.smax)  
            else:
                tlocs, extremes, rlocs = law_of_transform(corr_range)
        else:
            if corr_range is None:
                self.smin = -0.01
                positive_rlocs = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99])
                negative_rlocs = np.array([-0.2, -0.4, -0.6, -0.8, -0.9, -0.95, -0.99, -1.0])
                rlocs = np.concatenate([negative_rlocs, positive_rlocs])
                tlocs = np.arccos(rlocs)
                extremes = (0, np.pi, self.smin, self.smax)
            else:
                tlocs, extremes, rlocs = law_of_transform(corr_range)
        
        if rlocs is None or tlocs is None or extremes is None:
            raise ValueError("Error in value of axis")
        gl1 = gf.FixedLocator(tlocs)
        tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, rlocs))))
        
        gh = fa.GridHelperCurveLinear(
            tr,
            extremes=extremes,
            grid_locator1=gl1,
            tick_formatter1=tf1
        )
        

        self.rlocs = rlocs
        self.tlocs = tlocs
        self.extremes = extremes
        self.gh = gh  # 
  
        ax = fa.FloatingSubplot(fig, rect, grid_helper=gh)
        fig.add_subplot(ax)
        
        # Config AXES
        ax.axis['right'].set_axis_direction('top')
        ax.axis['left'].set_axis_direction('bottom')
        ax.axis['top'].set_axis_direction('bottom')
        if positive_only:
            ax.axis['top'].toggle(ticklabels=True, label=True)
            ax.axis['bottom'].toggle(ticklabels=False, label=False)
            ax.axis['right'].toggle(ticklabels=True, label=True)
            ax.axis['left'].toggle(ticklabels=True,label=True)
            ## Y axis
            ax.axis['top'].label.set_text(ylabel)
            ax.axis['top'].label.set_pad(20)
            ax.axis['top'].label.set_rotation(180)
            ax.axis['top'].label.set_fontsize(size_xlabel)  
            ax.axis['top'].label.set_fontname(fontfamily_xlabel)
            ax.axis['top'].label.set_fontweight(weight_xlabel)
            ## X axis
            ax.axis['left'].label.set_text(xlabel)
            ax.axis['left'].label.set_fontweight(weight_xlabel)
            ax.axis['left'].label.set_fontsize(size_xlabel)  
            ax.axis['left'].label.set_fontname(fontfamily_xlabel)
            ax.axis['left'].label.set_fontweight(weight_xlabel)
            ## Direction of the texts
            ax.axis['right'].major_ticklabels.set_axis_direction('left')
            ax.axis['top'].major_ticklabels.set_axis_direction('top')
            ax.set_position([0.1, 0.1, 0.7, 0.7])

        else:
            for kind in ['top','right']: 
                ax.axis[kind].toggle(ticklabels=True, label=True)
            ax.axis['top'].set_axis_direction('bottom')
            ax.axis['top'].major_ticklabels.set_axis_direction('top')
            ax.axis['right'].major_ticklabels.set_axis_direction('bottom')
            ax.axis['bottom'].toggle(ticklabels=True, label=True)
            ax.axis['top'].label.set_text(xlabel)
            ax.axis['top'].label.set_fontsize(size_xlabel)  
            ax.axis['top'].label.set_fontname(fontfamily_xlabel)
            ax.axis['top'].label.set_fontweight(weight_xlabel)
            ax.axis['top'].label.set_pad(-460)
            ax.axis['top'].label.set_rotation(180)

        
        # Aplying config of font family
        kinds = ['top', 'bottom', 'right', 'left']
        for kind in kinds:
            ax.axis[kind].major_ticklabels.set_fontname(fontfamily)
            ax.axis[kind].major_ticklabels.set_fontsize(fontsize)
            ax.axis[kind].major_ticklabels.set_fontweight(fontweight)

        ax.grid(color=color_grid, linestyle=linestyle_grid, 
                linewidth=linewidth_grid, alpha=grid_alpha)
        
        self._ax = ax
        self.ax = ax.get_aux_axes(tr)
        
        if title:
            if positive_only:
                self._ax.set_title(title, fontfamily=fontfamily, 
                                fontsize=fontsize+2, fontweight='bold',
                                pad=20)
            else:
                self._ax.set_title(ylabel, fontfamily=fontfamily, 
                                fontsize=fontsize, fontweight='bold',
                                pad=20)
        
        l, = self.ax.plot([0], self.STD, 'k*', ls='', ms=8, label=label)

        if positive_only:
            t = np.linspace(0, np.pi/2, 200)
        else:
            t = np.linspace(0, np.pi, 200)
            
        r = np.zeros_like(t) + self.STD
        self.ax.plot(t, r, 'k--', label='_')
    
        self.samplePoints = [l]

    
    def add_sample(self, STD, r, *args, **kwargs):
        if self.positive_only and r < 0:
            print(f"Warning: The correlation and the r is negative (positive_only=True)")
            return None
        
        if hasattr(self, 'corr_range') and self.corr_range is not None:
            angle = np.pi * (1 - r)
            print("Warning These Function are Limited are 0.5 to 1.0!!")
        else:
            angle = np.arccos(r)
        l, = self.ax.plot(angle, STD, *args, **kwargs)
        self.samplePoints.append(l)
        return l


    def add_contours(self, levels=5, **kwargs):
        if hasattr(self, 'corr_range') and self.corr_range is not None:
            if self.positive_only:
                correlations = np.linspace(self.corr_range[0], self.corr_range[1], 100)
            else:
                correlations = np.linspace(-1, 1, 200)
            
            rs = np.linspace(self.smin, self.smax, 100)
            CORRS, RS = np.meshgrid(correlations, rs)
            
            RMSE = np.sqrt(
                np.power(self.STD, 2) + np.power(RS, 2) -
                (2.0 * self.STD * RS * CORRS)
            )
            ANGLES = np.pi * (1 - CORRS)
            contours = self.ax.contour(ANGLES, RS, RMSE, levels, **kwargs)
            
        else:
            if self.positive_only:
                ts = np.linspace(0, np.pi/2, 100)  # 0 a 90
            else:
                ts = np.linspace(0, np.pi, 100)    # 0 a 180

            rs = np.linspace(self.smin, self.smax, 100)
            RS, TS = np.meshgrid(rs, ts)
            RMSE = np.sqrt(
                np.power(self.STD, 2) + np.power(RS, 2) -
                (2.0 * self.STD * RS * np.cos(TS))
            )
            contours = self.ax.contour(TS, RS, RMSE, levels, **kwargs)

        # lines of RMSE
        if 'label' in kwargs:    
            proxy = Line2D([0], [0], 
                        linestyle=kwargs.get('linestyle', '--'),
                        color=kwargs.get('colors', kwargs.get('color', 'darkred')), 
                        linewidth=kwargs.get('linewidths', kwargs.get('linewidth', 0.7)),
                        label=kwargs['label'])
            self.samplePoints.append(proxy)
        return contours
                


def params_RMSE(diagram, colors='darkred', linewidths=0.7, label='RMSE', 
                linestyles='--', fontsize=10, inline=True):
    contours = diagram.add_contours(
        colors=colors, 
        linewidths=linewidths, 
        label=label,
        linestyles=linestyles
    )
    if inline:
        plt.clabel(contours, fontsize=fontsize)
    return contours

def PlotTaylorDiagram(obsSTD: Union[list[float], np.ndarray, pd.Series],
         std_val_model: Union[list[float], np.ndarray, pd.Series], 
         r_values: Union[list[float], np.ndarray, pd.Series], 
         name_models: Union[list[str], np.ndarray, pd.Series],
         corr_range,
         grid_params: dict = None, 
         font_params: dict = None,
         savefig: bool = False,
         name_fig: str='diagram.png',
         dpi: int=600,
         positive_only: bool = True,  # Forçando True para esta implementação
         title: str = None):
    
    '''
    Create a Taylor Diagram for model evaluation with interactive tooltips.
    
    Parameters:
    -----------
    obsSTD : float, list, np.ndarray, pd.Series
        Observed standard deviation (reference value)
        Standard deviation of the reference observational data
    
    std_val_model : list, np.ndarray, pd.Series
        Standard deviation values from models
        Model-predicted standard deviations to compare against observations
    
    r_values : list, np.ndarray, pd.Series
        Correlation coefficients between models and observations
        Pearson correlation coefficients (range: -1 to 1)
    
    name_models : list, np.ndarray, pd.Series
        Names of the models for legend identification
        Model identifiers for the legend
    
    grid_params : dict, optional
        Grid customization parameters
        Dictionary with keys:
          - color_grid: str (default: 'gray')
          - linestyle_grid: str (default: '-')
          - linewidth_grid: float (default: 0.6)
          - grid_alpha: float (default: 1)
    
    font_params : dict, optional
        Font customization parameters
        Dictionary with keys:
          - fontfamily: str (default: 'serif')
          - fontsize: int (default: 12)
          - fontweight: str (default: 'normal')
    
    savefig : bool, optional
        Whether to save the figure (default: False)
        Set to True to save the plot as image
    
    name_fig : str, optional
        Filename for saving the figure (default: 'diagram.png')
        Output filename when savefig=True
    
    dpi : int, optional
        DPI resolution for saved figure (default: 600)
        Image resolution quality
    
    positive_only : bool, optional
        Show only positive correlations (0 to 1) (default: False)
        If True, restricts display to positive correlation quadrant
    
    title : str, optional
        Plot title (default: None)
        Title text for the diagram
    
    '''
    s, r, l = std_val_model, r_values, name_models
    
    if positive_only: fig = plt.figure(figsize=(8, 6))  # For positive correlations 
    else: fig = plt.figure(figsize=(12, 8))  # For negative correlations 
    
    #  Default configuration for grid Params
    default_grid_params = {
        'color_grid': 'gray',
        'linestyle_grid': '-',
        'linewidth_grid': 0.6,
        'grid_alpha': 1
    }

    # Default configuration for font params
    default_font_params = {
        'fontfamily': 'Georgia',
        'fontsize': 12,
        'fontweight': 'normal',
        'size_xlabel': 12,
        'weight_xlabel':'normal',
        'fontfamily_xlabel':'Georgia'}
    
    # Mergin params from user
    if grid_params:
        default_grid_params.update(grid_params)
    if font_params:
        default_font_params.update(font_params)
    
    # Combine params from user
    all_params = {**default_grid_params, **default_font_params}
    all_params['positive_only'] = positive_only
    # Acessing class Taylor Diagram
    diagram = TaylorDiagram(obsSTD, fig=fig, rect=111, label='Observed', title=title,corr_range=corr_range,
                           **all_params)

    #Utils params From RMSE 
    params_RMSE(diagram=diagram,
    colors='darkred', 
    linewidths=0.8, 
    label='RMSE',
    linestyles='--',
    fontsize=10,
    inline=True)
    
    # Input the point into graphics 
    cs = plt.matplotlib.cm.Set1(np.linspace(0, 1, len(l)))
    srlc = zip(s, r, l, cs)
    for i in srlc:
        diagram.add_sample(i[0], i[1], label=i[2], c=i[3], marker='s')
    spl = [p.get_label() for p in diagram.samplePoints]
    
    # Legend Params
    fig.legend(
        diagram.samplePoints,
        spl,
        numpoints=1,
        prop=dict(size='medium', 
                 family=default_font_params['fontfamily'], 
                 weight=default_font_params['fontweight']),
        loc='center left',
        bbox_to_anchor=(0.9, 0.85) # multiple (0.82, 0.8)
    )
    
    plt.tight_layout(pad=0)
    if positive_only:
        plt.tight_layout(pad=0)
    else:
        plt.tight_layout(pad=-1)
    if savefig == True:
        plt.savefig(name_fig, dpi=dpi, bbox_inches='tight')
    return plt.show()