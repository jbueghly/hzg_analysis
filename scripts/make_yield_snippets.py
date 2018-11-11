#!/usr/bin/env python
import pandas as pd
import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
from root_pandas import read_root

channels = ['mumug', 'elelg']
#datasets = ['hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
muon_data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
             'muon_2016F', 'muon_2016G', 'muon_2016H']
electron_data = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                 'electron_2016F', 'electron_2016G', 'electron_2016H']
data_dict = {'mumug': mc + muon_data, 'elelg': mc + electron_data}
#categories = ['dijet', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
categories = ['dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
#categories = ['dijet_1', 'dijet_2', 'untagged_11', 'untagged_12', 'untagged_21', 'untagged_22', 'untagged_3', 'untagged_4']
#cat_num = [5, 1, 2, 3, 4]
cat_num = [51, 52, 1, 2, 3, 4]
#cat_num = [51, 52, 11, 12, 21, 22, 3, 4]

if __name__ == '__main__':

    for channel in channels:
        yield_dict = {}
        for dataset in data_dict[channel]:
            for cat in categories:
                #if channel == 'elelg' and cat == 'dijet_1':
                #    if dataset == 'hzg_zh' or dataset == 'hzg_tth':
                #        yield_dict['{0}_{1}'.format(dataset, cat)] = 0.
                #        continue
                #df = read_root('data/step4_cats/output_{0}_2016_yields.root'.format(channel), '{0}_{1}'.format(dataset, cat))
                df = read_root('data/step4_cats_new/output_{0}_2016_yields.root'.format(channel), '{0}_{1}'.format(dataset, cat)).astype('float')
                df.query('115. < three_body_mass < 170.', inplace=True)
                yield_dict['{0}_{1}'.format(dataset, cat)] = np.sum(df.eventWeight) 
                
            df = read_root('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel), '{0}'.format(dataset)).astype('float')
            #df.query('115. < three_body_mass < 170.', inplace=True)

            if dataset in yield_dict:
                yield_dict['{0}'.format(dataset)] += np.sum(df.eventWeight*df.genWeight)
            else:
                yield_dict['{0}'.format(dataset)] = np.sum(df.eventWeight*df.genWeight)

            if dataset in muon_data:
                if 'mumug_total' in yield_dict:
                    yield_dict['mumug_total'] += np.sum(df.eventWeight*df.genWeight)
                else:
                    yield_dict['mumug_total'] = np.sum(df.eventWeight*df.genWeight)
            
            elif dataset in electron_data:
                if 'elelg_total' in yield_dict:
                    yield_dict['elelg_total'] += np.sum(df.eventWeight*df.genWeight)
                else:
                    yield_dict['elelg_total'] = np.sum(df.eventWeight*df.genWeight)

            elif dataset[0] == 'z':
                if 'background' in yield_dict:
                    yield_dict['background'] += np.sum(df.eventWeight*df.genWeight)
                else:
                    yield_dict['background'] = np.sum(df.eventWeight*df.genWeight)
        # make datacard snippets
        for i, cat in enumerate(categories):
            num = cat_num[i]
            #snippet = f'bin     {cat}       {cat}       {cat}       {cat}       {cat}       {cat}\n'
            snippet = 'bin     cat{0}       cat{0}      cat{0}       cat{0}       cat{0}      cat{0}\n'.format(num)
            snippet += 'process     ttH_hzg     ZH_hzg      WH_hzg      qqH_hzg     ggH_hzg     bgr\n'
            snippet += 'process     -4      -3      -2      -1      0       1\n'
            snippet += 'rate '
            snippet += '{0:.6f}     '.format(yield_dict['hzg_tth_{0}'.format(cat)])
            snippet += '{0:.6f}     '.format(yield_dict['hzg_zh_{0}'.format(cat)])
            snippet += '{0:.6f}     '.format(yield_dict['hzg_wh_{0}'.format(cat)])
            snippet += '{0:.6f}     '.format(yield_dict['hzg_vbf_{0}'.format(cat)])
            snippet += '{0:.6f}     '.format(yield_dict['hzg_gluglu_{0}'.format(cat)])
           # for proc in signal_labels:
           #     yield_val = table[f'condition_{i+1}'].loc[proc]
           #     snippet += '{0:.6f}     '.format(yield_val)
            snippet += '1.000000\n'
            snippet += '-------------------------------------------------------------\n'
            #text_file = open('signal_yields/{0}_{1}.txt'.format(channel, cat), 'w')
            text_file = open('signal_yields_new/{0}_{1}.txt'.format(channel, cat), 'w')
            text_file.write(snippet)
            text_file.close()

        text_file = open('yields/{0}.txt'.format(channel), 'w')
        for dataset in data_dict[channel]:
            snippet = '{0}: {1}\n'.format(dataset, yield_dict[dataset])
            text_file.write(snippet)
        text_file.write('{0} data: {1}\n'.format(channel, yield_dict['{0}_total'.format(channel)]))
        text_file.write('{0} background: {1}\n'.format(channel, yield_dict['background']))
        text_file.close()


            

   # # make html tables for slides
   # taiwan_yields = pd.read_csv('data/taiwan_yields.csv')
   # for i, cat in enumerate(categories):
   #     html = ''
   #     html += '<div class="sl-block" data-block-type="table" data-block-id="57e1dca4d04ea986795954abbc584db3" style="height: auto; min-width: 120px; min-height: 30px; width: 887px; left: 37px; top: 140px;">\n'
   #     html += '<div class="sl-block-content" style="z-index: 12;" data-table-rows="3" data-table-cols="7" data-table-border-color="">\n'
   #     html += '<table>\n'
   #     html += '<tbody>\n'
   #     html += '<tr>\n'
   #     html += '<th></th>\n'
   #     html += '<th>data</th>\n'
   #     html += '<th>ttH</th>\n'
   #     html += '<th>ZH</th>\n'
   #     html += '<th>WH</th>\n'
   #     html += '<th>qqH</th>\n'
   #     html += '<th>ggH</th>\n'
   #     html += '</tr>\n'
   #     html += '<tr>\n'
   #     html += '<td>\n'
   #     html += '<strong>James</strong>\n'
   #     html += '</td>\n'

   #     data_yield = table[f'condition_{i+1}'].loc['data']
   #     ttH_yield = table[f'condition_{i+1}'].loc['hzg_tth']
   #     ZH_yield = table[f'condition_{i+1}'].loc['hzg_zh']
   #     WH_yield = table[f'condition_{i+1}'].loc['hzg_wh']
   #     qqH_yield = table[f'condition_{i+1}'].loc['hzg_vbf']
   #     ggH_yield = table[f'condition_{i+1}'].loc['hzg_gluglu']

   #     taiwan_data_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "data"').yield_val.values[0]
   #     taiwan_ttH_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "hzg_tth"').yield_val.values[0]
   #     taiwan_ZH_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "hzg_zh"').yield_val.values[0]
   #     taiwan_WH_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "hzg_wh"').yield_val.values[0]
   #     taiwan_qqH_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "hzg_vbf"').yield_val.values[0]
   #     taiwan_ggH_yield = taiwan_yields.query(f'channel == "{selection[0]}" and cat == "{cat}" and process == "hzg_gluglu"').yield_val.values[0]

   #     html += '<td>{0}</td>\n'.format(int(data_yield))
   #     html += '<td>{0:.3f}</td>\n'.format(ttH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(ZH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(WH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(qqH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(ggH_yield)
   #     html += '</tr>\n'
   #     html += '<tr>\n'
   #     html += '<td>\n'
   #     html += '<strong>Taiwan</strong>\n'
   #     html += '</td>\n'
   #     html += '<td>{0}</td>\n'.format(int(taiwan_data_yield))
   #     html += '<td>{0:.3f}</td>\n'.format(taiwan_ttH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(taiwan_ZH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(taiwan_WH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(taiwan_qqH_yield)
   #     html += '<td>{0:.3f}</td>\n'.format(taiwan_ggH_yield)
   #     html += '</tr>\n'
   #     html += '</tbody>\n'
   #     html += '</table>\n'
   #     html += '</div>\n'
   #     html += '</div>\n'
   #     html_file = open(f'html_tables/{channel}_{cat}.html', 'w')
   #     html_file.write(html)
   #     html_file.close()
