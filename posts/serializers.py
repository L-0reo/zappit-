from rest_framework import serializers

from .models import Post, Vote

class PostSerializer(serializers.ModelSerializer): #ModelSerializer makes it easy to translate an API call into a model that we created
    poster = serializers.ReadOnlyField(source='poster.username') #this is to make sure the API poster can not post as another person
    poster_id = serializers.ReadOnlyField(source='poster.id') #this is to make sure the API poster can not post as another person
    votes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'votes' ] #id isn't specifically listed but it's automatically included in every Django model.
                                                                                    # poster_id is automatically included with authentication
    def get_votes(self, post): #to be able to see total votes on each post in APIView
        return Vote.objects.filter(post=post).count()
                                                                           #these fields will show up on API page

#so when somebody wants to see a post in our reddit clone, it's gonna come out as a model and this serializer is goint to turn it into a api and viceversa when creating

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
