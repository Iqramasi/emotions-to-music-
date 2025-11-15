from transformers import pipeline

class EmotionModel:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=False
        )

    def predict_emotion(self, text):
        result = self.classifier(text)[0]
        return result["label"]
