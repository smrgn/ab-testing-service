import pandas as pd
import scipy.stats as ss
import statsmodels.stats.proportion as sms
import numpy as np
import math

# Расчёт размера выборки для среднего значения
def calculate_sample_size_mean(std_dev, abs_mde, alpha, power):
    z_alpha = ss.norm.ppf(1 - alpha / 2)
    z_beta = ss.norm.ppf(power)
    return math.ceil(2 * ((z_alpha + z_beta) ** 2) * (std_dev ** 2) / (abs_mde ** 2))

# Расчёт размера выборки для пропорции (конверсии)
def calculate_sample_size_proportion(p1, p2, alpha, power):
    z_alpha = ss.norm.ppf(1 - alpha / 2)
    z_beta = ss.norm.ppf(power)
    std1 = p1 * (1 - p1)
    std2 = p2 * (1 - p2)
    return math.ceil(((z_alpha + z_beta) ** 2 * (std1 + std2)) / (p2 - p1) ** 2)

import scipy.stats as ss
import statsmodels.stats.proportion as sms
import numpy as np

# A/A-тест для бинарной метрики (z-test)
def aa_test_binary(df, n_sim=10000):
    aa_binary_ztest_pvalue_list = []

    for i in range(n_sim):
        sample_mask = ss.bernoulli.rvs(0.5, size=len(df)) == 1

        binary_mask_group_a = (df['metric']==1)[sample_mask]
        binary_mask_group_b = (df['metric']==1)[~sample_mask]

        binary_nobs_group_a = len(binary_mask_group_a)
        binary_nobs_group_b = len(binary_mask_group_b)

        binary_counts_group_a = binary_mask_group_a.sum()
        binary_counts_group_b = binary_mask_group_b.sum()

        binary_z_score_i, binary_ztest_pvalue_i = sms.proportions_ztest(count = [binary_counts_group_a, binary_counts_group_b],
                            nobs = [binary_nobs_group_a, binary_nobs_group_b])

        aa_binary_ztest_pvalue_list.append(binary_ztest_pvalue_i)

    binary_alpha_ci = sms.proportion_confint((np.array(aa_binary_ztest_pvalue_list) <= 0.05).sum(), n_sim, alpha=0.01)

    p_count = (np.array(aa_binary_ztest_pvalue_list) <= 0.05).sum()
    p_value = (np.array(aa_binary_ztest_pvalue_list) <= 0.05).sum()/n_sim

    return p_count, p_value, binary_alpha_ci

# A/A-тест для небинарной метрики (t-test)
def aa_test_mean(df, n_sim=10000):
    p_values = []

    for _ in range(n_sim):
        sample_mask = ss.bernoulli.rvs(0.5, size=len(df)) == 1

        group_a = df['metric'][sample_mask]
        group_b = df['metric'][~sample_mask]

        t_stat, p_val = ss.ttest_ind(group_a, group_b, equal_var=False)  # Welch's t-test
        p_values.append(p_val)

    p_values = np.array(p_values)
    p_count = (p_values <= 0.05).sum()
    p_rate = p_count / n_sim

    alpha_ci = sms.proportion_confint(count=p_count, nobs=n_sim, alpha=0.01, method='wilson')

    return p_count, p_rate, alpha_ci

# Расчет результатов А/B-теста
def run_ab_test(df, test_type='t-test'):
    group_a = df[df['group'] == 0]['metric']
    group_b = df[df['group'] == 1]['metric']

    if test_type == 't-test с линеаризацией (для ratio)': 
        group_a_num = df[df['group'] == 0]['num']
        group_a_denom = df[df['group'] == 0]['denom']
        group_b_num = df[df['group'] == 1]['num']
        group_b_denom = df[df['group'] == 1]['denom']
        metric_a = group_a_num / group_a_denom

        stat, p_value = ss.ttest_ind((group_a_num - metric_a * group_a_denom), \
                                     (group_b_num - metric_a * group_b_denom), equal_var=False)

    elif test_type == 't-test':
        stat, p_value = ss.ttest_ind(group_a, group_b, equal_var=False)

    elif test_type == 'z-test':
        stat, p_value = sms.proportions_ztest(count = [group_a.sum(), group_b.sum()],
                            nobs = [len(group_a), len(group_b)])
    
    return stat, p_value, group_a.mean(), group_b.mean() 

