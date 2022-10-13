from rest_framework import serializers
from .models import Artist, Song

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    songs = serializers.HyperlinkedRelatedField(
        view_name='song_detail',
        many=True,
        read_only=True,
    )

    artist_url = serializers.ModelSerializer.serializer_url_field(
        view_name='artist_detail'
    )

    class Meta:
        model = Artist
        fields = ('id', 'artist_url', 'img', 'bio', 'name', 'songs',)

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('pk', 'title', 'length', 'artist',)