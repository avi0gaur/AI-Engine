
import json
import sys
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

engine = IntentDeterminationEngine()

card_keyword = [
"card",
"wallet",
"purse"
]

for card in card_keyword:
    engine.register_entity(card, "Card")

card_related_issue = [
    "lost",
    "missed",
    "stolen"
]

for cri in card_related_issue:
    engine.register_entity(cri, "CardLost")

card_type = [
    "credit",
    "debit",
    "cash card"
]

for ct in card_type:
    engine.register_entity(cri, "CardType")

card_lost_intent = IntentBuilder("Card_Lost_Intent")\
    .require("Card")\
    .require("CardLost")\
    .optionally("CardType")\
    .build()

engine.register_intent_parser(card_lost_intent)

if __name__ == '__main__':
    text = input("Enter Your Text: ")
    for intent in engine.determine_intent(text):
        if intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
