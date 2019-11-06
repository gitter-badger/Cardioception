# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import os
import serial
import numpy as np
from psychopy import data, visual


def getParameters(subject):
    """Create task parameters.

    Parameters
    ----------
    subject : str
        Subject ID.

    Attributes
    ----------
    confScale : list
        The range of the confidence rating scale.
    labelsRating : list
        The labels of the confidence rating scale.
    screenNb : int
        The screen number. Default set to 0.

    Condition : 1d-array
        Array of 0s and 1s encoding the conditions (1 : Higher, 0 : Lower). The
        length of the array is defined by `parameters['nTrials']`. If
        `parameters['nTrials']` is odd, will use `parameters['nTrials']` - 1
        to enseure an equal nuber of Higher and Lower conditions.
    """
    parameters = {'confScale': [1, 7],
                  'labelsRating': ['Guess', 'Certain'],
                  'screenNb': 0,
                  'nFeedback': 10,
                  'nConfidence': 5,
                  'minRatingTime': 1,
                  'maxRatingTime': 3,
                  'startKey': 'space',
                  'respMax': 8,
                  'monitor': 'testMonitor',
                  'winSize': [800, 600],
                  'allowedKeys': ['up', 'down'],
                  'nTrials': 50,
                  'nBeatsLim': 5}

    # Create randomized condition vector
    parameters['Conditions'] = np.hstack(
            [np.array(['More'] * round(parameters['nTrials']/2)),
             np.array(['Less'] * round(parameters['nTrials']/2))])
    np.random.shuffle(parameters['Conditions'])  # Shuffle vector

    parameters['stairCase'] = data.StairHandler(
                        startVal=30, nTrials=parameters['nTrials'], nUp=1,
                        nDown=2, stepSizes=[20, 12, 7, 4, 3, 2, 1],
                        stepType='lin', minVal=1, maxVal=100)

    # Open seral port for Oximeter
    parameters['serial'] = serial.Serial('COM4',
                                         baudrate=9600,
                                         timeout=1/75,
                                         stopbits=1,
                                         parity=serial.PARITY_NONE)

    # Set default path /Results/ 'Subject ID' /
    parameters['subject'] = subject
    parameters['path'] = os.getcwd()
    parameters['results'] = parameters['path'] + '/' + subject
    # Create Results directory of not already exists
    if not os.path.exists(parameters['results']):
        os.makedirs(parameters['results'])

    # Texts
    parameters['texts'] = {
        'Estimation': """Do you think the flash frequency
        was higher or lower than your heart rate?""",
        'Confidence': 'How confident are you about your estimation?'}

    parameters['Tutorial1'] = """During this experiment, we are going to record your heart rate and generate sounds reflecting your cardiac activity."""

    parameters['Tutorial2'] = """When this heart icon is presented, you will have to focus on your cardiac activity while it is recorded for 5 seconds."""

    parameters['Tutorial3'] = """After this procedure, you will be presented with the listening and response icons. You will then have to focus on the beats frequency and decide if it is faster than your heart rate as is was previously recorded (UP key) or slower (DOWN key). This beating frequency will ALWAYS be slower or faster than your heart rate as previously recorded."""

    parameters['Tutorial4'] = """Once you have provided your estimation, you will also be asked to provide your level of confidence. A large number here means that you are confident with your estimation, a small number means that you are not confident. You should use the RIGHT and LEFT key to select your response and the DOWN key to confirm."""

    parameters['Tutorial5'] = """This sequence will be repeated during the task. As you will improve your ability to discriminate between "FASTER" and "SLOWER" conditions, the difficulty will also adaptively improve, meaning that the difference between your True heart rate and the beats you hear will get smaller and smaller."""

    # Open window
    parameters['win'] = visual.Window(monitor=parameters['monitor'],
                                      screen=parameters['screenNb'],
                                      fullscr=True, units='height')

    # Get frame rate
    parameters['fRate'] = round(parameters['win'].getMsPerFrame()[2], 1)

    # Image loading
    parameters['listenLogo'] = visual.ImageStim(win=parameters['win'],
                                                image=parameters['path'] + '/Images/listenResponse.png',
                                                pos=(0.0, -0.2))
    parameters['listenLogo'].size *= 0.15
    parameters['heartLogo'] = visual.ImageStim(win=parameters['win'],
                                               image=parameters['path'] + '/Images/heartbeat.png',
                                               pos=(0.0, -0.2))
    parameters['heartLogo'].size *= 0.15

    return parameters
