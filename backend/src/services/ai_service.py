from transformers import pipeline
import torch
import os
import whisper

class AIService:
    def __init__(self):
        # Initialize the Stance Analysis pipeline
        self.stance_pipeline = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1
        )
        # Initialize the Summarization pipeline
        self.summarizer_pipeline = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=0 if torch.cuda.is_available() else -1
        )
        # Load the base Whisper model
        self.whisper_model = whisper.load_model("base")

    def transcribe_audio_file(self, audio_path: str) -> str:
        """Transcribes an audio file using OpenAI's Whisper."""
        try:
            if not audio_path or not os.path.exists(audio_path):
                print(f"ERROR: Audio file not found at {audio_path}")
                return "Audio file not found for transcription."

            print(f"INFO: Transcribing {audio_path} with Whisper...")
            result = self.whisper_model.transcribe(audio_path)
            transcribed_text = result['text']

            # Save the transcript for review
            video_id = os.path.basename(audio_path).split('.')[0]
            reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'reports'))
            transcript_file_path = os.path.join(reports_dir, f'{video_id}_whisper_transcript.txt')
            with open(transcript_file_path, 'w', encoding='utf-8') as f:
                f.write(transcribed_text)

            return transcribed_text
        except Exception as e:
            print(f"Error during Whisper transcription: {e}")
            return "Failed to transcribe audio."
        finally:
            # Clean up the audio file
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

    def summarize_text(self, text: str) -> str:
        """Summarizes a long text into a concise summary."""
        if not text or text == "No transcript available for this video." or text == "Could not download or find audio file." or text == "Failed to transcribe audio.":
            return text
        
        print("INFO: Summarizing transcript...")
        # The model works best with text between 50 and 1000 characters for a good summary
        # We'll truncate the text to a reasonable length
        max_length = min(len(text.split()), 1000)
        min_length = max(30, max_length // 4)
        
        summary = self.summarizer_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def analyze_stance(self, comments: list[str], video_claim: str) -> list[dict]:
        """Analyzes the stance of comments relative to the video's claim."""
        hypothesis_template = "This comment is {} the video's claim."
        candidate_labels = ["agreeing with", "disagreeing with", "neutral towards"]
        results = self.stance_pipeline(comments, candidate_labels=candidate_labels, hypothesis_template=hypothesis_template)
        
        normalized_results = []
        for res in results:
            top_label = res['labels'][0]
            if top_label == 'agreeing with':
                normalized_results.append({'stance': 'AGREEMENT'})
            elif top_label == 'disagreeing with':
                normalized_results.append({'stance': 'DISAGREEMENT'})
            else:
                normalized_results.append({'stance': 'NEUTRAL'})
        return normalized_results

    def generate_word_cloud_data(self, texts: list[str]) -> dict[str, float]:
        """Generates word frequency data for a word cloud."""
        word_counts = {}
        for text in texts:
            for word in text.lower().split():
                if len(word) > 3 and word.isalpha():
                    word_counts[word] = word_counts.get(word, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_words[:30])