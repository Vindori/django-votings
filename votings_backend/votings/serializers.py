from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('label', 'votes', 'question', 'id')
        read_only_fields = ('question', 'votes', 'id')


class QuestionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['author'] = user
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(question=question, **choice)
        return question

    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.public = validated_data.get('public', instance.public)

        for choice in instance.choices.all():
            choice.votes = 0
            choice.save()

        choices = validated_data.get('choices')

        if choices:
            instance.choices.all().delete()
            for choice in choices:
                Choice.objects.create(label=choice['label'], question=instance)

        saved = instance.save()
        return validated_data

    choices = ChoiceSerializer(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = ('topic', 'description', 'cr_date',
                  'access_token', 'author', 'public', 'choices')
        read_only_fields = ('access_token', 'author', 'cr_date')
