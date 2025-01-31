
from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question_en = models.TextField()
    answer_en = RichTextField()  # WYSIWYG for English
    question_hi = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_translated(self, lang):
        # Dynamically fetch translated fields
        return {
            "question": getattr(self, f'question_{lang}', self.question_en),
            "answer": getattr(self, f'answer_{lang}', self.answer_en)
        }

    def save(self, *args, **kwargs):
        translator = Translator()
        
        # Translate questions
        if not self.question_hi:
            self.question_hi = translator.translate(self.question_en, dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question_en, dest='bn').text
        
        # Translate answers
        if not self.answer_hi:
            self.answer_hi = translator.translate(self.answer_en, dest='hi').text
        if not self.answer_bn:
            self.answer_bn = translator.translate(self.answer_en, dest='bn').text
        
        super().save(*args, **kwargs)
        