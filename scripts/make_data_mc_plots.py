#!/usr/bin/env python

from root_pandas import read_root
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
plt.style.use('classic')
plt.rc('figure', facecolor='w', figsize=(10,10))
plt.rc('axes', labelsize=36)
plt.rc('axes', titlesize=24)
import itertools

def make_data_mc_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_feature, period, do_ratio=True, cat='all'):

    if do_ratio:
        fig, axes = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[3,1]})
        fig.subplots_adjust(hspace=0)
        ax= axes[0]
    else:
        fig, ax = plt.subplots(1, 1)

    labels = []
    colors = []
    stack_data = []
    stack_weights = []
    overlay_data = []
    overlay_weights = []
    for i, dataset_name in enumerate(dataset_list):
        #if dataset_name[:3] == 'hzg':
        #    continue
        #datasets[i].query('leptonOneFlavor != leptonTwoFlavor', inplace=True)

        if dataset_name == 'signal' or dataset_name[:3] == 'hzg':
            #labels.append(lut_datasets.loc[dataset_name].text)
            #colors.append(lut_datasets.loc[dataset_name].color)
            #overlay_data.append(datasets[i][feature])
            #overlay_weights.append(datasets[i]['eventWeight']*datasets[i]['genWeight']*datasets[i]['mc_sf']*datasets[i]['pt_weight'])
            #overlay_data = datasets[i][feature]
            #overlay_weights = datasets[i]['eventWeight']*datasets[i]['genWeight']*datasets[i]['mc_sf']*datasets[i]['pt_weight']
            overlay_data.append(datasets[i][feature])
            scale_factor = 1.
            if dataset_name == 'signal':
                scale_factor = 100.
            else:
                scale_factor = 5000.
            overlay_weights.append(scale_factor*datasets[i]['eventWeight']*datasets[i]['genWeight']*datasets[i]['mc_sf']*datasets[i]['pt_weight'])

        elif dataset_name != 'data':
            labels.append(lut_datasets.loc[dataset_name].text)
            colors.append(lut_datasets.loc[dataset_name].color)
            stack_data.append(datasets[i][feature])
            stack_weights.append(datasets[i]['eventWeight']*datasets[i]['genWeight']*datasets[i]['mc_sf']*datasets[i]['pt_weight'])
            print(f'n_bg = {np.sum(datasets[i].puWeight*datasets[i].prefWeight*datasets[i].leptonOneRecoIDWeight*datasets[i].leptonTwoRecoIDWeight*datasets[i].genWeight*datasets[i].triggerWeight*datasets[i].mc_sf)}')
        else:
            y, bins = np.histogram(datasets[i][feature], bins=int(lut_feature.n_bins), range=[lut_feature.xmin, lut_feature.xmax])
            x = (bins[1:] + bins[:-1])/2.
            yerr = np.sqrt(y)
            print(f'n_data = {datasets[i].shape[0]}')
   
    stack, bins, p = ax.hist(stack_data,
                             bins       = int(lut_feature.n_bins),
                             range     = [lut_feature.xmin, lut_feature.xmax],
                             color     = colors,
                             alpha     = 1.,
                             linewidth = 0.5,
                             stacked   = True,
                             histtype  = 'stepfilled',
                             weights   = stack_weights,
                             label = labels
                            )

    stack_noscale = np.histogram(np.concatenate(stack_data),
                                 bins = int(lut_feature.n_bins),
                                 range = [lut_feature.xmin, lut_feature.xmax],
                                 weights = np.concatenate(stack_weights)**2
                                 )[0]

    stack_sum = stack[-1] if len(stack_data) > 1 else stack
    stack_x = (bins[1:] + bins[:-1])/2.
    stack_err = np.sqrt(stack_noscale)
    

    no_blanks = stack_sum > 0
    stack_sum, stack_x, stack_err = stack_sum[no_blanks], stack_x[no_blanks], stack_err[no_blanks]
    if do_ratio:
        denominator = (stack_x, stack_sum, stack_err)
    ax.errorbar(stack_x, stack_sum, yerr=stack_err,
                fmt = 'none', 
                ecolor = 'k', 
                capsize = 0,
                elinewidth = 10,
                alpha = 0.15
                )
   
    x, y, yerr = x[no_blanks], y[no_blanks], yerr[no_blanks]
    ax.errorbar(x, y, yerr=yerr, fmt='ko', capsize=9, elinewidth=2, label='data')

    ax.hist(overlay_data,
            bins = int(lut_feature.n_bins),
            range = [lut_feature.xmin, lut_feature.xmax],
            color = 'b', 
            #color = ['b', 'brown'], 
            alpha = 1., 
            linewidth = 2., 
            histtype = 'step', 
            weights = overlay_weights,
            stacked = False,
            label = 'signal x 100'
            #label = ['signal x 1000', 'VBF signal x 5000']
            )

    ax.grid()

    if feature == 'transformed_vbf_bdt':
        ax.set_yscale('log')
        ax.axvline(0.3, color='k', linestyle='--', linewidth=2)
        ax.axvline(0.5, color='k', linestyle='--', linewidth=2)
    
    if feature == 'transformed_kin_bdt':
        ax.set_yscale('log')  

    if do_ratio:
        numerator = (x, y, yerr)
        axes[1].set_xlabel(r'$\sf {0}$'.format(lut_feature.x_label))
        axes[1].set_ylabel(r'Data/MC')
        #axes[1].set_ylim((0.5, 1.5))
        axes[1].set_ylim((0., 2.))
        axes[1].set_yticks(np.arange(0., 2., 0.5))
        axes[1].grid()
        axes[1].set_yticks(np.arange(0., 2., 0.1), minor=True)
        axes[1].tick_params(axis='y', length=10, width=1, direction='in')
        axes[1].tick_params(axis='y', length=3, width=1, direction='in', which='minor')

        box = axes[1].get_position()
        axes[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])

        ### calculate ratios 
        mask = (numerator[1] > 0) & (denominator[1] > 0)

        ratio = numerator[1][mask]/denominator[1][mask]
        error = ratio*np.sqrt(numerator[2][mask]**2/numerator[1][mask]**2 + denominator[2][mask]**2/denominator[1][mask]**2)
        axes[1].errorbar(numerator[0][mask], ratio, yerr=error,
                         fmt = 'ko',
                         capsize = 0,
                         elinewidth = 2
                        )
        axes[1].plot([lut_feature.xmin, lut_feature.xmax], [1., 1.], 'r--')
    else: 
        ax.set_xlabel(r'$\sf {0}$'.format(lut_feature.x_label))
  
    ax.set_xlim(lut_feature.xmin, lut_feature.xmax);
    ax.set_ylim(0, ymax=ax.get_ylim()[1]*1.2);
    ax.set_ylabel(r'$\sf {0}$'.format(lut_feature.y_label))
    ax.legend();
    plt.tight_layout();
    plt.savefig('plots/data-mc/signal_overlay/{0}/{1}/{2}/{0}_{1}_{2}_{3}'.format(period, channel, cat, feature), dpi=500);
    plt.close();


def make_sig_bg_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_feature, cat='all'):

    fig, ax = plt.subplots(1, 1)

    labels = []
    colors = []
    stack_data = []
    stack_weights = []
    for i, dataset_name in enumerate(dataset_list):
        if dataset_name == 'data':
            continue
        else:
            labels.append(lut_datasets.loc[dataset_name].text)
            colors.append(lut_datasets.loc[dataset_name].color)
            stack_data.append(datasets[i][feature])
            stack_weights.append(datasets[i]['eventWeight']*datasets[i]['genWeight']*datasets[i]['mc_sf'])
   
    stack, bins, p = ax.hist(stack_data,
                             bins       = int(lut_feature.n_bins),
                             range     = [lut_feature.xmin, lut_feature.xmax],
                             color     = colors,
                             #alpha     = 1.,
                             alpha     = 0.5,
                             linewidth = 0.5,
                             #stacked   = True,
                             stacked   = False,
                             histtype  = 'stepfilled',
                             weights   = stack_weights,
                             density = True,
                             label = labels
                            )

    ax.set_xlabel(r'$\sf {0}$'.format(lut_feature.x_label))
  
    ax.set_xlim(lut_feature.xmin, lut_feature.xmax);
    ax.set_ylim(0, ymax=ax.get_ylim()[1]*1.2);
    ax.set_ylabel(r'$\sf {0}$'.format(lut_feature.y_label))
    ax.legend();
    plt.tight_layout();
    plt.savefig('plots/sig-bg/{0}/{1}/{0}_{1}_{2}'.format(channel, cat, feature), dpi=500);
    plt.close();
 
if __name__ == '__main__':
    
    periods = [2016, 2017, 2018]

    channels = ['mmg', 'eeg']
    #channels = ['llg']
    mc_16 = ['zjets_M50_2016', 'zg_llg_2016'] 
    mc_17 = ['zjets_M50_2017', 'zg_llg_2017'] 
    mc_18 = ['zjets_M50_2018', 'zg_llg_2018']

    #signal_16 = ['hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016']
    signal_16 = ['hzg_gluglu_M125_2016', 'hzg_vbf_M125_2016']
    signal_17 = ['hzg_gluglu_M125_2017', 'hzg_tth_M125_2017', 'hzg_vbf_M125_2017', 'hzg_wplush_M125_2017', 'hzg_wminush_M125_2017', 'hzg_zh_M125_2017']
    signal_18 = ['hzg_gluglu_M125_2018', 'hzg_tth_M125_2018', 'hzg_vbf_M125_2018', 'hzg_wplush_M125_2018', 'hzg_wminush_M125_2018', 'hzg_zh_M125_2018']

    data_16 = {'mmg': ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 'muon_2016F', 'muon_2016G', 'muon_2016H'],
               'eeg': ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 'electron_2016F', 'electron_2016G', 'electron_2016H']}
    data_16['llg'] = data_16['mmg'] + data_16['eeg']

    data_17 = {'mmg': ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F'],
               'eeg': ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F']}
    data_17['llg'] = data_17['mmg'] + data_17['eeg']
    data_18 = {'mmg': ['muon_2018A', 'muon_2018B', 'muon_2018C', 'muon_2018D'],
               'eeg': ['electron_2018A', 'electron_2018B', 'electron_2018C', 'electron_2018D']}
    data_18['llg'] = data_18['mmg'] + data_18['eeg']

    data = {2016: data_16, 2017: data_17, 2018: data_18}

    signal = {2016: signal_16, 2017: signal_17, 2018: signal_18}
    
    dataset_dict = {2016: {'mmg': mc_16 + ['data'] + ['signal'], 'eeg': mc_16 + ['data'] + ['signal'], 
                           'llg': mc_16 + ['data'] + ['signal'] + ['hzg_vbf_M125_2016']},
                    2017: {'mmg': mc_17 + ['data'] + ['signal'], 'eeg': mc_17 + ['data'] + ['signal'], 
                           'llg': mc_17 + ['data'] + ['signal'] + ['hzg_vbf_M125_2017']},
                    2018: {'mmg': mc_18 + ['data'] + ['signal'], 'eeg': mc_18 + ['data'] + ['signal'], 
                           'llg': mc_18 + ['data'] + ['signal'] + ['hzg_vbf_M125_2018']}}

    for period, channel in itertools.product(periods, channels):
        datasets = []
        dataset_list = dataset_dict[period][channel]
        for dataset in tqdm(dataset_list):
            print(dataset)
            if dataset == 'data':
                data_df_list = []
                for entry in data[period][channel]:
                    if channel == 'llg':
                        data_df_list.append(read_root('data/step3_vbf_bdt/output_combined_{0}.root'.format(period), '{0}'.format(entry)).astype('float'))
                    else:
                        data_df_list.append(read_root('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period), '{0}'.format(entry)).astype('float'))
                data_df = pd.concat(data_df_list)
                datasets.append(data_df)
            elif dataset == 'signal':
                signal_df_list = []
                for entry in signal[period]:
                    if channel == 'llg':
                        signal_df_list.append(read_root('data/step3_vbf_bdt/output_combined_{0}.root'.format(period), '{0}'.format(entry)).astype('float'))
                    else:
                        signal_df_list.append(read_root('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period), '{0}'.format(entry)).astype('float'))
                signal_df = pd.concat(signal_df_list)
                datasets.append(signal_df)
            else:
                if channel == 'llg':
                    datasets.append(read_root('data/step3_vbf_bdt/output_combined_{0}.root'.format(period), '{0}'.format(dataset)).astype('float'))
                else:
                    datasets.append(read_root('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period), '{0}'.format(dataset)).astype('float'))
        
        lut_datasets = pd.read_excel('data/plotting_lut.xlsx', sheet_name='datasets_{0}'.format(period), index_col='dataset_name').dropna(how='all')
        lut_features = pd.read_excel('data/plotting_lut.xlsx', sheet_name='variables_{0}'.format(channel),index_col='variable_name').dropna(how='all')
        #f_list = lut_features.index.values
        f_list = ['corrPhotonMVA']

        for feature in f_list:
            make_data_mc_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_features.loc[feature], period)
            #make_sig_bg_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_features.loc[feature])

  
    #category_scheme = 'optimal'
    #if category_scheme == 'nominal':
    #    #categories = ['lepton', 'dijet', 'boosted', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
    #    categories = ['dijet', 'boosted', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']

    #elif category_scheme == 'optimal':
    #    #categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
    #    categories = ['dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
    #
    ## category plots
    #for channel in channels:
    #    for cat in categories:
    #        datasets = []
    #        dataset_list = dataset_dict[channel]
    #        for dataset in tqdm(dataset_list):
    #            if dataset == 'data':
    #                data_df_list = []
    #                for entry in data[channel]:
    #                    data_df_list.append(read_root('data/step4_cats/output_{0}_2016_yields.root'.format(channel), '{0}_{1}'.format(entry, cat)).astype('float'))
    #                data_df = pd.concat(data_df_list)
    #                datasets.append(data_df)
    #            else:
    #                datasets.append(read_root('data/step4_cats/output_{0}_2016_yields.root'.format(channel), '{0}_{1}'.format(dataset, cat)).astype('float'))
    #    
    #        lut_datasets = pd.read_excel('data/plotting_lut.xlsx', sheet_name='datasets_2016', index_col='dataset_name').dropna(how='all')
    #        lut_features = pd.read_excel('data/plotting_lut.xlsx', sheet_name='variables_{0}'.format(channel),index_col='variable_name').dropna(how='all')

    #        f_list = ['zgLittleThetaMY', 'zgBigThetaMY', 'dileptonM', 'llgM', 'llgMKin', 'dileptonMKin', 'photonOnePt', 'photonOneMVA']

    #        for feature in f_list:
    #            make_data_mc_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_features.loc[feature], cat=cat)
    #            make_sig_bg_plot(dataset_list, datasets, feature, channel, lut_datasets, lut_features.loc[feature], cat=cat)

