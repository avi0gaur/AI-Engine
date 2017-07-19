
''' Chat corpus to make response for the user and to generate appropriate card '''
class Bank_Corpus:
    card_keyword = [
        "card",
        "wallet",
        "purse"
    ]
    card_related_issue = [
        "lost",
        "missed",
        "stolen"
    ]
    card_type = [
        "credit",
        "debit",
        "cash card"
    ]

    """
    Tags for different kind of cards
    """
    # Loan Context form
    FORM_USER_VERIFICATION = "#show_form"
    CARD_ACTION_FORM = "#showactions"

    """
    Responses for card lost flow
    """

    CARD_LOST_FLOW_RESPONSES = {
        0: "We need some info to validate please fill below form.",
        1: 'Please enter OTP sent on your registered mobile number ending with :{}',
        2: 'Hi {}, I can see {} cards registered with your account, which one you want to block.',
        3: "",
        4: "Do you wish to report any fraud transactions.",
        5: "Sure, your credit card ending {}, has been successfully blocked. while replacing do you want to upgrade your card?",
        6: "#re_issue_card_status"
    }

    CARD_LOST_FLOW_EXP_RES = {
        0: [],
        1: [],
        2: ['both'],
        3: [],
        4: [['no','na','not any','not sure'], ['yes','haan','yes please']],
        5: ['yes', 'sure'],
        6: []
    }