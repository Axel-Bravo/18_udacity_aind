import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        # Model quality parameters
        best_BIC = float('Inf')
        best_model = None
        best_hidden_states = None

        N = len(self.X)  # Number of total data points (components)
        d = len(self.X[0])  # Number of features

        # Finding the best model for a concrete word
        for num_hidden_states in range(self.min_n_components, self.max_n_components+1): # Try possible hidden states
            try:
                p = num_hidden_states * num_hidden_states + 2 * num_hidden_states * d - 1  # Number of parameters
                hmm_model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                logL= hmm_model.score(self.X, self.lengths)
                BIC = -2 * logL + p * math.log(N)  # Model evaluation

                if BIC < best_BIC:  # Best model record update (lower better)
                    best_model = hmm_model
                    best_BIC = BIC
                    best_hidden_states = num_hidden_states
            except:
                pass

        if not best_model:
            return self.base_model(self.n_constant)
        else:
            return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        # Model quality parameters
        best_DIC = -float('Inf')
        best_model = None
        best_hidden_states = None

        #Model aditional parameters
        rest_of_words = list(self.words.keys())
        rest_of_words.remove(self.this_word)
        M = len(self.hwords)

        # Finding the best model for a concrete word
        for num_hidden_states in range(self.min_n_components, self.max_n_components+1): # Try possible hidden states
            try:
                hmm_model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                logL= hmm_model.score(self.X, self.lengths)

                # Rest of words evaluation
                logL_others = 0
                for word in rest_of_words:
                    loop_log = hmm_model.score(self.hwords[word])
                    logL_others += loop_log

                # Model evaluation
                DIC = logL - (1/(M -1)) * logL_others
                if DIC > best_DIC:  # Best model record update
                    best_model = hmm_model
                    best_DIC = DIC
                    best_hidden_states = num_hidden_states
            except:
                pass

        if not best_model:
            return self.base_model(self.n_constant)
        else:
            return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # Model quality parameters
        best_likelihood = -float('Inf')
        best_model = None
        best_hidden_states = None

        # Finding the best model for a concrete word
        if self.lengths == 1:  # One available example case
            for num_hidden_states in range(self.min_n_components, self.max_n_components+1): # Try possible hidden states
                try:
                    hmm_model = GaussianHMM(n_components=3, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                    logL = hmm_model.score(self.X,self.lengths)

                    if logL > best_likelihood:  # Update best model, based on log-Like score
                        best_model = hmm_model
                        best_likelihood = logL
                        best_hidden_states = num_hidden_states
                except:
                    pass
        else:  # There are more than just one example case
            split_method = KFold(n_splits= 3 if len(self.lengths) > 2 else 2)  # Split selection

            for num_hidden_states in range(self.min_n_components, self.max_n_components+1): # Try possible hidden states
                try:
                    logL_total = 0
                    n_cases = 0
                    for cv_train_idx, cv_test_idx in split_method.split(self.sequences): # Each KFold combination

                        # Select the slitted data and model training
                        loop_X_train, loop_lengths_train = combine_sequences(cv_train_idx, self.sequences)
                        hmm_model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000,
                                                random_state=self.random_state, verbose=False).\
                            fit(loop_X_train, loop_lengths_train)
                        # Model evaluation
                        loop_X_test, loop_lengths_test = combine_sequences(cv_test_idx, self.sequences)
                        logL= hmm_model.score(loop_X_test, loop_lengths_test) # We add the new value and do the avg
                        # Model evaluation addition
                        logL_total += logL
                        n_cases += 1

                    logL_total = logL_total / n_cases  #  Averaging value for selected HMM
                    if logL_total > best_likelihood:  # Best model record update
                        best_model = hmm_model
                        best_likelihood = logL_total
                        best_hidden_states = num_hidden_states
                except:
                    pass

        # Creating the optimal model, with all the available data
        if best_hidden_states:
            hmm_model = GaussianHMM(n_components=3, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(self.X, self.lengths)

        if not best_model:
            return self.base_model(self.n_constant)
        else:
            return best_model