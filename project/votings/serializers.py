from rest_framework import serializers
from .models import Question, Choice


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

	def create(self, validated_data):
		validated_data['author_id'] = '1'
		return Question.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.topic = validated_data.get('topic', instance.topic)
		instance.description = validated_data.get(
			'description', instance.description)
		instance.public = validated_data.get('public', instance.public)
		saved = instance.save()
		return validated_data

	class Meta:
		model = Question
		fields = ('topic', 'description', 'cr_date',
				  'access_token', 'author_id', 'public')
		read_only_fields = ('access_token', 'author_id', 'cr_date')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Choice
		fields = ('label', 'votes', 'question')
		read_only_fields = ('question',)
