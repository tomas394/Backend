class AIService:
    
    @staticmethod
    async def process_document_ocr(file_bytes):
        """Simula leitura de receita médica"""
        # Aqui entraria o código real da AWS Textract
        return {
            "document_type": "prescription",
            "extracted_data": {
                "medication": "Varfarina",
                "dosage": "5mg",
                "frequency": "Ao jantar",
                "doctor": "Dr. Rui Silva"
            },
            "confidence": 0.98
        }

    @staticmethod
    async def predict_health_risk(metrics: dict):
        """Simula análise preditiva"""
        steps = metrics.get("steps", 0)
        sleep = metrics.get("sleep_score", 100)
        
        if sleep < 50 and steps < 1000:
            return {
                "alert_level": "HIGH",
                "risk_type": "POSSIBLE_INFECTION",
                "message": "Deteção de padrão anómalo: Pouco movimento e sono interrompido."
            }
        return {"alert_level": "LOW", "message": "Padrões normais."}

def mock_ocr(file):
    # Mock: Always return a fixed structure
    return {
        "medication": "Paracetamol",
        "dosage": "500mg",
        "frequency": "2x/day",
        "patient": "John Doe"
    }