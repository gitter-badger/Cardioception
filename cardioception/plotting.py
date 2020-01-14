# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import numpy as np
import seaborn as sns
from pingouin import madmedianrule
import matplotlib.pyplot as plt


def plot_hr(oximeter, ax=None):
    """Given a peaks vector, returns frequency plots.

    Parameters
    ----------
    oximeter : instance of Oximeter
        The recording instance, where additional channels track different
        events using boolean recording.

    Returns
    -------
    ax : Matplotlib instance
        Figure.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(oximeter.times, oximeter.instant_rr)
    ax.set_xlabel('Time (s)', size=20)
    ax.set_ylabel('R-R (ms)', size=20)

    return ax


def plot_events(oximeter, ax=None):
    """Plot events distribution.

    Parameters
    ----------
    oximeter : instance of Oximeter
        The recording instance, where additional channels track different
        events using boolean recording.

    Returns
    -------
    ax : Matplotlib instance
        The axe instance of the Matplotlib figure.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(13, 5))
    events = oximeter.channels
    for i, ev in enumerate(events):
        events[ev] = np.asarray(events[ev]) == 1
        ax.fill_between(x=oximeter.times, y1=i, y2=i+1, where=events[ev])

    # Add y ticks with channels names
    ax.set_yticks(np.arange(len(events)) + 0.5)
    ax.set_yticklabels([key for key in events])
    ax.set_xlabel('Time (s)', size=20)

    return ax


def plot_oximeter(oximeter, ax=None):
    """Plot recorded PPG signal.

    Parameters
    ----------
    oximeter : Oximeter instance
        The Oximeter instance used to record the signal.

    Return
    ------
    fig, ax : Matplotlib instances.
        The figure and axe instances.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(oximeter.times, oximeter.threshold, linestyle='--', color='gray',
            label='Threshold')
    ax.fill_between(x=oximeter.times,
                    y1=oximeter.threshold,
                    y2=np.asarray(oximeter.recording).min(),
                    alpha=0.2,
                    color='gray')
    ax.plot(oximeter.times, oximeter.recording, label='Recording')
    ax.fill_between(x=oximeter.times,
                    y1=oximeter.recording,
                    y2=np.asarray(oximeter.recording).min(),
                    color='w')
    ax.plot(np.asarray(oximeter.times)[np.where(oximeter.peaks)[0]],
            np.asarray(oximeter.recording)[np.where(oximeter.peaks)[0]],
            'ro', label='Online estimation')
    ax.set_ylabel('PPG level', size=20)
    ax.set_xlabel('Time (s)', size=20)
    ax.legend()

    return ax


def hrd_convergence(results_df, path=None):
    """Plot the trial by trial performances.

    Parameters
    ----------
    results_df : pandas DataFrame
        The behavioral results generated by the run function.
    path : str | None
        Result folder.

    Returns
    -------
    fig, ax : Matplotlib instances.
    """
    # Plot convergence
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(13, 5))
    plt.subplot(121)

    # Convergence line
    revers = np.abs(results_df.Alpha[results_df.Accuracy == 0])
    conv = np.median(revers[~madmedianrule(revers)])
    plt.axhline(y=conv, linestyle='--')

    # Text
    plt.text(len(results_df)/2, conv*2, 'Convergence: ' + str(conv))

    plt.plot(results_df.nTrials,
             np.abs(results_df.Alpha), 'gray', linestyle='--')
    plt.plot(results_df.nTrials[results_df.Accuracy == 1],
             np.abs(results_df.Alpha[results_df.Accuracy == 1]), 'bo')
    plt.plot(results_df.nTrials[results_df.Accuracy == 0],
             np.abs(results_df.Alpha[results_df.Accuracy == 0]), 'ro')

    plt.ylabel('Noise (bpm)')
    plt.xlabel('Trials')
    plt.title('Noise convergence')

    # Using actual heart rate
    plt.subplot(122)
    # True HR
    plt.plot(results_df.HR, 'gray', linestyle='--', marker='o',
             alpha=0.5, label='True HR')

    # Estimated HR
    plt.plot(results_df.nTrials[results_df.Accuracy == 1],
             results_df.HR[results_df.Accuracy == 1] +
             results_df.Alpha[results_df.Accuracy == 1], 'bo')
    plt.plot(results_df.nTrials[results_df.Accuracy == 0],
             results_df.HR[results_df.Accuracy == 0] +
             results_df.Alpha[results_df.Accuracy == 0], 'ro')
    plt.plot(results_df.nTrials,
             results_df.HR + results_df.Alpha, color='b', linestyle='--',
             label='Estimate')

    plt.ylabel('BPM')
    plt.xlabel('Trials')
    plt.legend()
    plt.title('Heart rate convergence')
    sns.despine()
    plt.tight_layout()
    if path is not None:
        plt.savefig(path + 'convergence.png', dpi=600)

    return fig, ax


def plot_confidence(confidence, accuracy, path=None):
    """Plot confidence distribution for correct and incorrect responses.

    Parameters
    ----------
    confidence : 1d array
        Array containing the confidence values.
    accuracy : 1d array
        Array containing the accuracy (correct/incorrect) values.
    path : str | None
        Result folder.

    Returns
    -------
    fig, ax : Matplotlib instances.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Confidence
    for conf in range(1, 8):
        # Correct trials
        p = sum((accuracy == 0) & (confidence == conf)) / sum(accuracy == 0)
        plt.bar(conf-0.15, p, width=0.30, color='r', label = 'Error Trials')

        # Incorrect trials
        p = sum((accuracy == 1) & (confidence == conf)) / sum(accuracy == 1)
        plt.bar(conf+0.15, p, width=0.30, color='g', label = 'Correct Trials')
    plt.legend()
    plt.ylabel('P(Rating|Precision)')
    plt.xlabel('Confidence rating')
    plt.xticks(range(1, 8))
    sns.despine()
    plt.tight_layout()
    if path is not None:
        plt.savefig(path + 'confidence.png', dpi=600)

    return fig, ax
