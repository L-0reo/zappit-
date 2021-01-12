from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

class PostList(generics.ListCreateAPIView): #this helps list and create Post objects
    queryset = Post.objects.all() #specifies what objects to fetch from db for listing
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user) #create a new Post for that user


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):  #to go /api/post/<'int'>
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):   #so a user can only delete his own posts
        post = Post.objects.filter(pk=self.kwargs['pk'], poster=self.request.user) #only fetches that certain post because of pk
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  #instead of queryset we override this function to know which instance of Vote (with which user) to get for listing out
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk']) #specify which Post to vote on

        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You already voted on this post :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))  #to specify which post exactly is getting voted

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You don\'t have a vote on this post')
