## Chat bot for crmnext.
import sys
import json
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine
from Corpus import Bank_Corpus
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

__author__ = 'avi0gaur'

class CrmnextChatBot:

    engine = IntentDeterminationEngine()
    ps = PorterStemmer()
    stop_cor = set(stopwords.words('english'))
    first_time = True
    st = 0
    card_lost_intent = []

    def __init__(self):
        pass

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
        msg = conv["user_text"]
        if self.first_time:
            self.train_intent()
            self.first_time = False
            #self.process_flow(self.intent_parser(conv))
            return self.intent_parser(msg)


    def process_flow(self, intent_json):
        intent = intent_json.get("intent_type")
        {
            "CARD_LOST_INTENT": self.card_lost_process
        }[intent]()

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
            'card_type': "No Card"
        }

        if self.st is 0:
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st]
            response['card_type'] = Bank_Corpus.FORM_USER_VERIFICATION
            self.st += 1
        elif self.st is 1:
            mn = ud.get("mobile_number")
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st].format(mn[6:10])
            self.st += 1
        elif self.st is 2:
            mn = ud.get("user_name")
            num_cards = ud.get("number of cards")
            response['response_text'] = Bank_Corpus.CARD_LOST_FLOW_RESPONSES[self.st].format(mn, num_cards)
            # Provide json response to build card on UI
            response['card_type'] = "#select_card"
            self.st += 1
        elif self.st is 3:
            #It should to be card number or list of card user need to block
            ud_res = ud.get('user_response')
            ud_card_lst = ud.get("cards")
            # self.cb.block_card(ud,)
            self.st += 1
        elif self.st is 4:
            response['response_text'] = "Do you wish to report any fraud transactions."
            self.st += 1
        elif self.st is 5:
            response['response_text'] = "Sure, your credit card ending 5694 and debit card ending 7654, has been successfully blocked. while replacing do you want to upgrade your card?"
            self.st +=1
        elif self.st is 6:
            return "#re_issue_card_status"
        else:
            return "Please be specific"






