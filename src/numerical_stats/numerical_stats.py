import csv
from scipy import stats
import numpy as np
from numpy import var
from numpy import mean
from math import sqrt
from db import database


def numerical_statistics():
    """
    Fetches lyrics for three time frames for each genre from the database.
    Then performs change analysis for every numerical feature, starting with ANOVA, then post-hoc one tailed t-test.
    Afterwards calculates effect size Cohen's d. Then writes results in a csv file.
    """
    rows = []
    genres = ["Country", "Pop", "Hip-Hop"]
    features = ["avg_word_length", "ttr", "non_std_words", "egocentrism", "sentiment"]
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()

    for genre in genres:
        for feature in features:

            # fetch songs from database
            s1 = 'SELECT ' + feature + ' FROM songs WHERE (year NOT LIKE "2%" OR year IS "2000") AND genre IS ?;'
            s2 = 'SELECT ' + feature + ' FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" AND genre IS ?;'
            s3 = 'SELECT ' + feature + ' FROM songs WHERE year LIKE "201%" AND year IS NOT "2010"  AND genre IS ?;'
            cur.execute(s1, (genre,))
            iterator = cur.fetchall()
            s1_vals = [el[0] for el in iterator]
            cur.execute(s2, (genre,))
            iterator = cur.fetchall()
            s2_vals = [el[0] for el in iterator]
            cur.execute(s3, (genre,))
            iterator = cur.fetchall()
            s3_vals = [el[0] for el in iterator]

            # make sure we have equal lengths
            min_len = min(len(s1_vals), len(s2_vals), len(s3_vals))
            s1_vals, s2_vals, s3_vals = equal_len(s1_vals, s2_vals, s3_vals, min_len)

            # anova
            anova_vals = anova(s1_vals, s2_vals, s3_vals)

            # post hoc: one tailed t=test
            tval12, tval23, pval12_onetailed, pval23_onetailed, correlation12, correlation23 = one_tailed_t(s1_vals,
                                                                                                            s2_vals,
                                                                                                            s3_vals)

            # calculate effect size (cohen's d)
            sdv1, sdv2, sdv3, mean1, mean2, mean3, effectsize12, effectsize23, interpretation12, interpretation23 = cohens_d(
                s1_vals, s2_vals, s3_vals, min_len)

            # prepare for csv
            rows.append([genre, min_len, feature, (mean1, sdv1), (mean2, sdv2), (mean3, sdv3), anova_vals,
                         ("t-val:", tval12, "p-val:", pval12_onetailed), correlation12, effectsize12, interpretation12,
                         ("t-val:", tval12, "p-val:", pval23_onetailed), correlation23, effectsize23, interpretation23])

    conn.close()
    header = ['Genre', 'Group size', 'Feature', 'Mean and standard deviation s1', 'Mean and standard deviation s2',
              'Mean and standard deviation s3', 'Anova results', 'One tailed t-test s1 and s2', 'Correlation s1 s2',
              'Effect size s1 s2', 'Interpretation effect size s1 s2', 'One tailed t-test s2 and s3',
              'Correlation s2 s3', 'Effect size s2 s3', 'Interpretation effect size s2 s3']
    write_csv(header, rows)

    return


def anova(s1_vals, s2_vals, s3_vals):
    """
    The one-way ANOVA tests the null hypothesis that two or more groups have the same population mean.

    :param s1_vals: lyrics corresponding to year <= 2000
    :param s2_vals: lyrics corresponding to 2001 <= year <= 2010
    :param s3_vals: lyrics corresponding to year >= 2011
    :return: F-value and p-value from ANOVA calculation
    """
    return stats.f_oneway(s1_vals, s2_vals, s3_vals)


def equal_len(s1_vals, s2_vals, s3_vals, min_len):
    """
    Makes sure all groups have the same length

    :param s1_vals: lyrics corresponding to year <= 2000
    :param s2_vals: lyrics corresponding to 2001 <= year <= 2010
    :param s3_vals: lyrics corresponding to year >= 2011
    :param min_len: minimal group size
    :return: equalized groups
    """

    return s1_vals[:min_len], s2_vals[:min_len], s3_vals[:min_len]


def one_tailed_t(s1_vals, s2_vals, s3_vals):
    """
    First calculates a two tailed t-test for independent groups
    between group 1 and 2 and group 2 and 3.
    Then uses the resulting t- and p-values to calculate a one
    tailed t-test in both directions and evaluates the results.

    :param s1_vals: lyrics corresponding to year <= 2000
    :param s2_vals: lyrics corresponding to 2001 <= year <= 2010
    :param s3_vals: lyrics corresponding to year >= 2011
    :return: t-values, p-values (one tailed), interpretations of correlations
    """
    # set alpha
    alpha = 0.05

    # two tailed t test
    corr12 = stats.ttest_ind(s1_vals, s2_vals, equal_var=False)
    corr23 = stats.ttest_ind(s2_vals, s3_vals, equal_var=False)

    # save t and p values
    tval12 = corr12[0]
    pval12 = corr12[1]
    tval23 = corr23[0]
    pval23 = corr23[1]

    # one tailed t-test
    # given p and t values from a two-tailed test,
    # you would reject the null hypothesis of a greater-than test when p/2 < alpha
    # and t > 0, and of a less-than test when p/2 < alpha and t < 0.

    # prepare p values
    pval12_onetailed = pval12 / 2
    pval23_onetailed = pval23 / 2

    # calculate direction of effect
    if pval12_onetailed < alpha:
        if tval12 < 0:
            correlation12 = " 'less than' correlation between 1 and 2"
        else:
            correlation12 = " 'greater than' correlation between 1 and 2"
    else:
        correlation12 = "no correlation"

    if pval23_onetailed < alpha:
        if tval23 < 0:
            correlation23 = " 'less than' correlation between 2 and 3"
        else:
            correlation23 = " 'greater than' correlation between 2 and 3"
    else:
        correlation23 = "no correlation"

    return tval12, tval23, pval12_onetailed, pval23_onetailed, correlation12, correlation23


def cohens_d(s1_vals, s2_vals, s3_vals, min_len):
    """
    Calculate the effect size using Cohen's d for correlations between
    group 1 and group 2, group 2 and group 3.
    Modified from https://machinelearningmastery.com/effect-size-measures-in-python/
    :param s1_vals: lyrics corresponding to year <= 2000
    :param s2_vals: lyrics corresponding to 2001 <= year <= 2010
    :param s3_vals: lyrics corresponding to year >= 2011
    :param min_len: sample size
    :return: standard deviations, means, effect sizes, interpretations of effect sizes
    """
    # calculate the variance of the samples
    s1_var, s2_var, s3_var = var(s1_vals, ddof=1), var(s2_vals, ddof=1), var(s3_vals, ddof=1)

    # calculate the pooled standard deviation
    pooled_s12 = sqrt(((min_len - 1) * s1_var + (min_len - 1) * s2_var) / (min_len + min_len - 2))
    pooled_s23 = sqrt(((min_len - 1) * s2_var + (min_len - 1) * s3_var) / (min_len + min_len - 2))

    # calculate the means of the samples
    mean1, mean2, mean3 = mean(s1_vals), mean(s2_vals), mean(s3_vals)

    sdv1 = np.std(s1_vals)
    sdv2 = np.std(s2_vals)
    sdv3 = np.std(s3_vals)

    # calculate the effect size
    effectsize12 = (mean1 - mean2) / pooled_s12
    effectsize23 = (mean2 - mean3) / pooled_s23

    # interpret the effect size according to conventions
    if abs(effectsize12) < 0.2:
        interpretation12 = "not very significant"
    elif abs(effectsize12) > 0.2 and abs(effectsize12) <= 0.5:
        interpretation12 = "somewhat significant"
    elif abs(effectsize12) > 0.5 and abs(effectsize12) <= 0.8:
        interpretation12 = "quite significant"
    elif abs(effectsize12) > 0.8:
        interpretation12 = "very significant"

    if abs(effectsize23) < 0.2:
        interpretation23 = "not very significant"
    elif abs(effectsize23) > 0.2 and abs(effectsize23) <= 0.5:
        interpretation23 = "somewhat significant"
    elif abs(effectsize23) > 0.5 and abs(effectsize23) <= 0.8:
        interpretation23 = "quite significant"
    elif abs(effectsize23) > 0.8:
        interpretation23 = "very significant"

    return sdv1, sdv2, sdv3, mean1, mean2, mean3, effectsize12, effectsize23, interpretation12, interpretation23


def write_csv(header, rows):
    """
    Creates a csv file containing the collected data

    :param header: header for csv file
    :param rows: list of rows for the csv file
    """
    with open('results.csv', 'wt') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(header)  # write header

        for row in rows:
            csv_writer.writerow(row)
    return

