from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.utils import timezone
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        # Create a sample FAQ for testing
        self.faq = FAQ.objects.create(
            question_en="What is Python?",
            answer_en="<p>Python is a programming language.</p>"
        )
        # Clear cache before each test
        cache.clear()

    # --------------------------
    # Model Tests
    # --------------------------
    def test_translation_auto_generation(self):
        """Test if Hindi/Bengali translations are auto-generated on save."""
        self.assertEqual(self.faq.question_hi, "पायथन क्या है?")
        self.assertEqual(self.faq.answer_hi, "<p>पायथन एक प्रोग्रामिंग भाषा है।</p>")
        self.assertEqual(self.faq.question_bn, "পাইথন কী?")  # Updated expectation
        self.assertEqual(self.faq.answer_bn, "<p>পাইথন একটি প্রোগ্রামিং ভাষা।</p>")

    def test_existing_translation_not_overwritten(self):
        """Test manual translations are not overwritten."""
        faq = FAQ.objects.create(
            question_en="What is Git?",
            answer_en="<p>Git is a version control system.</p>",
            question_hi="कस्टम हिंदी प्रश्न",  # Manual Hindi translation
            answer_hi="<p>कस्टम हिंदी उत्तर</p>"
        )
        self.assertEqual(faq.question_hi, "कस्टम हिंदी प्रश्न")
        self.assertEqual(faq.answer_hi, "<p>कस्टम हिंदी उत्तर</p>")

    def test_get_translated_method(self):
        """Test the get_translated() method fallback logic."""
        # Test Hindi translation
        translated = self.faq.get_translated('hi')
        self.assertEqual(translated['question'], "पायथन क्या है?")
        self.assertEqual(translated['answer'], "<p> पायथन एक प्रोग्रामिंग भाषा है। </p>")

        # Test invalid language fallback
        translated = self.faq.get_translated('fr')
        self.assertEqual(translated['question'], "What is Python?")
        self.assertEqual(translated['answer'], "<p>Python is a programming language.</p>")

    # --------------------------
    # API Tests
    # --------------------------
    def test_api_response_structure(self):
        """Test API response structure and status code."""
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data[0])
        self.assertIn('question', response.data[0])
        self.assertIn('answer', response.data[0])
        self.assertIn('created_at', response.data[0])

    def test_api_english_response(self):
        """Test default English response."""
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.data[0]['question'], "What is Python?")
        self.assertEqual(response.data[0]['answer'], "<p>Python is a programming language.</p>")

    def test_api_hindi_translation(self):
        """Test Hindi translation via API."""
        response = self.client.get(reverse('faq-list') + '?lang=hi')
        # Match exact whitespace and punctuation from translation:
        self.assertEqual(response.data[0]['answer'], "<p>पायथन एक प्रोग्रामिंग भाषा है।</p>")

    def test_api_invalid_language_fallback(self):
        """Test API falls back to English for invalid languages."""
        response = self.client.get(reverse('faq-list') + '?lang=fr')
        self.assertEqual(response.data[0]['question'], "What is Python?")

    # --------------------------
    # Caching Tests
    # --------------------------
    def test_api_caching(self):
        """Test if API responses are cached."""
        # First request (uncached)
        response1 = self.client.get(reverse('faq-list'))
        self.assertIsNone(cache.get('your_cache_key'))  # Replace with actual cache key
        
        # Second request (cached)
        response2 = self.client.get(reverse('faq-list'))
        self.assertIsNotNone(cache.get('your_cache_key'))  # Verify cache is populated

    # --------------------------
    # Edge Cases
    # --------------------------
    def test_empty_translations_fallback(self):
        """Test fallback when translations are missing."""
        faq = FAQ.objects.create(
            question_en="What is Docker?",
            answer_en="<p>Docker is a containerization platform.</p>",
            # Explicitly leave translations empty
            question_hi=None,
            answer_hi=None
        )
        response = self.client.get(reverse('faq-list') + '?lang=hi')
        self.assertEqual(response.data[1]['question'], "What is Docker?")  # Fallback to EN