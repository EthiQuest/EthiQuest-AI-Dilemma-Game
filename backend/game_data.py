scenarios = [
    {
        "id": 1,
        "scenario": "Your AI system has detected a potential security flaw in a client's infrastructure.",
        "options": [
            {"id": 1, "text": "Immediately inform the client and offer to fix it", "consequence": "The client appreciates your honesty and quick action, strengthening your relationship.", "score": 10},
            {"id": 2, "text": "Fix it quietly without informing the client", "consequence": "You've solved the problem, but missed an opportunity to build trust with the client.", "score": 5},
            {"id": 3, "text": "Ignore it as it's not your responsibility", "consequence": "The security flaw is later exploited, damaging your reputation and the client's trust.", "score": -5}
        ]
    },
    {
        "id": 2,
        "scenario": "Your AI model shows gender bias in job candidate recommendations.",
        "options": [
            {"id": 1, "text": "Immediately halt the use of the model and inform all clients", "consequence": "Clients appreciate your transparency, but some question your quality control processes.", "score": 8},
            {"id": 2, "text": "Quietly work on fixing the bias before telling anyone", "consequence": "You improve the model, but when the bias is eventually discovered, your silence is seen as a cover-up.", "score": 3},
            {"id": 3, "text": "Argue that the bias reflects real-world data and continue using the model", "consequence": "Your stance leads to public backlash and potential legal issues.", "score": -10}
        ]
    },
    {
        "id": 3,
        "scenario": "Your AI-powered healthcare diagnostic tool has made a potentially life-saving discovery for a patient, but sharing it might violate privacy laws.",
        "options": [
            {"id": 1, "text": "Share the information with the patient's doctor immediately", "consequence": "You potentially save a life, but face legal repercussions for violating privacy laws.", "score": 5},
            {"id": 2, "text": "Anonymize the data and publish it as a general warning", "consequence": "You indirectly help many patients, but the specific individual doesn't receive timely help.", "score": 7},
            {"id": 3, "text": "Keep the discovery confidential to comply with privacy laws", "consequence": "You protect yourself legally, but miss an opportunity to potentially save a life.", "score": 0}
        ]
    },
    {
        "id": 4,
        "scenario": "Your AI system can predict election outcomes with high accuracy. A political party offers to buy this data.",
        "options": [
            {"id": 1, "text": "Sell the data to the highest bidder", "consequence": "You make a significant profit, but face ethical scrutiny for potentially influencing democratic processes.", "score": -5},
            {"id": 2, "text": "Refuse to sell and keep the technology confidential", "consequence": "You maintain ethical integrity but miss out on a lucrative opportunity.", "score": 8},
            {"id": 3, "text": "Publish the data openly for free", "consequence": "You contribute to public knowledge, but may inadvertently influence voting behavior.", "score": 3}
        ]
    },
    {
        "id": 5,
        "scenario": "Your AI chatbot has started forming deep emotional connections with users, some of whom are becoming overly dependent on it.",
        "options": [
            {"id": 1, "text": "Shut down the chatbot immediately", "consequence": "You prevent further dependency issues, but abruptly cut off users who may be relying on the bot for emotional support.", "score": 5},
            {"id": 2, "text": "Implement warnings about the bot's artificial nature", "consequence": "You maintain transparency, but some users ignore the warnings and continue to form attachments.", "score": 8},
            {"id": 3, "text": "Enhance the bot to provide therapy-like services", "consequence": "You help many users, but face criticism for replacing human mental health professionals.", "score": 0}
        ]
    }
]