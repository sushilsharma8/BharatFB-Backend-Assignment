from rest_framework import serializers

class FAQSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    answer = serializers.CharField()
    created_at = serializers.DateTimeField()