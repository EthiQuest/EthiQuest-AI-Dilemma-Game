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
    }
]