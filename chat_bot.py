## Chat bot for crmnext.
import sys
import json
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine
from .Corpus import Bank_Corpus
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from .chat_logger import BotLogger
from .spell_checker import correct


__author__ = 'avi0gaur'

class CrmnextChatBot:

    def __init__(self):
        self.engine = IntentDeterminationEngine()
        self.bot = BotLogger()
        self.ps = PorterStemmer()
        self.stop_cor = set(stopwords.words('english'))
        self.first_time = True
        self.st = 0
        self.card_lost_intent = []

    def train_intent(self):
        """
        Training intent engine to classify text intent
        :return:
        """
        for card in Bank_Corpus.card_keyword:
            self.engine.register_entity(card, "Card")

        for cri in Bank_Corpus.card_related_issue:
            self.engine.register_entity(cri, "CardLost")

        for ct in Bank_Corpus.card_type:
            self.engine.register_entity(ct, "CardType")

        self.card_lost_intent = IntentBuilder("CARD_LOST_INTENT") \
            .require("Card") \
            .require("CardLost") \
            .optionally("CardType") \
            .build()

        self.engine.register_intent_parser(self.card_lost_intent)
    """
    json pattern 
    eg:
    {
        "user_text":"Hi I lost my card",
        "user_name":"Avinash"
    }
    """
    def run_bot(self, conv):
        """
        Thread starts from here.
        :return:
        """
        self.bot.log_debug("Received Json in run_bot: {}".format(conv))

        msg = conv["user_text"]
        if self.first_time:
            self.train_intent()
            self.first_time = False
            self.process_flow(self.intent_parser(msg))
        else:
            self.process_flow(conv)

    def process_flow(self, intent_json):
        intent = intent_json["intent_type"]
        {
            "CARD_LOST_INTENT": self.card_lost_process
        }[intent](intent_json)

    def remove_stop_words(self, conv):
        word_tokens = word_tokenize(conv)
        fs = [w for w in word_tokens if not w in self.stop_cor]
        return self.rooting_word(fs)

    def rooting_word(self, conv):
        root_word = []
        for w in conv:
            root_word.append(self.ps.stem(w))
            return root_word

    def intent_parser(self, conv):
        for intent in self.engine.determine_intent(conv):
            if intent.get('confidence') > 0:
                return json.dumps(intent, indent=4)
            else:
                return {
                        "intent_type": "NA",
                        "Card": "NA",
                        "CardLost": "NA",
                        "target": "NA",
                        "confidence": 0.0
                        }

    def card_lost_process(self, ud):

        response = {
            'response_text': "I am sorry ! didn't get you.",
            'card_type': "No Card",
            'user_stage': self.st
        }

        num_cards = ud.get("number of cards")

        if self.st is 0:
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st]
            response['card_type'] = Bank_Corpus.FORM_USER_VERIFICATION
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 1:
            mn = ud.get("mobile_number")
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st].format(mn[6:10])
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 2:
            mn = ud.get("user_name")
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st].format(mn, num_cards)
            # Provide json response to build card on UI
            response['card_type'] = "#select_card"
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 3:
            #It should to be card number or list of card user need to block
            ud_res = ud.get('user_response')
            ud_card_lst = ud.get("cards")
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 4:
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st]
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 5:
            Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st].format(num_cards)
            self.st += 1
            response['user_stage'] = self.st
        elif self.st is 6:
            response['card_type'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st]
            self.st += 1
            response['user_stage'] = self.st
            return
        else:
            response['response_text'] = "Please be specific, would you like to cancel the card blocking process ?"

    def clean_text(self, raw):
        t = self.remove_stop_words(raw)
        c = []
        for w in t:
            c.append(correct(w))
        c = self.rooting_word(c)
        return c
