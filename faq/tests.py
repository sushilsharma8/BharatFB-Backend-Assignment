from django.test import TestCase
from django.urls import reverse
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        # Create a sample FAQ for testing
        self.faq = FAQ.objects.create(
            question_en="What is Python?",
            answer_en="<p>Python is a programming language.</p>"
        )

    # --------------------------
    # Model Tests
    # --------------------------
    def test_faq_creation(self):
        """Test if an FAQ is created successfully."""
        self.assertEqual(self.faq.question_en, "What is Python?")
        self.assertEqual(self.faq.answer_en, "<p>Python is a programming language.</p>")

    def test_translation_auto_generation(self):
        """Test if Hindi/Bengali translations are auto-generated on save."""
        self.assertEqual(self.faq.question_hi, "पायथन क्या है?")
        self.assertEqual(self.faq.answer_hi, "<p> पायथन एक प्रोग्रामिंग भाषा है। </p>")
        self.assertEqual(self.faq.question_bn, "পাইথন কী?")
        self.assertEqual(self.faq.answer_bn, "<p> পাইথন একটি প্রোগ্রামিং ভাষা </</p>")

    # --------------------------
    # API Tests
    # --------------------------
    def test_api_english_response(self):
        """Test default English response."""
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Python?")
        self.assertEqual(response.data[0]['answer'], "<p>Python is a programming language.</p>")

    def test_api_hindi_translation(self):
        """Test Hindi translation via API."""
        response = self.client.get(reverse('faq-list') + '?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "पायथन क्या है?")
        self.assertEqual(response.data[0]['answer'], "<p> पायथन एक प्रोग्रामिंग भाषा है। </p>")