import json
from datetime import datetime

class StudyReport:
    def __init__(self):
        self.start_time = datetime.now().isoformat()
        self.interactions = []

    def add(self, affective_summary, user_text, llm_response):
        self.interactions.append({
            "time": datetime.now().isoformat(),
            "affective_summary": affective_summary,
            "user_text": user_text,
            "llm_response": llm_response
        })

    def export(self):
        report = {
            "session_start": self.start_time,
            "session_end": datetime.now().isoformat(),
            "interactions": self.interactions
        }

        filename = f"study_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filename
