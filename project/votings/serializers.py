from rest_framework import serializers
from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('label', 'votes', 'question', 'id')
        read_only_fields = ('question', 'votes', 'id')


class QuestionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['author_id'] = '1'
        choices = validated_data.pop('choices')
        # TODO: check that user can't set 'votes' value
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(question=question, **choice)
        return question

    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.public = validated_data.get('public', instance.public)
        saved = instance.save()
        return validated_data

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('topic', 'description', 'cr_date',
                  'access_token', 'author_id', 'public', 'choices')
        read_only_fields = ('access_token', 'author_id', 'cr_date')
