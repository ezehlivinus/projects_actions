from rest_framework import serializers
from the_rest_api.models import Project, Action
from django.contrib.auth.models import User, Group

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'completed', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'project', 'description', 'note', 'created_at', 'updated_at']

    def create(self, validated_data):
        action = Action.objects.create(**validated_data)
        return action


    def update(self, instance, validated_data):

        instance.project = validated_data.get('project', instance.project)
        instance.description = validated_data.get('description', instance.description)
        instance.note = validated_data.get('note', instance.note)
        instance.save()
        return instance
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
