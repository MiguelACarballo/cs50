import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positives_list = list()
        self.negatives_list = list()

        positive_file = open(positives, "r")
        for line in positive_file:
            if line.startswith(';') == False:
                self.positives_list.append(line.strip('\n'))
        positive_file.close()

        negative_file = open(negatives, "r")
        for line in negative_file:
            if line.startswith(';') == False:
                self.negatives_list.append(line.strip('\n'))
        negative_file.close()




    def analyze(self, text):
        score = 0

        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        for token in tokens:
            if token.lower() in self.positives_list:
                score += 1
            elif token.lower() in self.negatives_list:
                score -= 1

        return score
