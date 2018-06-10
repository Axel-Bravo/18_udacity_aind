import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    # Probabilities list creation
    for test_element_id in range(0, len(test_set.get_all_Xlengths())):  # Operate all test elements in order
        test_element_dict = {}

        for word_model in models:  # We compare the given test word with all words trained with our model
            loop_model = models[word_model]  # Temporary model we will evaluate
            loop_X, loop_lengths = test_set.get_item_Xlengths(test_element_id)
            try:
                test_element_dict[word_model] = loop_model.score(loop_X, loop_lengths)
            except:
                pass

        if not test_element_dict:
            probabilities.append(float("-inf"))
        else:
            probabilities.append(test_element_dict)

    # Guess list creation
    for element in probabilities:
        guesses.append(max(element, key=element.get))

    return probabilities, guesses