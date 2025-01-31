from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer

class FAQListView(generics.ListAPIView):
    serializer_class = FAQSerializer

    # @method_decorator(cache_page(60*10))  # Cache for 10 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')  # Default to English
        faqs = FAQ.objects.all()
        # Return only translated fields
        return [{
            "id": faq.id,
            "question": getattr(faq, f'question_{lang}', faq.question_en),
            "answer": getattr(faq, f'answer_{lang}', faq.answer_en),
            "created_at": faq.created_at
        } for faq in faqs]