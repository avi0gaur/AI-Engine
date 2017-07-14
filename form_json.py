"""
class to provide json format to generate card on ui

"""
class BankCardJson:

    def __init__(self):
        pass

    show_validation_form = {
                    "type": "card",
                    "template": "form",
                    "message":
                        {
                            "heading": "Please provide your details:",
                            "ok": "OK",
                            "response": "Detials Provided",
                            "fields":
                                [
                                    {
                                        "name": "dob",
                                        "label": "DOB",
                                        "type": "date"
                                    },
                                    {
                                        "name": "mobile",
                                        "label": "Mobile",
                                        "type": "tel"
                                    }

                                ]
                        },

                    "senderId": "1234"
                }

    show_actions = {
            "type": "action",
            "message": [
                {
                    "label": "I will keep you updated",
                    "response": "OK. Keep me updated",
                },
                {
                    "label": "Any more assisance?",
                    "response": "Yes, I need Assistance"
                }
            ],
            "senderId": "1234"
        }

    reIssue_card_status = {
                "type": "card",
                "template": "status",
                "message": {
                    "heading": "Your Case Status",
                    "steps": [
                        {
                            "no": "01",
                            "label": "New",
                            "current": True
                        }, {
                            "no": "02",
                            "label": "Analysis",
                            "current": True
                        }, {
                            "no": "03",
                            "label": "Fixing",
                            "current": True
                        }, {
                            "no": "04",
                            "label": "Close",
                            "current": False
                        }
                    ],
                    "fields": [
                        {
                            "label": "Case Id",
                            "value": "39462"
                        }, {
                            "label": "Estimated Closure",
                            "value": "19th June 2017"
                        }, {
                            "label": "Product",
                            "value": "Credit card"
                        }
                    ],
                    "actions": [
                        {
                            "label": "Withdraw",
                            "response": "Withdraw",
                        }, {
                            "label": "Escalate",
                            "response": "Escalate",
                        }
                    ]
                }
            }