from rest_framework import serializers
from snippets.models import User , Project, UserLog

#JSON for Project
class ProjectSerializer(serializers.ModelSerializer):
     class Meta:
         model = Project
         fields = (
             'Id',
             'ModelPic',
             'Created',
             'Title' ,
             'HoursSpent' ,
             'HoursEstimated',
             'LastBuildDate',
             'NextBuildDate',
             'IsPending',
             'IsDeliever',
         )

#JSON for UserFetch
class UserFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'Id',
            'username',
            'first_name',
            'last_name',
            'UserType',
            'email',
        )

#JSON for UserCreate
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'Id',
            'username',
            'password',
            'first_name',
            'last_name',
            'UserType',
            'email'
        )

class UserLogDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = (
            'Id',
            'Name',
            'Action',
            'Time',
        )

#JSON for UserLogin
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )




